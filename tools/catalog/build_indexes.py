#!/usr/bin/env python3
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

DISALLOWED_ONLINE_SOURCE_IDS = {"standardQuotes"}


def resolve_repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    candidate = base / "QuoteIt"
    if (candidate / "Datasets").exists():
        return candidate
    return base


def resolve_workspace_root(repo_root: Path) -> Path:
    if repo_root.name == "QuoteIt":
        return repo_root.parent
    return repo_root


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        f.write("\n")


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def compute_inputs_hash(datasets_root: Path) -> str:
    tracked_files: List[Path] = []
    for subdir in ("Sources", "Packs", "Programs", "Collections"):
        tracked_files.extend(iter_json_files(datasets_root / subdir))
    tracked_files = sorted(set(tracked_files))

    digest = hashlib.sha256()
    for path in tracked_files:
        rel = path.relative_to(datasets_root).as_posix()
        digest.update(rel.encode("utf-8"))
        digest.update(b"\0")
        digest.update(file_sha256(path).encode("ascii"))
        digest.update(b"\0")
    return digest.hexdigest()


def resolve_build_timestamp(output_root: Path, input_hash: str) -> str:
    state_path = output_root / ".build_state.json"
    if state_path.exists():
        try:
            state = load_json(state_path)
            if (
                isinstance(state, dict)
                and state.get("inputHash") == input_hash
                and isinstance(state.get("generatedAt"), str)
                and state["generatedAt"].strip()
            ):
                return state["generatedAt"]
        except Exception:
            pass

    generated_at = now_utc()
    write_json(state_path, {"inputHash": input_hash, "generatedAt": generated_at})
    return generated_at


