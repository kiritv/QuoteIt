#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path


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


def restore_file(source: Path, destination: Path, dry_run: bool, overwrite: bool) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and not overwrite:
        raise FileExistsError(f"Destination exists: {destination} (use --overwrite)")
    if dry_run:
        print(f"[DRY-RUN] copy {source} -> {destination}")
        return
    shutil.copy2(source, destination)
    print(f"[OK] copied {source} -> {destination}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Restore one dataset from Datasets/ archive into app bundle Data/ for validation/testing."
    )
    parser.add_argument("--source-id", required=True, help="Source ID to restore (e.g. rumiMasnavi)")
    parser.add_argument("--dry-run", action="store_true", help="Print planned actions only")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing files in app Data/")
    parser.add_argument(
        "--delete-from-archive",
        action="store_true",
        help="After successful restore, delete restored files from Datasets/ archive",
    )
    args = parser.parse_args()

    source_id = args.source_id.strip()
    if not source_id:
        print("source-id cannot be empty")
        return 1

    repo_root = resolve_repo_root()
    archive_root = repo_root / "Datasets"
    app_data_root = repo_root / "QuoteIt" / "Data"
    archive_sources = archive_root / "Sources"
    archive_collections = archive_root / "Collections"

    manifest_path = archive_sources / f"{source_id}.manifest.json"
    if not manifest_path.exists():
        candidates = sorted(archive_sources.glob("*.manifest.json"))
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
            print(f"Archived manifest not found for sourceId '{source_id}' in {archive_sources}")
            return 1
        manifest_path = found

    manifest = load_json(manifest_path)
    data_path = str(manifest.get("dataPath", "")).strip()
    supplemental_path = str(manifest.get("supplementalDataPath", "")).strip()
    if not data_path:
        print(f"Manifest missing dataPath: {manifest_path}")
        return 1

    collection_file = Path(data_path).name
    archive_collection = archive_collections / collection_file
    if not archive_collection.exists():
        print(f"Archived collection not found: {archive_collection}")
        return 1

    files: list[tuple[Path, Path]] = []
    files.append((manifest_path, app_data_root / "Sources" / manifest_path.name))
    files.append((archive_collection, app_data_root / "Collections" / archive_collection.name))

    if supplemental_path:
        supplemental_file = Path(supplemental_path).name
        archive_supplemental = archive_collections / supplemental_file
        if not archive_supplemental.exists():
            print(f"Archived supplemental collection not found: {archive_supplemental}")
            return 1
        files.append((archive_supplemental, app_data_root / "Collections" / archive_supplemental.name))

    print(f"Restoring sourceId '{source_id}' from {archive_root} into {app_data_root}")
    for src, dst in files:
        try:
            restore_file(src, dst, dry_run=args.dry_run, overwrite=args.overwrite)
        except FileExistsError as exc:
            print(str(exc))
            return 1

    if args.delete_from_archive:
        if args.dry_run:
            for src, _ in files:
                print(f"[DRY-RUN] delete archive file {src}")
        else:
            for src, _ in files:
                src.unlink(missing_ok=True)
                print(f"[OK] deleted archive file {src}")

    print("Restore complete.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

