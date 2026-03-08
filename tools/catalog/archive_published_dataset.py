#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

PROTECTED_BUNDLED_SOURCE_IDS = {"standardQuotes"}


def resolve_repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    candidate = base / "QuoteIt"
    if (candidate / "QuoteIt" / "Data").exists():
        return candidate
    return base


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return payload


def copy_then_delete(source: Path, destination: Path, dry_run: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if dry_run:
        print(f"[DRY-RUN] move {source} -> {destination}")
        return
    shutil.copy2(source, destination)
    source.unlink()
    print(f"[OK] moved {source} -> {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Move a published dataset out of app bundle into Datasets/ with same subfolder names."
    )
    parser.add_argument("--source-id", required=True, help="Source ID to archive (e.g. rumiMasnavi)")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions only")
    args = parser.parse_args()

    source_id = args.source_id.strip()
    if not source_id:
        print("source-id cannot be empty")
        return 1
    if source_id in PROTECTED_BUNDLED_SOURCE_IDS:
        print(
            f"Refusing to archive '{source_id}': this dataset is protected and must stay bundled in app."
        )
        return 1

    repo_root = resolve_repo_root()
    app_data_root = repo_root / "QuoteIt" / "Data"
    sources_root = app_data_root / "Sources"

    manifest_path = sources_root / f"{source_id}.manifest.json"
    if not manifest_path.exists():
        # Fallback: search by sourceId inside manifest files.
        candidates = sorted(sources_root.glob("*.manifest.json"))
        found = None
        for path in candidates:
            try:
                payload = load_json(path)
            except Exception:
                continue
            if str(payload.get("sourceId", "")).strip() == source_id:
                found = path
                break
        if found is None:
            print(f"Manifest not found for sourceId '{source_id}' in {sources_root}")
            return 1
        manifest_path = found

    manifest = load_json(manifest_path)
    data_raw = manifest.get("dataPath")
    supplemental_raw = manifest.get("supplementalDataPath")
    data_rel = str(data_raw).strip() if isinstance(data_raw, str) else ""
    supplemental_rel = str(supplemental_raw).strip() if isinstance(supplemental_raw, str) else ""
    if not data_rel:
        print(f"Manifest missing dataPath: {manifest_path}")
        return 1

    files_to_move = [repo_root / "QuoteIt" / data_rel, manifest_path]
    if supplemental_rel:
        files_to_move.append(repo_root / "QuoteIt" / supplemental_rel)

    missing = [str(p) for p in files_to_move if not p.exists()]
    if missing:
        print("Cannot archive; missing files:")
        for item in missing:
            print(f"- {item}")
        return 1

    destination_root = repo_root / "Datasets"
    print(f"Moving sourceId '{source_id}' into {destination_root}")
    for src in files_to_move:
        rel = src.relative_to(app_data_root)
        dst = destination_root / rel
        if dst.exists() and not args.dry_run:
            print(f"Cannot move: destination already exists: {dst}")
            return 1
        copy_then_delete(src, dst, args.dry_run)

    print(
        "Done. Dataset is removed from app bundle paths and preserved in Datasets/."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
