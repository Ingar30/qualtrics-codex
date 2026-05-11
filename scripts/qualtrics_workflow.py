from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import uuid
import zipfile
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"


DEFAULT_SURVEY_SPEC = {
    "questions": [
        {
            "tag": "role",
            "type": "mc",
            "text": "Which role best describes you?",
            "choices": ["Student", "Instructor", "Researcher", "Administrator", "Other"],
        },
        {
            "tag": "workflow_familiarity",
            "type": "mc",
            "text": "How familiar are you with reproducible data workflows?",
            "choices": [
                "Not familiar",
                "Slightly familiar",
                "Moderately familiar",
                "Very familiar",
                "Extremely familiar",
            ],
        },
    ]
}


class QualtricsApiError(RuntimeError):
    def __init__(self, method: str, path: str, message: str) -> None:
        super().__init__(redact_sensitive_text(f"{method} {path}: {message}"))
        self.method = method
        self.path = path


def load_project_env() -> None:
    env_path = PROJECT_ROOT / ".env"
    if not env_path.exists():
        return
    try:
        from dotenv import load_dotenv

        load_dotenv(env_path)
        return
    except ImportError:
        pass

    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        name, value = line.split("=", 1)
        name = name.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(name, value)


def load_requests():
    try:
        import requests
    except ImportError as exc:
        raise SystemExit(
            "The Python package 'requests' is required. "
            "Run: python -m pip install -r requirements.txt "
            "or py -3 -m pip install --user -r requirements.txt"
        ) from exc
    return requests


def require_env(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise SystemExit(
            f"{name} is missing. Load it from your local secrets file or shell environment. "
            "See docs/local-qualtrics-secrets.md."
        )
    return value


def safe_survey_key(survey_key: str) -> str:
    value = survey_key.strip()
    blocked = set('/\\:*?"<>|')
    if not value or value in {".", ".."} or any(ch in blocked for ch in value):
        raise SystemExit("Survey key must be a simple folder-safe name.")
    return value


def build_base_url(datacenter: str) -> str:
    value = datacenter.strip().removeprefix("https://").removeprefix("http://")
    value = value.removesuffix("/API/v3").strip("/")
    host = value if value.endswith(".qualtrics.com") else f"{value}.qualtrics.com"
    return f"https://{host}/API/v3"


QUALTRICS_LINK_RE = re.compile(r"https?://[^\s\"'<>]*qualtrics\.com[^\s\"'<>]*", re.IGNORECASE)
QUALTRICS_ID_RE = re.compile(r"\b(SV|BL|FL|R)_[A-Za-z0-9]+")


def redact_sensitive_text(text: object, token: str | None = None) -> str:
    value = str(text)
    if token:
        value = value.replace(token, "[QUALTRICS_API_TOKEN]")
    value = QUALTRICS_LINK_RE.sub("[QUALTRICS_LINK]", value)
    value = QUALTRICS_ID_RE.sub(lambda match: f"[{match.group(1)}_ID]", value)
    return value[:1200]


def sanitize_text(text: str, token: str) -> str:
    return redact_sensitive_text(text, token)


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def metadata_path(survey_key: str) -> Path:
    return DATA_DIR / safe_survey_key(survey_key) / "metadata" / "survey_info.json"


def default_spec_path(survey_key: str) -> Path:
    return PROJECT_ROOT / "code" / safe_survey_key(survey_key) / "survey_spec.json"


def load_metadata(survey_key: str) -> dict[str, Any]:
    path = metadata_path(survey_key)
    if path.exists():
        return read_json(path)
    return {}


def save_metadata(survey_key: str, metadata: dict[str, Any]) -> Path:
    path = metadata_path(survey_key)
    write_json(path, metadata)
    return path


def write_survey_link_slide_inputs(survey_key: str, reusable_link: str) -> tuple[Path, Path]:
    inputs_dir = PROJECT_ROOT / "slides" / safe_survey_key(survey_key) / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)
    tex_path = inputs_dir / "survey_link.tex"
    md_path = inputs_dir / "survey_link.md"
    tex_path.write_text(f"\\url{{{reusable_link}}}\n", encoding="utf-8")
    md_path.write_text(f"Reusable test link: [{reusable_link}]({reusable_link})\n", encoding="utf-8")
    return tex_path, md_path


