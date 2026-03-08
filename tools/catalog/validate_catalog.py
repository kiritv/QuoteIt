#!/usr/bin/env python3
import json
import sys
from pathlib import Path
from typing import Dict, List, Set

DISALLOWED_ONLINE_SOURCE_IDS = {"standardQuotes"}
REQUIRED_MANIFEST_KEYS = {"sourceId", "displayName", "version", "dataPath"}
REQUIRED_PACK_KEYS = {"packId", "displayName", "objective", "sourceIds"}
# Non-English manifests (languageCode set and not "en") must declare these fields
# so the app can render them correctly (RTL, font selection, search normalization).
REQUIRED_MULTILINGUAL_KEYS = {"script", "isRTL", "displayNameEnglish"}


def resolve_repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    candidate = base / "QuoteIt"
    if (candidate / "Datasets").exists():
        return candidate
    return base


def load_json(path: Path):
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as exc:
        raise ValueError(f"{path}: invalid JSON ({exc})")


def iter_files(root: Path, suffixes: Set[str]) -> List[Path]:
    if not root.exists():
        return []
    return sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in suffixes and not p.name.startswith(".")
    )


def language_code_for_manifest(obj: dict) -> str:
    raw = str(obj.get("languageCode", "")).strip().lower()
    return raw or "en"


def validate_sources(datasets_root: Path, errors: List[str]) -> Dict[str, dict]:
    sources_root = datasets_root / "Sources"
    collections_root = datasets_root / "Collections"
    manifests = iter_files(sources_root, {".json"})
    source_map: Dict[str, dict] = {}

    if not manifests:
        print(f"[WARN] No source manifests found in {sources_root}")
        return source_map

    for path in manifests:
        if not path.name.endswith(".manifest.json"):
            continue
        try:
            obj = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue

        if not isinstance(obj, dict):
            errors.append(f"{path}: manifest must be a JSON object")
            continue

        missing = REQUIRED_MANIFEST_KEYS - set(obj.keys())
        if missing:
            errors.append(f"{path}: missing required keys: {sorted(missing)}")

        source_id = str(obj.get("sourceId", "")).strip()
        if not source_id:
            errors.append(f"{path}: sourceId is empty")
            continue
        if source_id in DISALLOWED_ONLINE_SOURCE_IDS:
            errors.append(
                f"{path}: sourceId '{source_id}' is app-bundled only and must not be published online"
            )
        if source_id in source_map:
            errors.append(f"{path}: duplicate sourceId '{source_id}' in Sources")
            continue

        data_path = str(obj.get("dataPath", "")).strip()
        data_name = Path(data_path).name
        if not data_name:
            errors.append(f"{path}: invalid dataPath '{data_path}'")
        else:
            expected_collection = collections_root / data_name
            if not expected_collection.exists():
                errors.append(
                    f"{path}: data file not found in Datasets/Collections: {expected_collection}"
                )

        supplemental = obj.get("supplementalDataPath")
        if isinstance(supplemental, str) and supplemental.strip():
            supplemental_name = Path(supplemental).name
            expected_supplemental = collections_root / supplemental_name
            if not expected_supplemental.exists():
                errors.append(
                    f"{path}: supplemental file not found in Datasets/Collections: {expected_supplemental}"
                )

        # Multilingual manifests (languageCode set and not "en") must declare
        # script, isRTL, and displayNameEnglish so the app can render them correctly.
        lang_code = language_code_for_manifest(obj)
        if lang_code and lang_code != "en":
            missing_ml = REQUIRED_MULTILINGUAL_KEYS - set(obj.keys())
            if missing_ml:
                errors.append(
                    f"{path}: multilingual manifest (languageCode='{lang_code}') "
                    f"is missing required fields: {sorted(missing_ml)}"
                )
            if "isRTL" in obj and not isinstance(obj["isRTL"], bool):
                errors.append(f"{path}: isRTL must be a boolean (true/false), got {obj['isRTL']!r}")

        source_map[source_id] = obj

    return source_map


def validate_packs(datasets_root: Path, source_ids: Set[str], errors: List[str]) -> None:
    packs_root = datasets_root / "Packs"
    files = iter_files(packs_root, {".json"})
    seen: Set[str] = set()
    for path in files:
        try:
            obj = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(obj, dict):
            errors.append(f"{path}: pack must be a JSON object")
            continue
        if path.name == "packs.index.json":
            continue

        missing = REQUIRED_PACK_KEYS - set(obj.keys())
        if missing:
            errors.append(f"{path}: missing required keys: {sorted(missing)}")

        pack_id = str(obj.get("packId", "")).strip()
        if not pack_id:
            errors.append(f"{path}: packId is empty")
        elif pack_id in seen:
            errors.append(f"{path}: duplicate packId '{pack_id}'")
        else:
            seen.add(pack_id)

        source_list = obj.get("sourceIds", [])
        if not isinstance(source_list, list) or not source_list:
            errors.append(f"{path}: sourceIds must be a non-empty array")
            continue
        for sid in source_list:
            s = str(sid).strip()
            if s not in source_ids:
                errors.append(f"{path}: unknown sourceId '{s}' (missing in Datasets/Sources)")


def validate_programs(datasets_root: Path, source_ids: Set[str], errors: List[str]) -> None:
    programs_root = datasets_root / "Programs"
    files = iter_files(programs_root, {".json", ".quoteitprogram"})
    for path in files:
        try:
            obj = load_json(path)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if not isinstance(obj, dict):
            errors.append(f"{path}: program must be a JSON object")
            continue

        required = obj.get("requiredSourceIds", [])
        if required and not isinstance(required, list):
            errors.append(f"{path}: requiredSourceIds must be an array")
            continue
        if isinstance(required, list):
            for sid in required:
                s = str(sid).strip()
                if s and s not in source_ids:
                    errors.append(f"{path}: unknown requiredSourceId '{s}'")

        days = obj.get("days", [])
        if isinstance(days, list):
            for day in days:
                if not isinstance(day, dict):
                    continue
                s = str(day.get("sourceId", "")).strip()
                if s and s not in source_ids:
                    errors.append(f"{path}: day.sourceId '{s}' not found in Datasets/Sources")


def main() -> int:
    repo_root = resolve_repo_root()
    datasets_root = repo_root / "Datasets"
    errors: List[str] = []

    source_map = validate_sources(datasets_root, errors)
    source_ids = set(source_map.keys())
    validate_packs(datasets_root, source_ids, errors)
    validate_programs(datasets_root, source_ids, errors)

    if errors:
        print("Catalog validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    language_counts: Dict[str, int] = {}
    for obj in source_map.values():
        code = language_code_for_manifest(obj)
        language_counts[code] = language_counts.get(code, 0) + 1

    print("Catalog validation passed.")
    print(f"Datasets root: {datasets_root}")
    print(f"Source IDs: {len(source_ids)}")
    if language_counts:
        print(f"Language coverage: {language_counts}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
