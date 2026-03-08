# Catalog Tooling (QIT-6004 + QIT-6006d)

Direct tooling for local dataset offload + distributed catalog artifacts.

## Target structure

```text
Datasets/
  Collections/*.json
  Sources/*.manifest.json
  Packs/*.json
  Programs/*.json
tools/catalog/output/
  metadata/{lang}/*.json
  packages/{lang}/*.quoteit
  packs/{lang}/index.json
  programs/{lang}/index.json
  indexes/
    datasets-{lang}.json
    packs-{lang}.json
    programs-{lang}.json
    index-manifest.json
    signing-manifest.json
    *.sig
```

## Commands

From workspace repo root:

```bash
python3 tools/catalog/init_catalog_layout.py
python3 tools/catalog/keys_status.py
python3 tools/catalog/validate_catalog.py
python3 tools/catalog/build_indexes.py
python3 tools/catalog/sign_indexes.py --private-key-env CATALOG_SIGNING_KEY
python3 tools/catalog/verify_signatures.py --public-key-env CATALOG_SIGNING_PUBLIC_KEY
python3 tools/catalog/publish_to_github.py --dry-run
python3 tools/catalog/publish_to_github.py
python3 tools/catalog/commit_and_push.py --dry-run
python3 tools/catalog/commit_and_push.py
python3 tools/catalog/publish_catalog.py --validate --build --sign --verify --sync-github-tree
python3 tools/catalog/publish_catalog.py --validate --build --sign --verify --sync-github-tree --push-github
python3 tools/catalog/archive_published_dataset.py --source-id rumiMasnavi
python3 tools/catalog/restore_dataset_to_app.py --source-id rumiMasnavi --dry-run
python3 tools/catalog/restore_dataset_to_app.py --source-id rumiMasnavi
```

## What each script does

- `validate_catalog.py`
  - Validates metadata JSON and pack JSON schema basics.
  - Enforces source ID uniqueness.
  - Ensures pack `sourceIds` map to existing metadata source IDs.
  - Ensures program `requiredSourceIds` map to existing metadata source IDs.
  - Blocks app-bundled source IDs from online catalog (currently `standardQuotes`).

- `build_indexes.py`
  - Builds online artifacts from local canonical files.
  - Generates language-scoped metadata under `tools/catalog/output/metadata/{lang}/`.
  - Generates language-scoped index files under `tools/catalog/output/indexes/`.
  - Also writes pack/program language indexes under `tools/catalog/output/packs/{lang}/index.json`
    and `tools/catalog/output/programs/{lang}/index.json`.

- `sign_indexes.py`
  - Signs all index JSON files with ED25519.
  - Writes sidecar signatures (`.sig`) plus `signing-manifest.json`.

- `verify_signatures.py`
  - Verifies `.sig` files against the public key before publish/CI pass.

- `publish_catalog.py`
  - Orchestrates validate/build/sign/verify and optional GitHub tree sync in one command.

- `publish_to_github.py`
  - Syncs generated `tools/catalog/output/*` into repo `Datasets/*` for commit/push.
  - Mirrors only publish folders: `metadata`, `packages`, `packs`, `programs`, `indexes`.
  - Supports `--dry-run` preview mode and removes stale files in synced folders.

- `commit_and_push.py`
  - Before staging, synchronizes:
    - `Documentation/USER_GUIDE.md` -> `README.md`
    - `Documentation/PRIVACY_POLICY.md` -> `PRIVACY_POLICY.md`
  - Stages `Datasets/*`, `README.md`, and `PRIVACY_POLICY.md`, then commits/pushes to GitHub.
  - Reads token from `GITHUB_TOKEN` or fallback `Credentials/github_token.txt`.
  - Supports `--dry-run`.

- `init_catalog_layout.py`
  - Creates the required `Datasets/` folder structure with language subfolders.
  - Safe to run repeatedly.

- `keys_status.py`
  - Preflight check for signing keys.
  - Validates Base64 format/length and private key file mode (`0600`).

- `archive_published_dataset.py`
  - Moves a pushed dataset out of app-bundle paths (`QuoteIt/QuoteIt/Data/...`) into `QuoteIt/Datasets/...`.
  - Keeps the same subfolder names (`Collections/`, `Sources/`) to stay simple locally.
  - Refuses protected bundled IDs (currently `standardQuotes`).

- `restore_dataset_to_app.py`
  - Restores one dataset from `QuoteIt/Datasets/{Sources,Collections}` into app bundle `QuoteIt/QuoteIt/Data/{Sources,Collections}`.
  - Default mode is copy-only (archive remains intact); optional `--delete-from-archive`.
  - Supports `--dry-run` and `--overwrite`.

## Publish mapping

- Local generated output stays in `tools/catalog/output/*`.
- Publish copies those artifacts to GitHub under `Datasets/*` (without an `Online/` layer).
- `publish_to_github.py` is the canonical sync step for this mapping.
- `commit_and_push.py` is the optional final push step for a one-command operator flow.

## Notes

- Signature format: Base64 ED25519 in `*.sig` sidecars.
- Private key source: env var `CATALOG_SIGNING_KEY` (Base64 seed/private key bytes).
- Public key source for verification: env var `CATALOG_SIGNING_PUBLIC_KEY` (Base64 32-byte key).
- Default key file fallbacks:
  - `Credentials/catalog_signing_private.key.b64`
  - `Credentials/catalog_signing_public.key.b64`
- Protected bundled source IDs that must never go online: `standardQuotes`.