def load_survey_spec(spec_file: str | None) -> dict[str, Any]:
    if not spec_file:
        return DEFAULT_SURVEY_SPEC

    path = Path(spec_file)
    if not path.is_absolute():
        path = PROJECT_ROOT / path
    data = read_json(path)
    questions = data.get("questions")
    if not isinstance(questions, list) or not questions:
        raise SystemExit("Survey spec must include a non-empty 'questions' list.")

    seen_tags: set[str] = set()
    for question in questions:
        for field in ["tag", "type", "text"]:
            if not question.get(field):
                raise SystemExit(f"Survey question is missing required field: {field}")
        tag = str(question["tag"])
        if tag in seen_tags:
            raise SystemExit(f"Duplicate survey question tag: {tag}")
        seen_tags.add(tag)
        question_type = question["type"]
        if question_type not in {"mc", "text", "descriptive"}:
            raise SystemExit(f"Unsupported question type for '{tag}': {question_type}")
        if question_type == "mc" and not question.get("choices"):
            raise SystemExit(f"Multiple-choice question '{tag}' needs choices.")

    data["spec_file"] = str(path)
    return data


def question_payload(question: dict[str, Any]) -> dict[str, Any]:
    force_response = "ON" if question.get("force_response") else "OFF"
    base = {
        "QuestionText": question["text"],
        "QuestionDescription": question["tag"],
        "DataExportTag": question["tag"],
        "Configuration": {"QuestionDescriptionOption": "SpecifyLabel"},
        "Validation": {
            "Settings": {
                "ForceResponse": force_response,
                "Type": "None",
            }
        },
    }

    if question["type"] == "text":
        return {**base, "QuestionType": "TE", "Selector": "SL"}

    if question["type"] == "descriptive":
        base.pop("Validation", None)
        return {**base, "QuestionType": "DB", "Selector": "TB"}

    choices = {
        str(index): {"Display": choice}
        for index, choice in enumerate(question["choices"], start=1)
    }
    return {
        **base,
        "QuestionType": "MC",
        "Selector": "SAVR",
        "SubSelector": "TX",
        "Choices": choices,
        "ChoiceOrder": list(choices.keys()),
        "RecodeValues": {choice_id: choice_id for choice_id in choices},
        "NextChoiceId": len(choices) + 1,
        "NextAnswerId": 1,
    }


def export_payload(export_format: str) -> dict[str, Any]:
    if export_format not in {"csv", "spss"}:
        raise SystemExit("Export format must be 'csv' or 'spss'.")
    return {
        "format": export_format,
        "compress": True,
        "useLabels": True,
        "breakoutSets": False,
    }


