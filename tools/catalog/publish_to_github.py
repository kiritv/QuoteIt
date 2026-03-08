#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path
from typing import Iterable

SYNC_DIRS = ("metadata", "packages", "packs", "programs", "indexes")


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


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            chunk = handle.read(1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def iter_files(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.rglob("*") if p.is_file())


def remove_empty_dirs(root: Path, dry_run: bool) -> int:
    if not root.exists():
        return 0
    removed = 0
    for path in sorted((p for p in root.rglob("*") if p.is_dir()), key=lambda p: len(p.parts), reverse=True):
        if any(path.iterdir()):
            continue
        if dry_run:
            print(f"[DRY-RUN] rmdir {path}")
        else:
            path.rmdir()
        removed += 1
    return removed


def sync_tree(source: Path, target: Path, dry_run: bool) -> tuple[int, int, int]:
    copied = 0
    updated = 0
    deleted = 0

    source_files = {p.relative_to(source): p for p in iter_files(source)}
    target_files = {p.relative_to(target): p for p in iter_files(target)} if target.exists() else {}

    for rel_path, src in source_files.items():
        dest = target / rel_path
        if rel_path not in target_files:
            if dry_run:
                print(f"[DRY-RUN] copy {src} -> {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            copied += 1
            continue

        existing = target_files[rel_path]
        if file_hash(src) != file_hash(existing):
            if dry_run:
                print(f"[DRY-RUN] update {src} -> {dest}")
            else:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
            updated += 1

    for rel_path, existing in target_files.items():
        if rel_path in source_files:
            continue
        if dry_run:
            print(f"[DRY-RUN] delete {existing}")
        else:
            existing.unlink()
        deleted += 1

    deleted += remove_empty_dirs(target, dry_run=dry_run)
    return copied, updated, deleted


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync generated catalog output into repo Datasets/* for GitHub publish"
    )
    parser.add_argument(
        "--output-root",
        default="tools/catalog/output",
        help="Generated artifacts root (default: tools/catalog/output)",
    )
    parser.add_argument(
        "--target-root",
        default="Datasets",
        help="Repo target root for publish artifacts (default: Datasets)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview copy/update/delete operations without writing",
    )
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)

    output_root = Path(args.output_root)
    if not output_root.is_absolute():
        output_root = (workspace_root / output_root).resolve()
    target_root = Path(args.target_root)
    if not target_root.is_absolute():
        target_root = (repo_root / target_root).resolve()

    if not output_root.exists():
        print(f"Output root does not exist: {output_root}")
        return 1
    target_root.mkdir(parents=True, exist_ok=True)

    total_copied = 0
    total_updated = 0
    total_deleted = 0

    for folder in SYNC_DIRS:
        source_dir = output_root / folder
        target_dir = target_root / folder
        if not source_dir.exists():
            print(f"[WARN] Missing source folder, skipping: {source_dir}")
            continue
        copied, updated, deleted = sync_tree(source_dir, target_dir, dry_run=args.dry_run)
        total_copied += copied
        total_updated += updated
        total_deleted += deleted

    mode = "DRY-RUN" if args.dry_run else "APPLY"
    print(f"[{mode}] Sync complete")
    print(f"Output root: {output_root}")
    print(f"Target root: {target_root}")
    print(f"Copied: {total_copied}, Updated: {total_updated}, Deleted: {total_deleted}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

