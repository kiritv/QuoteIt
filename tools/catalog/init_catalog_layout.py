#!/usr/bin/env python3
import argparse
from pathlib import Path

DEFAULT_LANGS = ["en", "hi", "ar", "es", "pt", "tr", "id", "ur", "ja", "fr", "de"]


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


def main() -> int:
    parser = argparse.ArgumentParser(description="Initialize Datasets catalog folder layout")
    parser.add_argument("--langs", nargs="*", default=DEFAULT_LANGS, help="language folder codes")
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)
    datasets = repo_root / "Datasets"
    output_root = workspace_root / "tools" / "catalog" / "output"

    # Canonical local (mirrors app Data subfolders for simplicity).
    for root in ["Collections", "Sources", "Packs", "Programs"]:
        (datasets / root).mkdir(parents=True, exist_ok=True)

    # Generated publish artifacts (tool output, not canonical datasets).
    (output_root / "indexes").mkdir(parents=True, exist_ok=True)
    for root in ["metadata", "packages", "packs", "programs"]:
        for lang in args.langs:
            (output_root / root / lang).mkdir(parents=True, exist_ok=True)

    readme = datasets / "README.md"
    if not readme.exists():
        readme.write_text(
            "# Datasets Workspace\n\n"
            "Canonical local dataset files archived outside the app bundle.\n",
            encoding="utf-8",
        )

    for keep in [
        datasets / "Collections" / ".gitkeep",
        datasets / "Sources" / ".gitkeep",
        datasets / "Packs" / ".gitkeep",
        datasets / "Programs" / ".gitkeep",
        output_root / "indexes" / ".gitkeep",
        output_root / "metadata" / ".gitkeep",
        output_root / "packages" / ".gitkeep",
        output_root / "packs" / ".gitkeep",
        output_root / "programs" / ".gitkeep",
    ]:
        keep.touch(exist_ok=True)

    print(f"Initialized canonical datasets at: {datasets}")
    print(f"Initialized generated catalog output at: {output_root}")
    print(f"Languages: {', '.join(args.langs)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