class QualtricsClient:
    def __init__(self) -> None:
        load_project_env()
        requests = load_requests()
        self.token = require_env("QUALTRICS_API_TOKEN")
        self.base_url = build_base_url(require_env("QUALTRICS_DATACENTER"))
        self.session = requests.Session()
        self.session.headers.update(
            {
                "X-API-TOKEN": self.token,
                "Accept": "application/json",
                "Content-Type": "application/json",
            }
        )

    def request(self, method: str, path: str, **kwargs: Any) -> dict[str, Any]:
        url = path if path.startswith("http") else f"{self.base_url}{path}"
        try:
            response = self.session.request(method, url, timeout=60, **kwargs)
        except Exception as exc:
            raise QualtricsApiError(method, path, sanitize_text(str(exc), self.token)) from exc

        if response.status_code >= 400:
            body = sanitize_text(response.text, self.token)
            raise QualtricsApiError(method, path, f"HTTP {response.status_code}: {body}")

        if not response.text.strip():
            return {"meta": {"httpStatus": str(response.status_code)}}

        try:
            return response.json()
        except ValueError as exc:
            body = sanitize_text(response.text, self.token)
            raise QualtricsApiError(method, path, f"Expected JSON response, got: {body}") from exc

    def download(self, path: str, destination: Path) -> None:
        url = f"{self.base_url}{path}"
        try:
            response = self.session.get(url, headers={"Accept": "application/octet-stream"}, timeout=180)
        except Exception as exc:
            raise QualtricsApiError("GET", path, sanitize_text(str(exc), self.token)) from exc

        if response.status_code >= 400:
            body = sanitize_text(response.text, self.token)
            raise QualtricsApiError("GET", path, f"HTTP {response.status_code}: {body}")

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(response.content)

    def list_surveys(self) -> list[dict[str, Any]]:
        surveys: list[dict[str, Any]] = []
        next_page: str | None = "/surveys"
        while next_page:
            data = self.request("GET", next_page)
            result = data.get("result", {})
            surveys.extend(result.get("elements", []))
            next_page = result.get("nextPage")
            if next_page and next_page.startswith(self.base_url):
                next_page = next_page.replace(self.base_url, "", 1)
        return surveys

    def first_survey_page(self) -> dict[str, Any]:
        return self.request("GET", "/surveys", params={"limit": 1})

    def create_survey(self, survey_name: str) -> dict[str, Any]:
        return self.request(
            "POST",
            "/survey-definitions",
            json={
                "SurveyName": survey_name,
                "Language": "EN",
                "ProjectCategory": "CORE",
            },
        )

    def create_question(
        self, survey_id_value: str, block_id: str | None, question: dict[str, Any]
    ) -> dict[str, Any]:
        params = {"blockId": block_id} if block_id else None
        return self.request(
            "POST",
            f"/survey-definitions/{survey_id_value}/questions",
            params=params,
            json=question_payload(question),
        )

    def add_end_survey_flow(self, survey_id_value: str, block_id: str) -> dict[str, Any]:
        flow = {
            "Type": "Root",
            "FlowID": "FL_1",
            "Flow": [
                {"Type": "Block", "ID": block_id, "FlowID": "FL_2", "Autofill": []},
                {"Type": "EndSurvey", "FlowID": "FL_3"},
            ],
            "Properties": {"Count": 3},
        }
        return self.request("PUT", f"/survey-definitions/{survey_id_value}/flow", json=flow)

    def publish_and_activate(self, survey_id_value: str) -> dict[str, Any]:
        attempts: list[dict[str, str]] = []
        result: dict[str, Any] = {"ok": False, "attempts": attempts}
        try:
            result["version"] = self.request(
                "POST",
                f"/survey-definitions/{survey_id_value}/versions",
                json={"Description": "Initial version from qualtrics_workflow.py", "Published": True},
            )
        except QualtricsApiError as exc:
            attempts.append({"step": "publish", "error": str(exc)})
        try:
            result["activation"] = self.request(
                "PUT",
                f"/survey-definitions/{survey_id_value}/metadata",
                json={"SurveyStatus": "Active"},
            )
        except QualtricsApiError as exc:
            attempts.append({"step": "activate", "error": str(exc)})
        result["ok"] = "version" in result and "activation" in result
        return result

    def start_response_export(self, survey_id_value: str, export_format: str) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/surveys/{survey_id_value}/export-responses",
            json=export_payload(export_format),
        )

    def export_progress(self, survey_id_value: str, progress_id: str) -> dict[str, Any]:
        return self.request("GET", f"/surveys/{survey_id_value}/export-responses/{progress_id}")

    def download_export_file(self, survey_id_value: str, file_id: str, destination: Path) -> None:
        self.download(f"/surveys/{survey_id_value}/export-responses/{file_id}/file", destination)

    def create_response(
        self,
        survey_id_value: str,
        values: dict[str, Any],
        idempotency_key: str,
    ) -> dict[str, Any]:
        return self.request(
            "POST",
            f"/surveys/{survey_id_value}/responses",
            json={"values": values},
            headers={"Idempotency-Key": idempotency_key},
        )


def survey_id(survey: dict[str, Any]) -> str:
    return str(survey.get("id") or survey.get("surveyId") or survey.get("SurveyID") or "")


