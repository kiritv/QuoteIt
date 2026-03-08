#!/usr/bin/env python3
from __future__ import annotations

import base64
import os
import stat
import sys
from pathlib import Path


def resolve_workspace_root() -> Path:
    return Path(__file__).resolve().parents[2]


def validate_b64_key(path: Path, expected_len: int) -> tuple[bool, str]:
    if not path.exists():
        return False, "missing"
    try:
        raw = path.read_text(encoding="utf-8").strip()
    except Exception as exc:
        return False, f"unreadable: {exc}"
    if not raw:
        return False, "empty"
    try:
        decoded = base64.b64decode(raw, validate=True)
    except Exception as exc:
        return False, f"invalid_base64: {exc}"
    if len(decoded) != expected_len:
        return False, f"invalid_length:{len(decoded)} expected:{expected_len}"
    return True, "ok"


def mode_octal(path: Path) -> str:
    mode = path.stat().st_mode
    return oct(stat.S_IMODE(mode))


def is_private_mode_ok(path: Path) -> bool:
    mode = stat.S_IMODE(path.stat().st_mode)
    return mode == 0o600


def main() -> int:
    workspace_root = resolve_workspace_root()
    creds_root = workspace_root / "Credentials"
    private_path = creds_root / "catalog_signing_private.key.b64"
    public_path = creds_root / "catalog_signing_public.key.b64"

    private_ok, private_status = validate_b64_key(private_path, 32)
    public_ok, public_status = validate_b64_key(public_path, 32)

    env_private = bool(os.environ.get("CATALOG_SIGNING_KEY", "").strip())
    env_public = bool(os.environ.get("CATALOG_SIGNING_PUBLIC_KEY", "").strip())

    print("Catalog Signing Key Status")
    print(f"- workspace: {workspace_root}")
    print(f"- private_file: {private_path}")
    print(f"  - status: {private_status}")
    if private_path.exists():
        print(f"  - mode: {mode_octal(private_path)}")
    print(f"- public_file: {public_path}")
    print(f"  - status: {public_status}")
    if public_path.exists():
        print(f"  - mode: {mode_octal(public_path)}")
    print(f"- env.CATALOG_SIGNING_KEY: {'set' if env_private else 'not set'}")
    print(f"- env.CATALOG_SIGNING_PUBLIC_KEY: {'set' if env_public else 'not set'}")

    failures = []
    if not private_ok:
        failures.append("private key file invalid")
    if not public_ok:
        failures.append("public key file invalid")
    if private_path.exists() and not is_private_mode_ok(private_path):
        failures.append("private key file mode should be 0600")

    if failures:
        print("Result: FAIL")
        for item in failures:
            print(f"- {item}")
        return 1

    print("Result: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