def to_int(value: Any, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def iter_manifest_files(sources_root: Path) -> List[Path]:
    if not sources_root.exists():
        return []
    return sorted(
        p for p in sources_root.rglob("*.manifest.json")
        if p.is_file() and not p.name.startswith(".")
    )


def iter_json_files(root: Path) -> List[Path]:
    if not root.exists():
        return []
    return sorted(
        p for p in root.rglob("*.json")
        if p.is_file() and not p.name.startswith(".")
    )


def manifest_language_code(manifest: dict) -> str:
    code = str(manifest.get("languageCode", "")).strip().lower()
    return code or "en"


def package_url(source_id: str, language_code: str) -> str:
    return (
        "https://raw.githubusercontent.com/kiritv/QuoteIt/main/"
        f"Datasets/packages/{language_code}/{source_id}.quoteit"
    )


def build_dataset_indexes(repo_root: Path, output_root: Path, build_ts: str) -> Dict[str, Dict[str, Any]]:
    datasets_root = repo_root / "Datasets"
    metadata_root = output_root / "metadata"
    indexes_root = output_root / "indexes"
    manifest_files = iter_manifest_files(datasets_root / "Sources")

    by_lang: Dict[str, List[dict]] = {}
    source_lookup: Dict[str, Dict[str, Any]] = {}

    for manifest_path in manifest_files:
        manifest = load_json(manifest_path)
        if not isinstance(manifest, dict):
            continue
        source_id = str(manifest.get("sourceId", "")).strip()
        if not source_id or source_id in DISALLOWED_ONLINE_SOURCE_IDS:
            continue
        lang = manifest_language_code(manifest)
        item = {
            "sourceId": source_id,
            "displayName": manifest.get("displayName", source_id),
            "version": manifest.get("version", "1.0"),
            "languageCode": lang,
            "displayNameEnglish": manifest.get("displayNameEnglish"),
            "script": manifest.get("script"),
            "isRTL": bool(manifest.get("isRTL", False)),
            "transliterationAvailable": bool(manifest.get("transliterationAvailable", False)),
            "contentRating": manifest.get("contentRating"),
            "language": manifest.get("language"),
            "edition": manifest.get("edition"),
            "primaryCategory": manifest.get("primaryCategory"),
            "subcategory": manifest.get("subcategory"),
            "audienceTags": manifest.get("audienceTags") or [],
            "itemCount": to_int(manifest.get("itemCount"), 0),
            "supportsRandom": bool(manifest.get("supportsRandom", True)),
            "supportsBrowse": bool(manifest.get("supportsBrowse", True)),
            "browseOrder": manifest.get("browseOrder", "random"),
            "packageUrl": package_url(source_id, lang),
            "isFeatured": bool(manifest.get("isFeatured", False)),
            "priority": to_int(manifest.get("priority"), 9999),
            "generatedAt": build_ts,
        }
        by_lang.setdefault(lang, []).append(item)
        source_lookup[source_id] = item

    for lang, items in by_lang.items():
        items.sort(key=lambda x: (to_int(x.get("priority"), 9999), str(x.get("displayName", "")).lower()))
        for item in items:
            write_json(metadata_root / lang / f"{item['sourceId']}.json", item)
        write_json(indexes_root / f"datasets-{lang}.json", {
            "kind": "datasets",
            "language": lang,
            "count": len(items),
            "generatedAt": build_ts,
            "items": items,
        })

    return source_lookup


def build_pack_indexes(repo_root: Path, source_lookup: Dict[str, Dict[str, Any]], output_root: Path, build_ts: str) -> None:
    datasets_root = repo_root / "Datasets"
    packs_root = datasets_root / "Packs"
    online_packs_root = output_root / "packs"
    indexes_root = output_root / "indexes"

    files = [p for p in iter_json_files(packs_root) if p.name != "packs.index.json"]
    by_lang: Dict[str, List[dict]] = {}
    for path in files:
        obj = load_json(path)
        if not isinstance(obj, dict):
            continue
        source_ids = [str(s).strip() for s in obj.get("sourceIds", []) if str(s).strip()]
        estimated_count = sum(to_int(source_lookup.get(s, {}).get("itemCount"), 0) for s in source_ids)
        scopes = obj.get("languageScope", [])
        if not isinstance(scopes, list) or not scopes:
            scopes = ["en"]

        for raw_lang in scopes:
            lang = str(raw_lang).strip().lower()
            if not lang:
                continue
            item = {
                "packId": obj.get("packId", path.stem),
                "displayName": obj.get("displayName", path.stem),
                "languageCode": lang,
                "audience": obj.get("audience", ""),
                "objective": obj.get("objective", ""),
                "sourceIds": source_ids,
                "estimatedItemCount": estimated_count,
                "isFeatured": bool(obj.get("isFeatured", False)),
                "priority": to_int(obj.get("priority"), 9999),
            }
            by_lang.setdefault(lang, []).append(item)

    for lang, items in by_lang.items():
        items.sort(key=lambda x: (to_int(x.get("priority"), 9999), str(x.get("displayName", "")).lower()))
        write_json(online_packs_root / lang / "index.json", {
            "kind": "packs",
            "language": lang,
            "count": len(items),
            "generatedAt": build_ts,
            "items": items,
        })
        write_json(indexes_root / f"packs-{lang}.json", {
            "kind": "packs",
            "language": lang,
            "count": len(items),
            "generatedAt": build_ts,
            "items": items,
        })


def build_program_indexes(repo_root: Path, output_root: Path, build_ts: str) -> None:
    datasets_root = repo_root / "Datasets"
    programs_root = datasets_root / "Programs"
    online_programs_root = output_root / "programs"
    indexes_root = output_root / "indexes"

    files = iter_json_files(programs_root)
    by_lang: Dict[str, List[dict]] = {}
    for path in files:
        obj = load_json(path)
        if not isinstance(obj, dict):
            continue
        lang = str(obj.get("languageCode", "")).strip().lower() or "en"
        required_source_ids = [str(s).strip() for s in obj.get("requiredSourceIds", []) if str(s).strip()]
        item = {
            "programId": obj.get("programId", path.stem),
            "displayName": obj.get("title") or obj.get("displayName") or path.stem.replace("-", " ").title(),
            "languageCode": lang,
            "requiredSourceIds": required_source_ids,
            "dayCount": to_int(obj.get("dayCount") or obj.get("durationDays"), 0),
            "isFeatured": bool(obj.get("isFeatured", False)),
            "priority": to_int(obj.get("priority"), 9999),
            "relativePath": f"Datasets/Programs/{path.name}",
        }
        by_lang.setdefault(lang, []).append(item)

    for lang, items in by_lang.items():
        items.sort(key=lambda x: (to_int(x.get("priority"), 9999), str(x.get("displayName", "")).lower()))
        write_json(online_programs_root / lang / "index.json", {
            "kind": "programs",
            "language": lang,
            "count": len(items),
            "generatedAt": build_ts,
            "items": items,
        })
        write_json(indexes_root / f"programs-{lang}.json", {
            "kind": "programs",
            "language": lang,
            "count": len(items),
            "generatedAt": build_ts,
            "items": items,
        })


def build_index_manifest(indexes_root: Path, build_ts: str) -> None:
    files = sorted(
        p.name for p in indexes_root.glob("*.json")
        if p.name not in {"index-manifest.json", "signing-manifest.json"}
    )
    grouped = {"datasets": [], "packs": [], "programs": []}
    for name in files:
        if name.startswith("datasets-"):
            grouped["datasets"].append(name)
        elif name.startswith("packs-"):
            grouped["packs"].append(name)
        elif name.startswith("programs-"):
            grouped["programs"].append(name)
    write_json(indexes_root / "index-manifest.json", {
        "formatVersion": 1,
        "generatedAt": build_ts,
        "files": grouped,
    })


def main() -> int:
    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)
    datasets_root = repo_root / "Datasets"
    output_root = workspace_root / "tools" / "catalog" / "output"
    indexes_root = output_root / "indexes"
    if not datasets_root.exists():
        print(f"Datasets root not found: {datasets_root}")
        return 1

    input_hash = compute_inputs_hash(datasets_root)
    build_ts = resolve_build_timestamp(output_root, input_hash)
    source_lookup = build_dataset_indexes(repo_root, output_root, build_ts)
    build_pack_indexes(repo_root, source_lookup, output_root, build_ts)
    build_program_indexes(repo_root, output_root, build_ts)
    build_index_manifest(indexes_root, build_ts)
    print(f"Catalog output generated at: {output_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