def survey_name(survey: dict[str, Any]) -> str:
    return str(survey.get("name") or survey.get("surveyName") or survey.get("SurveyName") or "")


def find_survey_by_name(client: QualtricsClient, name: str) -> dict[str, Any]:
    matches = [survey for survey in client.list_surveys() if survey_name(survey) == name]
    if not matches:
        raise SystemExit(f"No Qualtrics survey found with exact name: {name}")
    if len(matches) > 1:
        raise SystemExit(f"Found more than one survey named '{name}'. Provide --survey-id locally to disambiguate.")
    return matches[0]


def resolve_survey_id(
    client: QualtricsClient,
    survey_key: str | None = None,
    survey_name_value: str | None = None,
    survey_id_value: str | None = None,
) -> str:
    if survey_id_value:
        return survey_id_value
    if survey_key:
        metadata = load_metadata(survey_key)
        if metadata.get("survey_id"):
            return str(metadata["survey_id"])
    if survey_name_value:
        selected = survey_id(find_survey_by_name(client, survey_name_value))
        if selected:
            return selected
    raise SystemExit("Provide --survey-id, a survey key with metadata, or --survey-name.")


def extract_question_id(value: Any) -> str:
    if isinstance(value, dict):
        for key in ("QuestionID", "QuestionId", "questionId", "id", "ID"):
            candidate = value.get(key)
            if isinstance(candidate, str) and candidate.startswith("QID"):
                return candidate
        for nested in value.values():
            candidate = extract_question_id(nested)
            if candidate:
                return candidate
    if isinstance(value, list):
        for nested in value:
            candidate = extract_question_id(nested)
            if candidate:
                return candidate
    if isinstance(value, str) and value.startswith("QID"):
        return value
    return ""


