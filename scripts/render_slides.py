from __future__ import annotations

import argparse
import html
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

WINDOWS_BROWSER_PATHS = [
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]

MACOS_BROWSER_PATHS = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
]

LINUX_BROWSER_COMMANDS = [
    "google-chrome",
    "google-chrome-stable",
    "microsoft-edge",
    "microsoft-edge-stable",
    "chromium",
    "chromium-browser",
]


def safe_survey_key(value: str) -> str:
    survey_key = value.strip()
    blocked = set('/\\:*?"<>|')
    if not survey_key or survey_key in {".", ".."} or any(ch in blocked for ch in survey_key):
        raise SystemExit("Survey key must be a simple folder-safe name.")
    return survey_key


def parse_front_matter(text: str) -> tuple[dict[str, str], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    metadata: dict[str, str] = {}
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return metadata, "\n".join(lines[index + 1 :])
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"').strip("'")
    return {}, text


def split_slides(text: str) -> list[str]:
    slides: list[list[str]] = [[]]
    for line in text.splitlines():
        if line.strip() == "---":
            if slides[-1]:
                slides.append([])
            continue
        slides[-1].append(line)
    return ["\n".join(slide).strip() for slide in slides if "\n".join(slide).strip()]


def inline_markdown(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"`([^`]+)`", r"<code>\1</code>", escaped)
    escaped = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", escaped)
    escaped = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2">\1</a>', escaped)
    return escaped


def local_asset_path(source_dir: Path, src: str) -> Path | None:
    if re.match(r"^[a-z]+://", src) or src.startswith("#"):
        return None
    candidate = (source_dir / src).resolve()
    try:
        candidate.relative_to(source_dir.resolve())
    except ValueError:
        return None
    return candidate


def copy_asset(source_dir: Path, output_dir: Path, src: str) -> str | None:
    asset = local_asset_path(source_dir, src)
    if asset is None or not asset.exists() or not asset.is_file():
        return None
    relative = asset.relative_to(source_dir.resolve())
    destination = output_dir / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(asset, destination)
    return relative.as_posix()


def image_html(source_dir: Path, output_dir: Path, alt: str, src: str) -> str:
    copied_src = copy_asset(source_dir, output_dir, src)
    if copied_src is None:
        return (
            '<div class="asset-placeholder">'
            f"<strong>Missing asset</strong><br>{html.escape(src)}<br>"
            "Run the analysis step to create this input."
            "</div>"
        )
    return f'<figure><img src="{html.escape(copied_src)}" alt="{html.escape(alt)}"><figcaption>{inline_markdown(alt)}</figcaption></figure>'


def include_markdown(line: str, source_dir: Path) -> list[str] | None:
    match = re.fullmatch(r"\{\{\s*include\s+([^}]+?)\s*\}\}", line.strip())
    if not match:
        return None
    include_path = local_asset_path(source_dir, match.group(1).strip())
    if include_path is None or not include_path.exists():
        return [
            f"**Missing include:** `{match.group(1).strip()}`",
            "Run the analysis step to create this input.",
        ]
    return include_path.read_text(encoding="utf-8").splitlines()


def is_table_separator(line: str) -> bool:
    cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def render_table(lines: list[str]) -> str:
    rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
    header = rows[0]
    body = rows[2:] if len(rows) > 1 and is_table_separator(lines[1]) else rows[1:]
    html_rows = ["<table>", "<thead><tr>"]
    html_rows.extend(f"<th>{inline_markdown(cell)}</th>" for cell in header)
    html_rows.append("</tr></thead>")
    html_rows.append("<tbody>")
    for row in body:
        html_rows.append("<tr>")
        html_rows.extend(f"<td>{inline_markdown(cell)}</td>" for cell in row)
        html_rows.append("</tr>")
    html_rows.append("</tbody></table>")
    return "".join(html_rows)


def render_blocks(markdown: str, source_dir: Path, output_dir: Path) -> str:
    raw_lines: list[str] = []
    for line in markdown.splitlines():
        included = include_markdown(line, source_dir)
        if included is None:
            raw_lines.append(line)
        else:
            raw_lines.extend(included)

    parts: list[str] = []
    index = 0
    in_code = False
    code_lang = ""
    code_lines: list[str] = []

    def flush_code() -> None:
        nonlocal code_lines, code_lang
        lang_class = f' class="language-{html.escape(code_lang)}"' if code_lang else ""
        parts.append(f"<pre><code{lang_class}>{html.escape(chr(10).join(code_lines))}</code></pre>")
        code_lines = []
        code_lang = ""

    while index < len(raw_lines):
        line = raw_lines[index]

        if line.startswith("```"):
            if in_code:
                flush_code()
                in_code = False
            else:
                in_code = True
                code_lang = line.strip().removeprefix("```").strip()
            index += 1
            continue

        if in_code:
            code_lines.append(line)
            index += 1
            continue

        if not line.strip():
            index += 1
            continue

        image_match = re.fullmatch(r"!\[([^\]]*)\]\(([^)]+)\)", line.strip())
        if image_match:
            parts.append(image_html(source_dir, output_dir, image_match.group(1), image_match.group(2)))
            index += 1
            continue

        if line.lstrip().startswith("|"):
            table_lines = []
            while index < len(raw_lines) and raw_lines[index].lstrip().startswith("|"):
                table_lines.append(raw_lines[index])
                index += 1
            parts.append(render_table(table_lines))
            continue

        heading_match = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            parts.append(f"<h{level}>{inline_markdown(heading_match.group(2))}</h{level}>")
            index += 1
            continue

        if re.match(r"^\s*[-*]\s+", line):
            items = []
            while index < len(raw_lines) and re.match(r"^\s*[-*]\s+", raw_lines[index]):
                items.append(re.sub(r"^\s*[-*]\s+", "", raw_lines[index]))
                index += 1
            parts.append("<ul>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ul>")
            continue

        if re.match(r"^\s*\d+\.\s+", line):
            items = []
            while index < len(raw_lines) and re.match(r"^\s*\d+\.\s+", raw_lines[index]):
                items.append(re.sub(r"^\s*\d+\.\s+", "", raw_lines[index]))
                index += 1
            parts.append("<ol>" + "".join(f"<li>{inline_markdown(item)}</li>" for item in items) + "</ol>")
            continue

        paragraph = [line.strip()]
        index += 1
        while index < len(raw_lines) and raw_lines[index].strip() and not re.match(
            r"^(#{1,6})\s+|^\s*[-*]\s+|^\s*\d+\.\s+|^\s*\||```|!\[", raw_lines[index]
        ):
            paragraph.append(raw_lines[index].strip())
            index += 1
        parts.append(f"<p>{inline_markdown(' '.join(paragraph))}</p>")

    if in_code:
        flush_code()
    return "\n".join(parts)


def page_template(metadata: dict[str, str], slide_html: list[str]) -> str:
    title = metadata.get("title") or "Survey Slides"
    subtitle = metadata.get("subtitle", "")
    author = metadata.get("author", "")
    slides = "\n".join(
        f'<section class="slide" data-slide="{index}">{content}</section>'
        for index, content in enumerate(slide_html, start=1)
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #52606d;
      --accent: #2f6f8f;
      --accent-2: #b7553d;
      --paper: #fbfbf8;
      --panel: #ffffff;
      --rule: #d8ded8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      min-height: 100vh;
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: var(--paper);
      color: var(--ink);
    }}
    .deck {{
      min-height: 100vh;
      display: grid;
      grid-template-rows: 1fr auto;
    }}
    .slide {{
      display: none;
      min-height: 100vh;
      padding: clamp(2rem, 5vw, 5rem);
      align-content: center;
      max-width: 1180px;
      width: 100%;
      margin: 0 auto;
    }}
    .slide.active {{ display: grid; gap: 1.25rem; }}
    h1, h2, h3 {{ margin: 0; line-height: 1.08; letter-spacing: 0; }}
    h1 {{ font-size: clamp(2.5rem, 7vw, 5.8rem); max-width: 12ch; }}
    h2 {{ font-size: clamp(2rem, 5vw, 4rem); color: var(--accent); }}
    h3 {{ font-size: clamp(1.4rem, 3vw, 2.2rem); }}
    p, li, td, th {{
      font-size: clamp(1.05rem, 2vw, 1.55rem);
      line-height: 1.45;
    }}
    p {{ max-width: 70ch; color: var(--muted); }}
    ol, ul {{ margin: 0; padding-left: 1.5em; max-width: 70ch; }}
    li + li {{ margin-top: 0.45rem; }}
    code {{
      font-family: "Cascadia Mono", "SFMono-Regular", Consolas, monospace;
      background: #eef3f1;
      padding: 0.12em 0.32em;
      border-radius: 4px;
      color: #12313f;
    }}
    pre {{
      width: min(100%, 980px);
      overflow-x: auto;
      background: #10252f;
      color: #eef8fb;
      padding: 1rem 1.2rem;
      border-radius: 8px;
      border-left: 6px solid var(--accent-2);
    }}
    pre code {{ background: transparent; color: inherit; padding: 0; }}
    figure {{ margin: 0; display: grid; gap: 0.5rem; justify-items: start; }}
    img {{
      max-width: min(100%, 980px);
      max-height: 68vh;
      border: 1px solid var(--rule);
      background: var(--panel);
      box-shadow: 0 18px 48px rgba(20, 35, 45, 0.12);
    }}
    figcaption {{ color: var(--muted); font-size: 0.95rem; }}
    table {{
      border-collapse: collapse;
      min-width: min(100%, 760px);
      background: var(--panel);
      border: 1px solid var(--rule);
      box-shadow: 0 14px 36px rgba(20, 35, 45, 0.08);
    }}
    th, td {{ padding: 0.75rem 1rem; border-bottom: 1px solid var(--rule); text-align: left; }}
    th {{ color: var(--accent); font-weight: 700; }}
    .asset-placeholder {{
      width: min(100%, 820px);
      padding: 2rem;
      border: 2px dashed var(--rule);
      border-radius: 8px;
      color: var(--muted);
      background: rgba(255, 255, 255, 0.65);
      font-size: 1.2rem;
    }}
    .chrome {{
      position: fixed;
      left: 0;
      right: 0;
      bottom: 0;
      display: flex;
      align-items: center;
      gap: 1rem;
      padding: 0.75rem 1rem;
      background: rgba(251, 251, 248, 0.92);
      border-top: 1px solid var(--rule);
      backdrop-filter: blur(8px);
    }}
    .meta {{ color: var(--muted); font-size: 0.9rem; flex: 1; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
    .counter {{ color: var(--muted); font-variant-numeric: tabular-nums; }}
    button {{
      border: 1px solid var(--rule);
      background: var(--panel);
      color: var(--ink);
      border-radius: 6px;
      padding: 0.45rem 0.7rem;
      cursor: pointer;
    }}
    button:hover {{ border-color: var(--accent); color: var(--accent); }}
    .progress {{
      position: fixed;
      top: 0;
      left: 0;
      height: 5px;
      background: var(--accent-2);
      width: 0;
      transition: width 140ms ease-out;
    }}
    @media print {{
      .slide {{ display: grid; min-height: 100vh; page-break-after: always; }}
      .chrome, .progress {{ display: none; }}
      img, table {{ box-shadow: none; }}
    }}
  </style>
</head>
<body>
  <div class="progress" id="progress"></div>
  <main class="deck">
    {slides}
  </main>
  <nav class="chrome" aria-label="Slide controls">
    <button type="button" id="previous" aria-label="Previous slide">Prev</button>
    <button type="button" id="next" aria-label="Next slide">Next</button>
    <div class="meta">{html.escape(title)}{(" - " + html.escape(subtitle)) if subtitle else ""}{(" - " + html.escape(author)) if author else ""}</div>
    <div class="counter"><span id="current">1</span>/<span id="total">1</span></div>
  </nav>
  <script>
    const slides = Array.from(document.querySelectorAll('.slide'));
    const total = document.getElementById('total');
    const current = document.getElementById('current');
    const progress = document.getElementById('progress');
    total.textContent = slides.length;
    let index = Math.max(0, Math.min(slides.length - 1, Number(location.hash.replace('#', '')) - 1 || 0));
    function show(nextIndex) {{
      index = Math.max(0, Math.min(slides.length - 1, nextIndex));
      slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
      current.textContent = index + 1;
      progress.style.width = `${{((index + 1) / slides.length) * 100}}%`;
      history.replaceState(null, '', `#${{index + 1}}`);
    }}
    document.getElementById('previous').addEventListener('click', () => show(index - 1));
    document.getElementById('next').addEventListener('click', () => show(index + 1));
    document.addEventListener('keydown', (event) => {{
      if (['ArrowRight', 'PageDown', ' '].includes(event.key)) show(index + 1);
      if (['ArrowLeft', 'PageUp'].includes(event.key)) show(index - 1);
      if (event.key === 'Home') show(0);
      if (event.key === 'End') show(slides.length - 1);
    }});
    show(index);
  </script>
</body>
</html>
"""


def candidate_browser_paths(system: str | None = None) -> list[str]:
    system_name = system or platform.system()
    if system_name == "Windows":
        commands = ["msedge", "chrome", "chromium", "chromium-browser"]
        return commands + WINDOWS_BROWSER_PATHS
    if system_name == "Darwin":
        commands = ["google-chrome", "microsoft-edge", "chromium"]
        return commands + MACOS_BROWSER_PATHS
    return LINUX_BROWSER_COMMANDS


def find_browser() -> str | None:
    for candidate in candidate_browser_paths():
        path = Path(candidate)
        if path.is_absolute() and path.exists():
            return str(path)
        resolved = shutil.which(candidate)
        if resolved:
            return resolved
    return None


def export_pdf(html_file: Path, pdf_file: Path, browser: str | None = None) -> Path:
    browser_path = browser or find_browser()
    if not browser_path:
        raise SystemExit(
            "Could not find Chrome, Edge, or Chromium for PDF export. "
            "Open the HTML deck in a browser and use Print to PDF, or install one of those browsers."
        )

    html_uri = html_file.resolve().as_uri()
    pdf_file.parent.mkdir(parents=True, exist_ok=True)
    command = [
        browser_path,
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        "--print-to-pdf-no-header",
        f"--print-to-pdf={pdf_file}",
        html_uri,
    ]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        if detail:
            detail = f" Details: {detail[:800]}"
        raise SystemExit(f"Browser PDF export failed with exit code {result.returncode}.{detail}")
    if not pdf_file.exists():
        raise SystemExit(f"Browser PDF export completed, but expected PDF was not created: {pdf_file}")
    return pdf_file


def render_slides(survey_key: str, project_root: Path = PROJECT_ROOT) -> Path:
    survey_key = safe_survey_key(survey_key)
    source_dir = project_root / "slides" / survey_key
    input_file = source_dir / "slides.md"
    if not input_file.exists():
        raise SystemExit(f"Slide file not found: {input_file}")

    output_dir = project_root / "build" / "slides" / survey_key
    output_dir.mkdir(parents=True, exist_ok=True)

    metadata, body = parse_front_matter(input_file.read_text(encoding="utf-8"))
    rendered_slides = [
        render_blocks(slide, source_dir=source_dir, output_dir=output_dir)
        for slide in split_slides(body)
    ]
    output_file = output_dir / "slides.html"
    output_file.write_text(page_template(metadata, rendered_slides), encoding="utf-8")
    return output_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Render a survey Markdown deck to native HTML slides.")
    parser.add_argument("--survey-key", default="repo_smoke_test")
    parser.add_argument("--pdf", action="store_true", help="Also export slides.pdf using Chrome/Edge/Chromium.")
    parser.add_argument("--browser", help="Path to Chrome, Edge, or Chromium for --pdf.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_file = render_slides(args.survey_key)
    print(f"Rendered slides: {output_file}")
    if args.pdf:
        pdf_file = output_file.with_suffix(".pdf")
        export_pdf(output_file, pdf_file, browser=args.browser)
        print(f"Rendered PDF: {pdf_file}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
