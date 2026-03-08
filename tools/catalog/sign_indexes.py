#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

try:
    from nacl.signing import SigningKey
except ImportError:
    SigningKey = None


def now_utc() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


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


def decode_private_key_from_env(env_name: str) -> bytes:
    raw = os.environ.get(env_name, "").strip()
    if not raw:
        raise ValueError(
            f"Missing env var {env_name}. Expected Base64-encoded ED25519 private key seed (32 bytes) "
            "or 64-byte private key."
        )
    try:
        key_bytes = base64.b64decode(raw, validate=True)
    except Exception as exc:
        raise ValueError(f"{env_name} is not valid Base64: {exc}") from exc

    if len(key_bytes) == 32:
        return key_bytes
    if len(key_bytes) == 64:
        return key_bytes[:32]
    raise ValueError(f"{env_name} decoded length must be 32 or 64 bytes, got {len(key_bytes)}")

def load_private_key(private_key_env: str, private_key_file: Path) -> bytes:
    env_value = os.environ.get(private_key_env, "").strip()
    if env_value:
        return decode_private_key_from_env(private_key_env)
    if private_key_file.exists():
        raw = private_key_file.read_text(encoding="utf-8").strip()
        if not raw:
            raise ValueError(f"Private key file is empty: {private_key_file}")
        try:
            key_bytes = base64.b64decode(raw, validate=True)
        except Exception as exc:
            raise ValueError(f"Private key file is not valid Base64: {private_key_file} ({exc})") from exc
        if len(key_bytes) == 32:
            return key_bytes
        if len(key_bytes) == 64:
            return key_bytes[:32]
        raise ValueError(f"Private key file decoded length must be 32 or 64 bytes, got {len(key_bytes)}")
    raise ValueError(
        f"Missing key: set {private_key_env} or create {private_key_file}"
    )


def collect_index_files(indexes_root: Path) -> List[Path]:
    return sorted(
        p for p in indexes_root.glob("*.json")
        if p.name not in {"signing-manifest.json"}
    )


def sign_file(signing_key: SigningKey, path: Path) -> str:
    payload = path.read_bytes()
    signed = signing_key.sign(payload)
    signature_bytes = signed.signature
    signature_b64 = base64.b64encode(signature_bytes).decode("ascii")
    path.with_suffix(path.suffix + ".sig").write_text(signature_b64 + "\n", encoding="utf-8")
    return hashlib.sha256(payload).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description="Sign catalog index JSON files with ED25519")
    parser.add_argument(
        "--indexes-root",
        default="tools/catalog/output/indexes",
        help="Path to indexes directory (default: tools/catalog/output/indexes)",
    )
    parser.add_argument(
        "--private-key-env",
        default="CATALOG_SIGNING_KEY",
        help="Env var containing Base64 private signing key seed (default: CATALOG_SIGNING_KEY)",
    )
    parser.add_argument(
        "--private-key-file",
        default="Credentials/catalog_signing_private.key.b64",
        help="Fallback private key file path (default: Credentials/catalog_signing_private.key.b64)",
    )
    parser.add_argument(
        "--public-key-out",
        default="",
        help="Optional output file path to write Base64 public key",
    )
    args = parser.parse_args()

    if SigningKey is None:
        print("PyNaCl is required for ED25519 signing. Install with: pip install pynacl")
        return 2

    repo_root = resolve_repo_root()
    workspace_root = resolve_workspace_root(repo_root)
    indexes_root = (repo_root / args.indexes_root).resolve()
    if not Path(args.indexes_root).is_absolute():
        indexes_root = (workspace_root / args.indexes_root).resolve()
    if not indexes_root.exists():
        print(f"Indexes root does not exist: {indexes_root}")
        return 1

    files = collect_index_files(indexes_root)
    if not files:
        print(f"No index JSON files found in {indexes_root}")
        return 1

    try:
        private_key_file = Path(args.private_key_file)
        if not private_key_file.is_absolute():
            private_key_file = (repo_root.parent / private_key_file).resolve() if repo_root.name == "QuoteIt" else (repo_root / private_key_file).resolve()
        private_seed = load_private_key(args.private_key_env, private_key_file)
        signing_key = SigningKey(private_seed)
    except ValueError as exc:
        print(f"Signing key error: {exc}")
        return 1

    public_key_bytes = bytes(signing_key.verify_key)
    public_key_b64 = base64.b64encode(public_key_bytes).decode("ascii")
    key_id = hashlib.sha256(public_key_bytes).hexdigest()[:16]

    signed_files: Dict[str, Dict[str, str]] = {}
    for path in files:
        sha = sign_file(signing_key, path)
        signed_files[path.name] = {
            "sha256": sha,
            "signatureFile": f"{path.name}.sig",
        }

    manifest = {
        "formatVersion": 1,
        "algorithm": "ed25519",
        "generatedAt": now_utc(),
        "keyId": key_id,
        "files": signed_files,
    }
    (indexes_root / "signing-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    if args.public_key_out:
        public_key_path = Path(args.public_key_out)
        if not public_key_path.is_absolute():
            public_key_path = (repo_root / public_key_path).resolve()
        public_key_path.parent.mkdir(parents=True, exist_ok=True)
        public_key_path.write_text(public_key_b64 + "\n", encoding="utf-8")
        print(f"Public key written: {public_key_path}")

    print(f"Signed {len(files)} index files in {indexes_root}")
    print(f"Key ID: {key_id}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
