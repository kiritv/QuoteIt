#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
import subprocess
import sys
import shutil
from pathlib import Path


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


def run(cmd: list[str], cwd: Path, capture: bool = False) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=str(cwd),
        check=True,
        text=True,
        capture_output=capture,
    )


def load_token(token_env: str, token_file: Path) -> str:
    token = os.environ.get(token_env, "").strip()
    if token:
        return token
    if token_file.exists():
        value = token_file.read_text(encoding="utf-8").strip()
        if value:
            return value
    raise ValueError(f"Missing GitHub token. Set {token_env} or create {token_file}.")


def has_staged_changes(repo_root: Path) -> bool:
    result = run(["git", "diff", "--cached", "--name-only"], cwd=repo_root, capture=True)
    return bool(result.stdout.strip())


def has_path_changes(repo_root: Path, pathspec: str) -> bool:
    result = run(["git", "status", "--porcelain", "--", pathspec], cwd=repo_root, capture=True)
    return bool(result.stdout.strip())

def has_any_path_changes(repo_root: Path, pathspecs: list[str]) -> bool:
    result = run(["git", "status", "--porcelain", "--", *pathspecs], cwd=repo_root, capture=True)
    return bool(result.stdout.strip())

def sync_publish_docs(repo_root: Path, dry_run: bool) -> list[Path]:
    source_user_guide = repo_root / "Documentation" / "USER_GUIDE.md"
    source_privacy = repo_root / "Documentation" / "PRIVACY_POLICY.md"
    target_readme = repo_root / "README.md"
    target_privacy = repo_root / "PRIVACY_POLICY.md"

    updated: list[Path] = []
    mappings = [
        (source_user_guide, target_readme),
        (source_privacy, target_privacy),
    ]
    for source, target in mappings:
        if not source.exists():
            continue
        source_bytes = source.read_bytes()
        target_bytes = target.read_bytes() if target.exists() else b""
        if source_bytes == target_bytes:
            continue
        if not dry_run:
            shutil.copy2(source, target)
        updated.append(target)
    return updated


def main() -> int:
    parser = argparse.ArgumentParser(description="Commit and push Datasets/* changes to GitHub")
    parser.add_argument(
        "--pathspec",
        nargs="+",
        default=["Datasets", "README.md", "PRIVACY_POLICY.md"],
        help="git pathspec(s) to stage (default: Datasets README.md PRIVACY_POLICY.md)",
    )
    parser.add_argument("--message", default="catalog: sync generated dataset artifacts", help="commit message")
    parser.add_argument("--remote-url", default="https://github.com/kiritv/QuoteIt.git", help="GitHub remote URL")
    parser.add_argument("--branch", default="main", help="target branch (default: main)")
    parser.add_argument("--token-env", default="GITHUB_TOKEN", help="token env var name (default: GITHUB_TOKEN)")
    parser.add_argument(
        "--token-file",
        default="Credentials/github_token.txt",
        help="fallback token file path (default: Credentials/github_token.txt)",
    )
    parser.add_argument("--dry-run", action="store_true", help="preview without committing/pushing")
    parser.add_argument(
        "--sync-docs",
        action="store_true",
        default=False,
        help=(
            "also sync Documentation/USER_GUIDE.md→README.md and "
            "Documentation/PRIVACY_POLICY.md→PRIVACY_POLICY.md before committing "
            "(off by default to avoid coupling doc changes to catalog pushes)"
        ),
    )
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)

    token_file = Path(args.token_file)
    if not token_file.is_absolute():
        token_file = (workspace_root / token_file).resolve()

    if args.sync_docs:
        synced_docs = sync_publish_docs(repo_root, dry_run=args.dry_run)
        if synced_docs:
            for path in synced_docs:
                print(f"Synchronized doc: {path.relative_to(repo_root)}")

    if not has_any_path_changes(repo_root, args.pathspec):
        print(f"No changes found under pathspecs: {', '.join(args.pathspec)}.")
        return 0

    if args.dry_run:
        print(f"[DRY-RUN] Would stage pathspecs: {', '.join(args.pathspec)}")
        print(f"[DRY-RUN] Would commit message: {args.message}")
        print(f"[DRY-RUN] Would push to: {args.remote_url} branch={args.branch}")
        return 0

    token = load_token(args.token_env, token_file)
    basic = base64.b64encode(f"x-access-token:{token}".encode("utf-8")).decode("ascii")
    auth_header = f"AUTHORIZATION: basic {basic}"

    run(["git", "add", *args.pathspec], cwd=repo_root)
    if not has_staged_changes(repo_root):
        print("No staged changes after git add; nothing to commit.")
        return 0

    run(["git", "commit", "-m", args.message], cwd=repo_root)
    run(
        [
            "git",
            "-c",
            f"http.https://github.com/.extraheader={auth_header}",
            "push",
            args.remote_url,
            f"HEAD:{args.branch}",
        ],
        cwd=repo_root,
    )

    print(f"Pushed commit to {args.remote_url} ({args.branch})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
