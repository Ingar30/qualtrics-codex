from __future__ import annotations

import argparse
import html
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SURVEY_KEY = "repo_smoke_test"
SYNTHETIC_FIXTURE = Path("build/fixtures/repo_smoke_test_responses.csv")
DEMO_SURVEY_KEY = "discrimination_beliefs_demo"
DEMO_SYNTHETIC_FIXTURE = Path("build/fixtures/discrimination_beliefs_demo_responses.csv")


def run_command(command: list[str], project_root: Path) -> None:
    result = subprocess.run(command, cwd=project_root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        output = "\n".join(part for part in [result.stdout, result.stderr] if part)
        raise SystemExit(f"Command failed: {' '.join(command)}\n{output[-2000:]}")


def clean_output(output_dir: Path) -> None:
    if output_dir.exists():
        shutil.rmtree(output_dir)
    (output_dir / "artifacts").mkdir(parents=True, exist_ok=True)


def copy_file(source: Path, destination: Path) -> Path | None:
    if not source.exists():
        return None
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return destination


def zip_matching(paths: list[Path], destination: Path) -> Path:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in paths:
            if path.exists() and path.is_file():
                archive.write(path, arcname=path.name)
    return destination


def page_template(title: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    :root {{
      --ink: #14202b;
      --muted: #52616f;
      --accent: #1f5f7a;
      --accent-2: #c7522a;
      --paper: #f6f8fa;
      --panel: #ffffff;
      --rule: #d9e1e8;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      color: var(--ink);
      background: var(--paper);
      line-height: 1.55;
    }}
    header {{
      background: linear-gradient(135deg, #17364a, #1f7a8c);
      color: #ffffff;
      padding: 4rem 1.5rem;
    }}
    main, .inner {{
      width: min(1080px, calc(100% - 2rem));
      margin: 0 auto;
    }}
    h1 {{ margin: 0 0 0.75rem; font-size: clamp(2.2rem, 6vw, 4.7rem); line-height: 1; }}
    h2 {{ margin-top: 2.4rem; color: var(--accent); }}
    p {{ color: var(--muted); max-width: 72ch; }}
    a {{ color: var(--accent); font-weight: 650; }}
    code {{
      background: #eef3f6;
      border: 1px solid var(--rule);
      border-radius: 4px;
      padding: 0.1rem 0.28rem;
    }}
    pre {{
      overflow-x: auto;
      background: #101b24;
      color: #edf7fb;
      border-radius: 8px;
      padding: 1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
      gap: 1rem;
      margin: 1rem 0 2rem;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--rule);
      border-radius: 8px;
      padding: 1rem;
    }}
    .card strong {{ display: block; margin-bottom: 0.3rem; }}
    .warning {{
      border-left: 5px solid var(--accent-2);
      background: #fff7f3;
      padding: 1rem;
      border-radius: 6px;
    }}
    footer {{ padding: 2rem 1rem 3rem; color: var(--muted); }}
  </style>
</head>
<body>
{body}
</body>
</html>
"""


def build_index(output_dir: Path, artifact_names: list[str]) -> None:
    cards = "\n".join(
        f'<article class="card"><strong>{html.escape(name)}</strong><a href="artifacts/{html.escape(name)}">Download</a></article>'
        for name in artifact_names
    )
    body = f"""
<header>
  <div class="inner">
    <h1>qualtrics-codex</h1>
    <p>A public starter workflow for economists using Qualtrics, Stata or Python, and Beamer or native HTML slides.</p>
  </div>
</header>
<main>
  <section>
    <h2>Demo Artifacts</h2>
    <p>These downloads are built from synthetic fixture data only. They do not contain real Qualtrics responses or private survey metadata.</p>
    <div class="grid">
      {cards}
    </div>
  </section>
  <section>
    <h2>Codex Loop</h2>
    <p>Ask Codex for a survey from exact questions or a broad idea. It should scaffold the survey, ask whether you want a quick local smoke test, a live Qualtrics test survey with synthetic response submission, or a real response export, then clean data and build figures and slides.</p>
    <pre><code>Create a public opinion survey on beliefs about discrimination in hiring in Qualtrics. Then generate 100 synthetic responses on Qualtrics, download and clean the generated data, create figures, and compile slides that summarize the workflow, survey design, synthetic response patterns, and main figures. Include the survey link in the slides.</code></pre>
    <p>Because this prompt asks for work on Qualtrics, Codex should verify credentials without printing them and ask before creating the draft survey, submitting synthetic responses, or exporting responses. For a no-credentials smoke test, ask Codex to generate disposable local responses only to check analysis and slides.</p>
    <p>For local preferences, start with <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/prompts/configure-local-preferences.md">prompts/configure-local-preferences.md</a>. Stata workflows use SPSS/SAV exports; Python workflows use CSV exports.</p>
    <p>For the full conversational workflow, see <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/docs/intended-codex-loop.md">docs/intended-codex-loop.md</a>.</p>
    <p>For the discrimination-beliefs prompt, see <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/prompts/discrimination-beliefs-example.md">prompts/discrimination-beliefs-example.md</a>.</p>
  </section>
  <section>
    <h2>Run Locally</h2>
    <pre><code>git clone https://github.com/Ingar30/qualtrics-codex.git
cd qualtrics-codex
.\\scripts\\setup.ps1
codex
python scripts/generate_synthetic_responses.py --survey-key repo_smoke_test --output build/fixtures/repo_smoke_test_responses.csv
python scripts/run_analysis.py --survey-key repo_smoke_test --input build/fixtures/repo_smoke_test_responses.csv
python scripts/build_slides.py --survey-key repo_smoke_test</code></pre>
    <p>After opening Codex, paste the starter prompt from <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/prompts/start-with-codex.md">prompts/start-with-codex.md</a>.</p>
    <p>For plain-language Codex prompts that mirror the commands, see <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/docs/codex-prompt-alternatives.md">docs/codex-prompt-alternatives.md</a>.</p>
    <p>If virtual environment setup fails or Stata is not found, see <a href="https://github.com/Ingar30/qualtrics-codex/blob/main/docs/setup-troubleshooting.md">docs/setup-troubleshooting.md</a>.</p>
  </section>
  <section class="warning">
    <strong>Private by default.</strong>
    Raw exports, processed real data, metadata, survey IDs, reusable links, and API tokens should stay local unless you explicitly decide otherwise.
  </section>
  <section>
    <h2>Live Qualtrics Loop</h2>
    <p>Store credentials outside the repository, start with <code>check-auth</code>, save reusable links only to ignored local files, submit generated synthetic rows to the test survey, export once, analyze once, and build slides. See <a href="walkthrough.html">the walkthrough</a> and <a href="validation.html">the validation notes</a>.</p>
  </section>
  <section>
    <h2>Validated Full Loop</h2>
    <p>A local live run validated the lean command loop with 100 synthetic Qualtrics submissions, one export, one analysis pass, and slide output. Public Pages artifacts remain synthetic-only; live validation runs locally with user secrets.</p>
    <pre><code>python scripts/run_live_validation.py --survey-key &lt;survey_key&gt; --survey-name "&lt;survey name&gt;" --spec-file code/&lt;survey_key&gt;/survey_spec.json --n 100 --dry-run</code></pre>
  </section>
</main>
<footer>
  <div class="inner">Built from synthetic data by the repository's Python site builder.</div>
</footer>
"""
    (output_dir / "index.html").write_text(page_template("qualtrics-codex", body), encoding="utf-8")


def build_walkthrough(output_dir: Path) -> None:
    body = """
<header>
  <div class="inner">
    <h1>Local Workflow</h1>
    <p>Use the public repo as a local research scaffold. Keep Qualtrics credentials and real response data off GitHub.</p>
  </div>
</header>
<main>
  <h2>1. Store Secrets Locally</h2>
  <p>Synthetic tests do not need Qualtrics credentials. For live API calls, store credentials outside the repository.</p>
  <p>Qualtrics documents API tokens under Account Settings, in the Qualtrics IDs area: <a href="https://www.qualtrics.com/support/integrations/api-integration/overview/">Qualtrics API overview</a>.</p>
  <p>On Windows PowerShell, create <code>$HOME\\.secrets\\qualtrics.env.ps1</code>:</p>
  <pre><code>$env:QUALTRICS_DATACENTER = "your_datacenter"
$env:QUALTRICS_API_TOKEN = "your_token"
$env:QUALTRICS_PUBLIC_HOST = "yourbrand.qualtrics.com"</code></pre>
  <p>Load it before live API calls:</p>
  <pre><code>. $HOME\\.secrets\\qualtrics.env.ps1</code></pre>
  <p>On macOS/Linux, create <code>$HOME/.secrets/qualtrics.env</code>:</p>
  <pre><code>export QUALTRICS_DATACENTER="your_datacenter"
export QUALTRICS_API_TOKEN="your_token"
export QUALTRICS_PUBLIC_HOST="yourbrand.qualtrics.com"</code></pre>
  <p>Load it before live API calls:</p>
  <pre><code>source "$HOME/.secrets/qualtrics.env"</code></pre>

  <h2>2. Export Responses</h2>
  <p>Use CSV for Python analysis and SPSS/SAV for Stata analysis.</p>
  <pre><code>python scripts/qualtrics_workflow.py check-auth
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --survey-id &lt;survey_id&gt; --format csv
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --survey-id &lt;survey_id&gt; --format spss</code></pre>

  <h2>3. Live Synthetic Test</h2>
  <pre><code>python scripts/qualtrics_workflow.py get-link --survey-key my_survey --write-slide-inputs
python scripts/generate_synthetic_responses.py --survey-key my_survey --output build/fixtures/my_survey_responses.csv --n 100
python scripts/qualtrics_workflow.py submit-synthetic-responses --survey-key my_survey --input build/fixtures/my_survey_responses.csv
python scripts/qualtrics_workflow.py export-responses --survey-key my_survey --format csv
python scripts/run_analysis.py --survey-key my_survey
python scripts/build_slides.py --survey-key my_survey</code></pre>
  <p>For a cautious first live check, add <code>--limit 1</code>, export and inspect that row, then continue later with <code>--resume</code>.</p>

  <h2>4. Smoke Test With Local Synthetic Responses</h2>
  <pre><code>python scripts/generate_synthetic_responses.py --survey-key my_survey --output build/fixtures/my_survey_responses.csv
python scripts/run_analysis.py --survey-key my_survey --input build/fixtures/my_survey_responses.csv
python scripts/build_slides.py --survey-key my_survey</code></pre>

  <h2>5. Analyze And Build Real Local Exports</h2>
  <pre><code>python scripts/run_analysis.py --survey-key my_survey
python scripts/build_slides.py --survey-key my_survey</code></pre>
  <p>Qualtrics CSV exports may include metadata rows after the header. The example analysis filters them when <code>ResponseId</code> exists by keeping IDs that start with <code>R_</code>.</p>

  <h2>Public Boundary</h2>
  <p>Publish synthetic/demo artifacts freely. Do not publish raw exports, processed real data, survey links, metadata, or secrets by default. Reusable links saved by <code>get-link</code> are local/private by default.</p>
  <p>Draft or inactive surveys may still accept API-created test responses. Treat API response submission as a live mutation.</p>
</main>
<footer><div class="inner"><a href="index.html">Back to demo artifacts</a></div></footer>
"""
    (output_dir / "walkthrough.html").write_text(page_template("Local workflow", body), encoding="utf-8")



def build_validation(output_dir: Path) -> None:
    body = """
<header>
  <div class="inner">
    <h1>Validated Full Loop</h1>
    <p>Public artifacts are synthetic-only. Live Qualtrics validation is local, lean, and credential-dependent.</p>
  </div>
</header>
<main>
  <section>
    <h2>What Was Validated</h2>
    <p>A local live run validated the repository command loop directly: create a Qualtrics test survey, save the reusable link only to ignored local files, prepare and submit 100 synthetic responses through Qualtrics, export responses once, clean to 100 rows, generate figures, and build slides.</p>
    <p>On May 12, 2026, the labor-market and immigration prompt completed through the same local loop with 100 synthetic Qualtrics submissions. This page records only the sanitized validation result.</p>
  </section>
  <section>
    <h2>Public Boundary</h2>
    <p>CI and GitHub Pages never call Qualtrics. They do not publish survey IDs, response IDs, reusable links, raw rows, metadata, tokens, or Qualtrics URLs. Public downloads are built from synthetic fixture data only.</p>
  </section>
  <section>
    <h2>Lean Helper</h2>
    <pre><code>python scripts/run_live_validation.py --survey-key &lt;survey_key&gt; --survey-name "&lt;survey name&gt;" --spec-file code/&lt;survey_key&gt;/survey_spec.json --n 100 --dry-run</code></pre>
    <p>Remove <code>--dry-run</code> only when you explicitly want local live Qualtrics calls with your own secrets.</p>
    <p>Add <code>--export-format spss</code> for the Stata/SAV validation path. Use the default CSV export for Python-first validation.</p>
  </section>
  <section>
    <h2>Cleanup</h2>
    <p>Live validation creates a draft or test survey in Qualtrics. Archive or delete test surveys manually in the Qualtrics UI after validation.</p>
  </section>
</main>
<footer><div class="inner"><a href="index.html">Back to demo artifacts</a></div></footer>
"""
    (output_dir / "validation.html").write_text(page_template("Validated full loop", body), encoding="utf-8")

def build_site(project_root: Path = PROJECT_ROOT, output_dir: Path | None = None) -> Path:
    output_dir = output_dir or project_root / "site"
    clean_output(output_dir)

    run_command(
        [
            sys.executable,
            "scripts/generate_synthetic_responses.py",
            "--survey-key",
            SURVEY_KEY,
            "--output",
            str(SYNTHETIC_FIXTURE),
        ],
        project_root,
    )
    run_command(
        [
            sys.executable,
            "scripts/generate_synthetic_responses.py",
            "--survey-key",
            DEMO_SURVEY_KEY,
            "--output",
            str(DEMO_SYNTHETIC_FIXTURE),
            "--n",
            "100",
        ],
        project_root,
    )
    run_command(
        [
            sys.executable,
            "scripts/run_analysis.py",
            "--survey-key",
            SURVEY_KEY,
            "--input",
            str(SYNTHETIC_FIXTURE),
            "--mode",
            "python",
        ],
        project_root,
    )
    run_command([sys.executable, "scripts/build_slides.py", "--survey-key", SURVEY_KEY, "--mode", "auto"], project_root)
    run_command(
        [
            sys.executable,
            "scripts/build_slides.py",
            "--survey-key",
            SURVEY_KEY,
            "--mode",
            "python",
            "--no-python-pdf",
        ],
        project_root,
    )
    run_command(
        [
            sys.executable,
            "scripts/run_analysis.py",
            "--survey-key",
            DEMO_SURVEY_KEY,
            "--input",
            str(DEMO_SYNTHETIC_FIXTURE),
            "--mode",
            "python",
        ],
        project_root,
    )
    run_command([sys.executable, "scripts/build_slides.py", "--survey-key", DEMO_SURVEY_KEY, "--mode", "auto"], project_root)
    run_command(
        [
            sys.executable,
            "scripts/build_slides.py",
            "--survey-key",
            DEMO_SURVEY_KEY,
            "--mode",
            "python",
            "--no-python-pdf",
        ],
        project_root,
    )

    artifacts_dir = output_dir / "artifacts"
    copied: list[str] = []

    for key, prefix in [(SURVEY_KEY, "smoke"), (DEMO_SURVEY_KEY, "discrimination-beliefs-demo")]:
        slide_build_dir = project_root / "build" / "slides" / key
        inputs_dir = project_root / "slides" / key / "inputs"
        for source, name in [
            (slide_build_dir / "slides.pdf", f"{prefix}-slides.pdf"),
            (slide_build_dir / "slides.html", f"{prefix}-slides.html"),
        ]:
            if copy_file(source, artifacts_dir / name):
                copied.append(name)

        figure_paths = sorted(inputs_dir.glob("*.pdf")) + sorted(inputs_dir.glob("*.png"))
        table_paths = [path for path in [inputs_dir / "summary.md", inputs_dir / "summary.tex"] if path.exists()]
        zip_matching(figure_paths, artifacts_dir / f"{prefix}-figures.zip")
        zip_matching(table_paths, artifacts_dir / f"{prefix}-tables.zip")
        copied.extend([f"{prefix}-figures.zip", f"{prefix}-tables.zip"])

    build_walkthrough(output_dir)
    copied.append("walkthrough.html")
    build_validation(output_dir)
    copied.append("validation.html")
    build_index(output_dir, copied)
    (output_dir / ".nojekyll").write_text("", encoding="utf-8")
    (output_dir / ".gitkeep").write_text("", encoding="utf-8")
    return output_dir


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build the synthetic-data GitHub Pages site.")
    parser.add_argument("--output-dir", default="site")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_dir = build_site(output_dir=(PROJECT_ROOT / args.output_dir).resolve())
    print(f"Built site: {output_dir}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