def question_ids_by_tag(metadata: dict[str, Any]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for question in metadata.get("questions", []):
        tag = str(question.get("tag", ""))
        question_id = extract_question_id(question.get("response"))
        if tag and question_id:
            mapping[tag] = question_id
    return mapping


def read_response_rows(input_csv: Path) -> list[dict[str, str]]:
    with input_csv.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def response_values_from_row(
    row: dict[str, str],
    survey_spec: dict[str, Any],
    qids_by_tag: dict[str, str],
    row_number: int,
) -> dict[str, Any]:
    start_date = datetime.now(timezone.utc) - timedelta(minutes=8, seconds=row_number)
    end_date = start_date + timedelta(minutes=3, seconds=row_number % 97)
    values: dict[str, Any] = {
        "distributionChannel": "api",
        "duration": int((end_date - start_date).total_seconds()),
        "endDate": end_date.isoformat().replace("+00:00", "Z"),
        "finished": 1,
        "progress": 100,
        "startDate": start_date.isoformat().replace("+00:00", "Z"),
        "userLanguage": "EN",
    }

    for question in survey_spec["questions"]:
        if question["type"] == "descriptive":
            continue
        tag = str(question["tag"])
        question_id = qids_by_tag.get(tag)
        if not question_id:
            raise SystemExit(f"No Qualtrics question ID found in metadata for tag: {tag}")
        answer = str(row.get(tag, "")).strip()
        if not answer:
            continue
        if question["type"] == "mc":
            choices = [str(choice) for choice in question["choices"]]
            try:
                values[question_id] = choices.index(answer) + 1
            except ValueError as exc:
                raise SystemExit(f"Row {row_number} has unsupported answer for {tag}: {answer}") from exc
        elif question["type"] == "text":
            values[question_id] = answer
    return values


def response_id_from_result(response: dict[str, Any]) -> str:
    result = response.get("result", response)
    for key in ("responseId", "ResponseID", "ResponseId", "id"):
        value = result.get(key) if isinstance(result, dict) else None
        if value:
            return str(value)
    return ""


def idempotency_key_for_response(survey_id_value: str, row_number: int, row: dict[str, str]) -> str:
    stable_row = json.dumps(row, sort_keys=True, ensure_ascii=True)
    return str(uuid.uuid5(uuid.NAMESPACE_URL, f"qualtrics:{survey_id_value}:{row_number}:{stable_row}"))


def synthetic_import_path(survey_key: str) -> Path:
    return DATA_DIR / safe_survey_key(survey_key) / "metadata" / "synthetic_response_import.json"


def next_resume_offset(survey_key: str) -> int:
    path = synthetic_import_path(survey_key)
    if not path.exists():
        return 0
    metadata = read_json(path)
    return int(metadata.get("offset", 0)) + int(metadata.get("submitted_count", 0))


def public_host_from_args(args: argparse.Namespace) -> str:
    load_project_env()
    public_host = (args.public_host or os.environ.get("QUALTRICS_PUBLIC_HOST") or "").strip()
    if public_host:
        return public_host.removeprefix("https://").removeprefix("http://").strip("/")
    datacenter = require_env("QUALTRICS_DATACENTER")
    return build_base_url(datacenter).removeprefix("https://").removesuffix("/API/v3")


def safe_extract(zip_path: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(zip_path) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            try:
                target.relative_to(root)
            except ValueError:
                raise SystemExit(f"Refusing to unzip unsafe path: {member.filename}")
        archive.extractall(destination)


def command_check_auth(_: argparse.Namespace) -> int:
    client = QualtricsClient()
    data = client.first_survey_page()
    result = data.get("result", {})
    elements = result.get("elements", [])
    print("Qualtrics authentication check succeeded.")
    print(f"First survey page reachable; visible surveys on that page: {len(elements)}.")
    print("No survey IDs, links, responses, or metadata were printed.")
    return 0


def command_list_surveys(args: argparse.Namespace) -> int:
    client = QualtricsClient()
    surveys = client.list_surveys()
    if not surveys:
        print("No surveys returned by the Qualtrics API.")
        return 0
    for survey in surveys:
        identifier = survey_id(survey) if args.show_private_ids else "[survey-id-hidden]"
        print(f"{identifier}\t{survey_name(survey)}")
    if not args.show_private_ids:
        print("Survey IDs hidden. Rerun with --show-private-ids only when you need IDs locally.")
    return 0


def command_create_survey(args: argparse.Namespace) -> int:
    survey_key = safe_survey_key(args.survey_key)
    survey_spec = load_survey_spec(args.spec_file)
    client = QualtricsClient()

    created = client.create_survey(args.survey_name)
    result = created.get("result", created)
    selected_survey_id = str(
        result.get("SurveyID") or result.get("surveyId") or result.get("id") or ""
    )
    if not selected_survey_id:
        raise SystemExit(f"Qualtrics did not return a survey ID: {redact_sensitive_text(created)}")
    default_block_id = str(
        result.get("DefaultBlockID") or result.get("defaultBlockId") or result.get("blockId") or ""
    )

    question_results = []
    for question in survey_spec["questions"]:
        response = client.create_question(selected_survey_id, default_block_id or None, question)
        q_result = response.get("result", response)
        question_results.append({"tag": question["tag"], "response": q_result})

    flow_result = None
    if default_block_id:
        flow_result = client.add_end_survey_flow(selected_survey_id, default_block_id)

    activation_result = None
    if args.activate:
        activation_result = client.publish_and_activate(selected_survey_id)

    metadata = {
        "survey_name": args.survey_name,
        "survey_key": survey_key,
        "survey_id": selected_survey_id,
        "default_block_id": default_block_id or None,
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "spec_file": survey_spec.get("spec_file"),
        "questions": question_results,
        "flow": flow_result.get("result", flow_result) if flow_result else None,
        "activation": activation_result,
    }
    info_path = save_metadata(survey_key, metadata)

    if args.show_private_ids:
        print(f"Created survey: {selected_survey_id}")
    else:
        print("Created survey. Survey ID was saved to ignored local metadata.")
    print(f"Wrote metadata: {info_path}")
    if args.activate:
        print("Activation was requested. Check metadata for publish/activation details.")
    else:
        print("Survey was created as a draft. Use --activate only when ready to collect responses.")
        print("Note: draft/inactive surveys may still accept API-created test responses. Treat API access as live.")
    return 0


def command_get_link(args: argparse.Namespace) -> int:
    survey_key = safe_survey_key(args.survey_key)
    client = QualtricsClient()
    selected_survey_id = resolve_survey_id(
        client,
        survey_key=survey_key,
        survey_name_value=args.survey_name,
        survey_id_value=args.survey_id,
    )
    public_host = public_host_from_args(args)
    reusable_link = f"https://{public_host}/jfe/form/{selected_survey_id}"

    metadata = load_metadata(survey_key)
    metadata.update(
        {
            "survey_key": survey_key,
            "survey_name": args.survey_name or metadata.get("survey_name"),
            "survey_id": selected_survey_id,
            "reusable_link": reusable_link,
            "reusable_link_type": "Qualtrics anonymous link / single reusable link",
            "reusable_link_saved_at": datetime.now().isoformat(timespec="seconds"),
        }
    )
    info_path = save_metadata(survey_key, metadata)
    if args.write_slide_inputs:
        tex_path, md_path = write_survey_link_slide_inputs(survey_key, reusable_link)
        print(f"Wrote private slide link inputs: {tex_path}, {md_path}")
    if args.show_private_link:
        print(f"Reusable link: {reusable_link}")
    else:
        print("Reusable link saved to ignored local metadata.")
    print(f"Wrote metadata: {info_path}")
    print("Keep reusable links and metadata private by default; do not commit or publish them.")
    return 0


def submit_response_batch(
    client: QualtricsClient,
    survey_id_value: str,
    survey_spec: dict[str, Any],
    qids_by_tag: dict[str, str],
    rows: list[dict[str, str]],
    offset: int,
    limit: int | None,
) -> tuple[list[str], int]:
    selected_rows = rows[offset:]
    if limit is not None:
        selected_rows = selected_rows[:limit]
    if not selected_rows:
        raise SystemExit("No response rows selected for submission.")

    response_ids: list[str] = []
    for local_index, row in enumerate(selected_rows, start=offset + 1):
        values = response_values_from_row(row, survey_spec, qids_by_tag, local_index)
        response = client.create_response(
            survey_id_value,
            values=values,
            idempotency_key=idempotency_key_for_response(survey_id_value, local_index, row),
        )
        response_id = response_id_from_result(response)
        if response_id:
            response_ids.append(response_id)
        print(f"Submitted response row {local_index}.")
    return response_ids, len(selected_rows)


def command_submit_synthetic_responses(args: argparse.Namespace) -> int:
    survey_key = safe_survey_key(args.survey_key)
    client = QualtricsClient()
    selected_survey_id = resolve_survey_id(
        client,
        survey_key=survey_key,
        survey_name_value=args.survey_name,
        survey_id_value=args.survey_id,
    )
    survey_spec = load_survey_spec(str(args.spec_file or default_spec_path(survey_key)))
    metadata = load_metadata(survey_key)
    qids_by_tag = question_ids_by_tag(metadata)
    if not qids_by_tag:
        raise SystemExit(
            "Could not find question IDs in saved survey metadata. "
            "Create the survey with this workflow before submitting synthetic responses."
        )

    input_csv = args.input
    if not input_csv.is_absolute():
        input_csv = PROJECT_ROOT / input_csv
    if not input_csv.exists():
        raise SystemExit(f"Input CSV not found: {input_csv}")

    rows = read_response_rows(input_csv)

    offset = args.offset
    if args.resume:
        if args.offset:
            raise SystemExit("Use either --resume or --offset, not both.")
        offset = next_resume_offset(survey_key)

    if args.smoke_then_rest and (args.limit is not None or offset != 0 or args.resume):
        raise SystemExit("--smoke-then-rest cannot be combined with --limit, --offset, or --resume.")

    response_ids: list[str] = []
    if args.smoke_then_rest:
        print("Submitting first synthetic response as the smoke row.")
        first_response_ids, first_count = submit_response_batch(
            client,
            selected_survey_id,
            survey_spec,
            qids_by_tag,
            rows,
            offset=0,
            limit=1,
        )
        response_ids.extend(first_response_ids)
        submitted_count = first_count
        if len(rows) > 1:
            print("Submitting remaining synthetic responses starting at offset 1.")
            remaining_response_ids, remaining_count = submit_response_batch(
                client,
                selected_survey_id,
                survey_spec,
                qids_by_tag,
                rows,
                offset=1,
                limit=None,
            )
            response_ids.extend(remaining_response_ids)
            submitted_count += remaining_count
        submitted_offset = 0
    else:
        response_ids, submitted_count = submit_response_batch(
            client,
            selected_survey_id,
            survey_spec,
            qids_by_tag,
            rows,
            offset=offset,
            limit=args.limit,
        )
        submitted_offset = offset

    import_path = synthetic_import_path(survey_key)
    import_metadata = {
        "survey_key": survey_key,
        "survey_id": selected_survey_id,
        "input_csv": str(input_csv),
        "offset": submitted_offset,
        "submitted_count": submitted_count,
        "submitted_at": datetime.now().isoformat(timespec="seconds"),
        "response_ids": response_ids,
    }
    write_json(import_path, import_metadata)
    print(f"Submitted synthetic responses: {submitted_count}")
    print(f"Wrote import metadata: {import_path}")
    print("Response IDs were saved only in ignored local metadata and were not printed.")
    return 0


def command_export_responses(args: argparse.Namespace) -> int:
    survey_key = safe_survey_key(args.survey_key)
    export_format = args.format
    client = QualtricsClient()
    selected_survey_id = resolve_survey_id(
        client,
        survey_key=survey_key,
        survey_name_value=args.survey_name,
        survey_id_value=args.survey_id,
    )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    raw_dir = DATA_DIR / survey_key / "raw" / timestamp
    zip_path = raw_dir / f"{timestamp}_{survey_key}_{export_format}.zip"

    start = client.start_response_export(selected_survey_id, export_format)
    progress_id = start.get("result", {}).get("progressId")
    if not progress_id:
        raise SystemExit(f"Qualtrics did not return an export progressId: {redact_sensitive_text(start)}")

    print(f"Started {export_format.upper()} export for the selected survey.")
    final_progress: dict[str, Any] | None = None
    for _ in range(60):
        time.sleep(2)
        progress_response = client.export_progress(selected_survey_id, progress_id)
        result = progress_response.get("result", {})
        status = str(result.get("status", "")).lower()
        percent = result.get("percentComplete")
        if percent is not None:
            print(f"Export status: {status} ({percent}%).")
        else:
            print(f"Export status: {status}.")
        if status == "complete":
            final_progress = progress_response
            break
        if status == "failed":
            raise SystemExit(f"Qualtrics export failed: {redact_sensitive_text(progress_response)}")

    if final_progress is None:
        raise SystemExit("Timed out while waiting for the Qualtrics response export.")

    file_id = final_progress.get("result", {}).get("fileId")
    if not file_id:
        raise SystemExit(f"Completed export did not include a fileId: {redact_sensitive_text(final_progress)}")

    client.download_export_file(selected_survey_id, file_id, zip_path)
    safe_extract(zip_path, raw_dir)

    suffix = ".sav" if export_format == "spss" else ".csv"
    exported_files = sorted(path for path in raw_dir.rglob("*") if path.suffix.lower() == suffix)
    metadata = {
        "survey_key": survey_key,
        "survey_id": selected_survey_id,
        "timestamp": timestamp,
        "format": export_format,
        "progress_id": progress_id,
        "file_id": file_id,
        "zip_file": str(zip_path),
        "raw_dir": str(raw_dir),
        "exported_files": [str(path) for path in exported_files],
    }
    write_json(raw_dir / "export_metadata.json", metadata)
    if not exported_files:
        raise SystemExit(f"Export downloaded, but no {suffix} file was found in {raw_dir}.")

    print(f"Downloaded ZIP: {zip_path}")
    print(f"Unzipped raw files: {raw_dir}")
    print(f"Response file: {exported_files[0]}")
    if export_format == "csv":
        print("Note: Qualtrics CSV exports may include metadata rows after the header; analysis scripts should filter real ResponseId values that start with R_.")
    return 0


def command_export_spss(args: argparse.Namespace) -> int:
    args.format = "spss"
    return command_export_responses(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Qualtrics workflow helper.")
    subparsers = parser.add_subparsers(dest="command")

    auth_parser = subparsers.add_parser("check-auth", help="Run a lightweight read-only API authentication check.")
    auth_parser.set_defaults(func=command_check_auth)

    list_parser = subparsers.add_parser("list-surveys", help="List surveys visible to the API token.")
    list_parser.add_argument("--show-private-ids", action="store_true", help="Print survey IDs in local terminal output.")
    list_parser.set_defaults(func=command_list_surveys)

    create_parser = subparsers.add_parser("create-survey", help="Create a Qualtrics survey.")
    create_parser.add_argument("--survey-name", required=True)
    create_parser.add_argument("--survey-key", required=True)
    create_parser.add_argument("--spec-file")
    create_parser.add_argument("--activate", action="store_true", help="Publish and activate after creation.")
    create_parser.add_argument("--show-private-ids", action="store_true", help="Print survey IDs in local terminal output.")
    create_parser.set_defaults(func=command_create_survey)

    link_parser = subparsers.add_parser("get-link", help="Save a reusable survey link to ignored local metadata.")
    link_parser.add_argument("--survey-key", required=True)
    link_parser.add_argument("--survey-name")
    link_parser.add_argument("--survey-id")
    link_parser.add_argument("--public-host", help="Respondent-facing host, e.g. yourbrand.qualtrics.com.")
    link_parser.add_argument("--show-private-link", action="store_true", help="Print the reusable link in local terminal output.")
    link_parser.add_argument(
        "--write-slide-inputs",
        action="store_true",
        help="Write ignored local slide inputs so decks can include the reusable link without printing it.",
    )
    link_parser.set_defaults(func=command_get_link)

    for command_name, help_text in [
        ("submit-synthetic-responses", "Submit local synthetic CSV rows as Qualtrics survey responses."),
        ("submit-responses", "Compatibility alias for submit-synthetic-responses."),
    ]:
        submit_parser = subparsers.add_parser(command_name, help=help_text)
        submit_parser.add_argument("--survey-key", required=True)
        submit_parser.add_argument("--input", type=Path, required=True)
        submit_parser.add_argument("--survey-name")
        submit_parser.add_argument("--survey-id")
        submit_parser.add_argument("--spec-file", type=Path)
        submit_parser.add_argument("--offset", type=int, default=0, help="Zero-based number of rows to skip.")
        submit_parser.add_argument("--limit", type=int, help="Maximum number of rows to submit.")
        submit_parser.add_argument("--resume", action="store_true", help="Continue after the last saved synthetic import offset.")
        submit_parser.add_argument("--smoke-then-rest", action="store_true", help="Submit row 1, then submit all remaining rows without duplicating row 1.")
        submit_parser.set_defaults(func=command_submit_synthetic_responses)

    export_parser = subparsers.add_parser("export-responses", help="Export survey responses.")
    export_parser.add_argument("--survey-key", required=True)
    export_parser.add_argument("--survey-name")
    export_parser.add_argument("--survey-id")
    export_parser.add_argument("--format", choices=["csv", "spss"], default="csv")
    export_parser.set_defaults(func=command_export_responses)

    export_spss_parser = subparsers.add_parser(
        "export-spss",
        help="Compatibility alias for: export-responses --format spss.",
    )
    export_spss_parser.add_argument("--survey-key", required=True)
    export_spss_parser.add_argument("--survey-name")
    export_spss_parser.add_argument("--survey-id")
    export_spss_parser.set_defaults(func=command_export_spss)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 0
    try:
        return int(args.func(args))
    except QualtricsApiError as exc:
        raise SystemExit(str(exc)) from None


if __name__ == "__main__":
    sys.exit(main())
