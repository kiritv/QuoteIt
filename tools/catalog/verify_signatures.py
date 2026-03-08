#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from pathlib import Path
from typing import Dict, List

try:
    from nacl.signing import VerifyKey
    from nacl.exceptions import BadSignatureError
except ImportError:
    VerifyKey = None
    BadSignatureError = Exception


def load_public_key(public_key_b64: str) -> bytes:
    return base64.b64decode(public_key_b64, validate=True)

def load_public_key_b64(public_key_arg: str, public_key_env: str, public_key_file: Path) -> str:
    if public_key_arg.strip():
        return public_key_arg.strip()
    env_val = os.environ.get(public_key_env, "").strip()
    if env_val:
        return env_val
    if public_key_file.exists():
        file_val = public_key_file.read_text(encoding="utf-8").strip()
        if file_val:
            return file_val
        raise ValueError(f"Public key file is empty: {public_key_file}")
    raise ValueError(
        f"Missing public key. Pass --public-key, set {public_key_env}, or create {public_key_file}."
    )

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


def verify_index_file(verify_key: VerifyKey, json_path: Path, sig_path: Path) -> None:
    payload = json_path.read_bytes()
    sig_b64 = sig_path.read_text(encoding="utf-8").strip()
    signature = base64.b64decode(sig_b64, validate=True)
    verify_key.verify(payload, signature)


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify ED25519 signatures for catalog index files")
    parser.add_argument(
        "--indexes-root",
        default="tools/catalog/output/indexes",
        help="Path to indexes directory (default: tools/catalog/output/indexes)",
    )
    parser.add_argument(
        "--public-key",
        default="",
        help="Base64 ED25519 public key. If omitted, read from --public-key-env.",
    )
    parser.add_argument(
        "--public-key-env",
        default="CATALOG_SIGNING_PUBLIC_KEY",
        help="Env var containing Base64 ED25519 public key (default: CATALOG_SIGNING_PUBLIC_KEY)",
    )
    parser.add_argument(
        "--public-key-file",
        default="Credentials/catalog_signing_public.key.b64",
        help="Fallback public key file path (default: Credentials/catalog_signing_public.key.b64)",
    )
    args = parser.parse_args()

    if VerifyKey is None:
        print("PyNaCl is required for ED25519 verification. Install with: pip install pynacl")
        return 2

    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)
    indexes_root = (repo_root / args.indexes_root).resolve()
    if not Path(args.indexes_root).is_absolute():
        indexes_root = (workspace_root / args.indexes_root).resolve()
    if not indexes_root.exists():
        print(f"Indexes root does not exist: {indexes_root}")
        return 1

    public_key_file = Path(args.public_key_file)
    if not public_key_file.is_absolute():
        public_key_file = (repo_root.parent / public_key_file).resolve() if repo_root.name == "QuoteIt" else (repo_root / public_key_file).resolve()
    try:
        public_key_b64 = load_public_key_b64(args.public_key, args.public_key_env, public_key_file)
    except ValueError as exc:
        print(str(exc))
        return 1

    try:
        verify_key = VerifyKey(load_public_key(public_key_b64))
    except Exception as exc:
        print(f"Invalid public key: {exc}")
        return 1

    manifest_path = indexes_root / "signing-manifest.json"
    if not manifest_path.exists():
        print(f"Missing signing-manifest.json in {indexes_root}")
        return 1

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        print(f"Invalid signing-manifest.json: {exc}")
        return 1

    files: Dict[str, Dict[str, str]] = manifest.get("files", {})
    if not isinstance(files, dict) or not files:
        print("signing-manifest.json contains no files")
        return 1

    failures: List[str] = []
    for file_name, info in sorted(files.items()):
        json_path = indexes_root / file_name
        sig_name = str(info.get("signatureFile", f"{file_name}.sig"))
        sig_path = indexes_root / sig_name
        if not json_path.exists():
            failures.append(f"Missing JSON file: {file_name}")
            continue
        if not sig_path.exists():
            failures.append(f"Missing signature file: {sig_name}")
            continue

        expected_sha = str(info.get("sha256", "")).lower()
        actual_sha = hashlib.sha256(json_path.read_bytes()).hexdigest()
        if expected_sha and expected_sha != actual_sha:
            failures.append(f"SHA mismatch: {file_name}")
            continue

        try:
            verify_index_file(verify_key, json_path, sig_path)
        except BadSignatureError:
            failures.append(f"Invalid signature: {sig_name}")
        except Exception as exc:
            failures.append(f"Verification error for {file_name}: {exc}")

    if failures:
        print("Signature verification failed:")
        for item in failures:
            print(f"- {item}")
        return 1

    print(f"Signature verification passed for {len(files)} index files in {indexes_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
