---
name: model-data-assets
description: Manage AutoResearch model weights and dataset assets. Use when downloading, locating, staging, recording, auditing, or cleaning model/data caches such as Qwen3.5-2B or geo3k; when editing config/data.yaml; when deciding local versus remote storage; or when an adapter needs dataset/model paths, ModelScope/Hugging Face source priority, proxy behavior, or remote asset registry rules.
---

# Model/Data Assets

## Overview

Use this skill as the workspace-core contract for model weights and dataset assets. It owns the local `config/data.yaml` registry, the `config/data.example.yaml` template, the local cache root, source priority, proxy fallback, and the rule for when bytes live on the Mac versus a remote server.

## Boundary

| Use | Don't Use |
|---|---|
| Download or locate model weights and datasets | Run training or render reports |
| Record asset source, size, cache path, remote IP, and remote path | Store passwords or tokens in asset registry |
| Decide local versus remote storage using configured size limits | Override adapter-specific training configs |
| Maintain ModelScope-first, Hugging Face fallback behavior | Replace network readiness checks |
| Provide canonical paths to workspace adapters such as Verl | Hide remote-only assets from local config |

## Workflow

1. Read `config/config.yaml` for `verl_case.cache_root`, `verl_case.local_asset_limit_gb`, server names, hosts, and preferred remote workdir.
2. Read `config/data.yaml` before downloading anything. If it is absent, use `config/data.example.yaml` as the schema and create a local ignored copy.
3. Resolve the asset by stable key, canonical id, kind (`model` or `dataset`), source ids, and storage policy.
4. Before any network download for weights or datasets, run remote local-asset discovery on the candidate machines. Search mandatory roots first: `/home/data`, `/data*`, and each user directory's `data` subdirectory such as `/home/*/data`. Then check common supplemental roots when present, such as `/home/weights`, `/home/*/weights`, `/home/*/res/weights`, and existing `autoresearch-assets` roots.
5. Record every discovered dataset or weight directory larger than 10GB in `config/data.yaml` under `discovered_large_assets`, including server, host, path, size, kind guess, and evidence files. Prefer a verified discovered path over a network download when it matches the requested canonical asset.
6. Prefer ModelScope for downloads only after discovery does not find a usable local or remote copy. Fall back to Hugging Face when ModelScope is missing, incomplete, or unavailable.
7. If Hugging Face or GitHub access fails from China, retry through `http://127.0.0.1:7890` on the Mac. For remote hosts without network, download locally and stage over SSH, or use the network skill's proxy/tunnel path.
8. Keep assets within `local_asset_limit_gb` under the Mac cache root, normally `/Users/Zhuanz/autoResearchData`. Put large assets on remote servers under a stable remote asset root, normally beneath `/home/t00906153`.
9. For one large model copied to several machines, keep one canonical asset entry and record each physical host path under `remotes.<server-name>`. Do not create fake per-machine model ids.
10. Update `config/data.yaml` after every successful discovery, download, stage, move, or verification. The registry is the source of truth for where assets are stored.

## Registry Rules

- Keep real machine-specific registry state in `config/data.yaml`; keep the shareable template in `config/data.example.yaml`.
- Do not put secrets, API tokens, cookies, SSH keys, or passwords in `config/data.yaml`.
- Record both logical identity and physical location: model size or dataset name, source website, local path, remote server name, remote IP, and remote directory.
- Do not rely on an adapter's hard-coded path when a registry entry exists.
- Treat missing registry entries as a setup gap, not permission to silently download to arbitrary paths.
- `remote` is the legacy/single primary location. `remotes` is the preferred multi-machine map keyed by server name; adapters must choose the entry matching the selected server name or host.
- Discovery records are inventory, not canonical assets. Keep them under `discovered_large_assets` until a path is verified to satisfy a specific model or dataset request.

## References

- Read `references/asset-registry.md` when editing `config/data.yaml`, changing source priority, adding a model or dataset, or deciding whether an asset belongs on the Mac or a remote server.
