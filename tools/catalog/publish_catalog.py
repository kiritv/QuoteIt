#!/usr/bin/env python3
import argparse
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> None:
    print("+", " ".join(cmd))
    subprocess.run(cmd, check=True)


def resolve_repo_root() -> Path:
    base = Path(__file__).resolve().parents[2]
    candidate = base / "QuoteIt"
    if (candidate / "Datasets").exists():
        return candidate
    return base


def main() -> int:
    parser = argparse.ArgumentParser(description="Catalog publish orchestrator")
    parser.add_argument("--validate", action="store_true", help="run validate_catalog.py")
    parser.add_argument("--build", action="store_true", help="run build_indexes.py")
    parser.add_argument("--sign", action="store_true", help="sign index JSON files with ED25519 (.sig)")
    parser.add_argument("--verify", action="store_true", help="verify generated signatures after signing")
    parser.add_argument(
        "--sync-github-tree",
        action="store_true",
        help="sync tools/catalog/output/* into repo Datasets/*",
    )
    parser.add_argument(
        "--sync-dry-run",
        action="store_true",
        help="preview sync operations without writing files (requires --sync-github-tree)",
    )
    parser.add_argument(
        "--push-github",
        action="store_true",
        help="commit and push Datasets/* changes to GitHub after sync",
    )
    parser.add_argument(
        "--push-branch",
        default="main",
        help="target branch for --push-github (default: main)",
    )
    parser.add_argument(
        "--push-remote-url",
        default="https://github.com/kiritv/QuoteIt.git",
        help="target remote URL for --push-github",
    )
    parser.add_argument(
        "--push-message",
        default="catalog: sync generated dataset artifacts",
        help="commit message for --push-github",
    )
    parser.add_argument(
        "--push-dry-run",
        action="store_true",
        help="preview commit/push operations (requires --push-github)",
    )
    parser.add_argument(
        "--push-sync-docs",
        action="store_true",
        default=False,
        help="also sync USER_GUIDE.md→README.md during push (off by default)",
    )
    parser.add_argument(
        "--private-key-env",
        default="CATALOG_SIGNING_KEY",
        help="env var for private signing key (default: CATALOG_SIGNING_KEY)",
    )
    parser.add_argument(
        "--public-key-env",
        default="CATALOG_SIGNING_PUBLIC_KEY",
        help="env var for public verification key (default: CATALOG_SIGNING_PUBLIC_KEY)",
    )
    args = parser.parse_args()

    repo_root = resolve_repo_root()
    tools_root = repo_root.parent / "tools" / "catalog" if repo_root.name == "QuoteIt" else repo_root / "tools" / "catalog"

    if not any([args.validate, args.build, args.sign, args.verify, args.sync_github_tree, args.push_github]):
        args.validate = True
        args.build = True
        args.sign = True
        args.verify = True
        args.sync_github_tree = True

    try:
        if args.validate:
            run([sys.executable, str(tools_root / "validate_catalog.py")])
        if args.build:
            run([sys.executable, str(tools_root / "build_indexes.py")])
        if args.sign:
            run([
                sys.executable,
                str(tools_root / "sign_indexes.py"),
                "--private-key-env",
                args.private_key_env,
            ])
        if args.verify:
            run([
                sys.executable,
                str(tools_root / "verify_signatures.py"),
                "--public-key-env",
                args.public_key_env,
            ])
        if args.sync_github_tree:
            cmd = [sys.executable, str(tools_root / "publish_to_github.py")]
            if args.sync_dry_run:
                cmd.append("--dry-run")
            run(cmd)
        if args.push_github:
            cmd = [
                sys.executable,
                str(tools_root / "commit_and_push.py"),
                "--branch",
                args.push_branch,
                "--remote-url",
                args.push_remote_url,
                "--message",
                args.push_message,
            ]
            if args.push_dry_run:
                cmd.append("--dry-run")
            if args.push_sync_docs:
                cmd.append("--sync-docs")
            run(cmd)
    except subprocess.CalledProcessError as exc:
        print(f"Command failed with code {exc.returncode}")
        return exc.returncode

    print("Catalog publish flow completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
