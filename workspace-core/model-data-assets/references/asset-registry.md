# Asset Registry

## Purpose

Use `config/data.yaml` as the local registry for model weights and datasets. It records what an asset is, where it came from, where its bytes live, and which path adapters should use.

Keep `config/data.example.yaml` tracked as the shareable template. Keep real `config/data.yaml` ignored, because it can contain machine-specific IPs and directories.

## Storage Policy

- Store small assets on the Mac under `defaults.local_root`, normally `/Users/Zhuanz/autoResearchData`.
- Use the configured local size threshold, normally `5` GB from `verl_case.local_asset_limit_gb`.
- Store large assets on a remote server under `defaults.remote_root`, normally `/home/t00906153/autoresearch-assets`.
- Always record remote server name, host/IP, and absolute remote path when bytes live remotely.
- When the same large asset is copied to multiple machines, keep one asset entry and record all host-specific paths in `remotes.<server-name>`.
- Prefer stable directory names by replacing `/` with `__`, for example `Qwen__Qwen3.5-2B`.

## Download Priority

0. Before any network download, search the remote machines for existing large local assets. Mandatory first-pass roots are `/home/data`, `/data*`, and user `data` directories such as `/home/*/data`. Also scan common supplemental roots when they exist, including `/home/weights`, `/home/*/weights`, `/home/*/res/weights`, and existing `autoresearch-assets` roots.
1. Record every likely dataset or weight path larger than 10GB in `discovered_large_assets`.
2. Reuse a discovered path when it can be verified against the requested canonical asset.
3. Try ModelScope only when discovery does not find a usable copy.
4. Fall back to Hugging Face.
5. If Hugging Face or GitHub access fails on the Mac, retry through `http://127.0.0.1:7890`.
6. If the remote server has no network, download on the Mac and stage over SSH, or use the existing network proxy/tunnel path.

Use the source ids in the registry instead of guessing ids from adapter code. If a ModelScope id differs from a Hugging Face id, record both.

## Required Fields

For each asset, include:

- `key`: stable short key used by humans and adapters.
- `kind`: `model` or `dataset`.
- `canonical_id`: the upstream id used by the adapter, such as `Qwen/Qwen3.5-2B`.
- `display_name`: readable asset name.
- `source_priority`: ordered source labels, normally `["modelscope", "huggingface"]`.
- `sources`: source-specific ids and URLs.
- `size_gb`: approximate size when known.
- `parameter_count_b`: model parameter count when known.
- `storage_policy`: `local_if_within_limit`, `remote_preferred`, or `remote_only`.
- `local.path`: absolute Mac cache path, if present or intended.
- `remote.server`, `remote.host`, and `remote.path`: legacy or primary remote location, if present or intended.
- `remotes.<server>.server`, `remotes.<server>.host`, and `remotes.<server>.path`: preferred multi-machine remote locations for one canonical asset.
- `remotes.<server>.status`, `verified_at`, `checked_at`, and `note`: optional per-machine operational state. Use `ready`, `copying`, or `blocked` when a multi-machine rollout is only partially complete.
- `status`: `planned`, `downloading`, `ready`, `missing`, or `stale`.
- `updated_at`: ISO date or datetime for the last registry update.

Do not store tokens, passwords, cookies, or private URLs with credentials in this file.

## Discovery Inventory

`discovered_large_assets` is an operational inventory of large paths found on remote machines before downloading. It is intentionally separate from canonical `assets.models` and `assets.datasets`.

Each entry should include:

- `server`: server name from `config/config.yaml`.
- `host`: host/IP from `config/config.yaml`.
- `path`: absolute remote path.
- `size_gb`: apparent or allocated size in GB.
- `kind_guess`: `model`, `dataset`, or `unknown`.
- `name_guess`: readable path basename or inferred model/dataset name.
- `evidence`: files or markers that justify the guess, such as `model.safetensors.index.json`, `config.json`, `.parquet`, `.jsonl`, `.arrow`, `.bin`, or shard counts.
- `status`: `discovered`, `verified`, `ignored`, or `stale`.
- `scanned_at`: ISO timestamp.

Do not treat a discovery entry as reusable until the requested adapter verifies identity and completeness. When a discovery entry is verified for a specific canonical asset, copy its path into that asset's `remote` or `remotes.<server>` location.

## Example Layout

```yaml
version: 1
defaults:
  local_root: /Users/Zhuanz/autoResearchData
  local_asset_limit_gb: 5
  proxy_url: http://127.0.0.1:7890
  source_priority: [modelscope, huggingface]
  remote_root: /home/t00906153/autoresearch-assets

assets:
  models:
    qwen3-5-2b:
      kind: model
      canonical_id: Qwen/Qwen3.5-2B
      display_name: Qwen3.5-2B
      parameter_count_b: 2
      size_gb: null
      storage_policy: local_if_within_limit
      source_priority: [modelscope, huggingface]
      sources:
        modelscope:
          id: Qwen/Qwen3.5-2B
          url: https://modelscope.cn/models/Qwen/Qwen3.5-2B
        huggingface:
          id: Qwen/Qwen3.5-2B
          url: https://huggingface.co/Qwen/Qwen3.5-2B
      local:
        path: /Users/Zhuanz/autoResearchData/models/Qwen__Qwen3.5-2B
      remote:
        server: A2-AK-225
        host: 192.168.9.225
        path: /home/t00906153/autoresearch-assets/models/Qwen__Qwen3.5-2B
      remotes:
        A2-AK-225:
          server: A2-AK-225
          host: 192.168.9.225
          path: /home/t00906153/autoresearch-assets/models/Qwen__Qwen3.5-2B
      status: planned
      updated_at: null

  datasets:
    geo3k:
      kind: dataset
      canonical_id: hiyouga/geometry3k
      display_name: geometry3k
      size_gb: null
      storage_policy: local_if_within_limit
      source_priority: [modelscope, huggingface]
      sources:
        modelscope:
          id: hiyouga/geometry3k
          url: https://modelscope.cn/datasets/hiyouga/geometry3k
        huggingface:
          id: hiyouga/geometry3k
          url: https://huggingface.co/datasets/hiyouga/geometry3k
      local:
        path: /Users/Zhuanz/autoResearchData/datasets/hiyouga__geometry3k
      remote:
        server: A2-AK-225
        host: 192.168.9.225
        path: /home/t00906153/autoresearch-assets/datasets/hiyouga__geometry3k
      status: planned
      updated_at: null
```

## Adapter Contract

Adapters must:

- Read this registry before downloading or staging assets.
- Reuse `local.path`, matching `remotes.<server>.path`, or legacy `remote.path` when `status` is `ready`.
- Update status and paths after successful preparation.
- Add a new registry entry when introducing a new model or dataset.
- Avoid conflicting source priority or cache layout rules in adapter-level skills.
