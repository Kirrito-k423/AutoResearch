#!/usr/bin/env python3
"""扫描 Verl examples 参数，生成中文参数解释库与 Excel 汇总。"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import urllib.parse
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable
from xml.sax.saxutils import escape


HYDRA_RE = re.compile(
    r"(?P<key>\+?[A-Za-z0-9_][A-Za-z0-9_.-]*(?:\.[A-Za-z0-9_.-]+)+)=(?P<value>\"[^\"]*\"|'[^']*'|\$\{[^}]+\}|[^\s\\)]+)"
)
ENV_DEFAULT_RE = re.compile(r"^\s*(?P<var>[A-Za-z_][A-Za-z0-9_]*)=\$\{(?P<env>[A-Za-z_][A-Za-z0-9_]*):-?(?P<default>[^}]*)\}")
ASSIGN_RE = re.compile(r"^\s*(?P<var>[A-Za-z_][A-Za-z0-9_]*)=(?P<value>[^\s#]+)")
FLAG_RE = re.compile(r"(?P<flag>--[A-Za-z][A-Za-z0-9_.-]*)(?:[= ](?P<value>[^\s\\]+))?")
TEXT_SUFFIXES = {".sh", ".yaml", ".yml"}
NPU_TOKENS = ("npu", "ascend", "torch_npu", "hccl", "cann", "910", "mindspeed")
EXCEL_COLUMNS = ["参数名", "分类", "中文解释", "常见值", "性能影响", "精度影响", "示例数"]


@dataclass
class Evidence:
    path: str
    line: int
    text: str


@dataclass
class ParamFeature:
    parameter: str
    category: str
    values: set[str] = field(default_factory=set)
    env_vars: set[str] = field(default_factory=set)
    scripts: set[str] = field(default_factory=set)
    evidence: list[Evidence] = field(default_factory=list)
    count: int = 0
    saw_npu: bool = False
    saw_ci: bool = False


def git_value(repo: Path, *args: str) -> str:
    try:
        return subprocess.check_output(["git", "-C", str(repo), *args], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def iter_example_files(repo: Path, roots: Iterable[str]) -> Iterable[Path]:
    for root in roots:
        base = repo / root
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                yield path


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(errors="ignore").splitlines()
    except Exception:
        return []


def read_text(path: Path) -> str:
    try:
        return path.read_text(errors="ignore")
    except Exception:
        return ""


def normalize_value(value: str) -> str:
    return value.strip().strip(",").strip()


def complete_shell_value(line: str, value_start: int, raw: str) -> str:
    if raw.startswith("$(("):
        end = line.find("))", value_start)
        if end != -1:
            return line[value_start : end + 2]
    if raw.startswith("${"):
        end = line.find("}", value_start)
        if end != -1:
            return line[value_start : end + 1]
    return raw


def feature_filename(parameter: str) -> str:
    raw = parameter.lstrip("+").strip() or "unnamed"
    digest = hashlib.sha1(raw.encode("utf-8")).hexdigest()[:10]
    safe = urllib.parse.quote(raw, safe="._-+=@")
    if len(safe) > 180:
        safe = f"{safe[:160]}-{digest}"
    else:
        safe = f"{safe}-{digest}"
    return f"{safe}.md"


def category_for(parameter: str) -> str:
    """Return the three-way category requested by the user: 配置 / 算法 / 效率."""
    p = parameter.lower().lstrip("+")
    if any(x in p for x in ("path", "file", "dir", "name", "logger", "project", "experiment", "dataset", "prompt_key", "response_key", "tokenizer", "ckpt", "checkpointing_path", "save_freq", "test_freq", "val_before_train")):
        return "配置"
    if any(x in p for x in ("lr", "learning_rate", "rollout.n", "rollout_n", "adv_estimator", "kl", "entropy", "reward", "temperature", "top_p", "top_k", "do_sample", "ppo_epochs", "total_epochs", "loss", "critic_warmup", "gamma", "lam", "clip")):
        return "算法"
    return "效率"


def explain(parameter: str) -> str:
    p = parameter.lower().lstrip("+")
    rules = [
        (("rollout.name",), "选择 rollout 推理后端，例如 vLLM、SGLang 或 TensorRT-LLM，决定生成吞吐、兼容性和 NPU 迁移风险。"),
        (("tensor_model_parallel_size", "rollout_tp", "train_tp"), "控制张量并行切分度，降低单卡权重/KV 压力，但会增加层内通信。"),
        (("pipeline_model_parallel_size", "train_pp"), "控制流水并行切分度，降低单卡层数和激活压力，但会引入 pipeline bubble。"),
        (("context_parallel_size", "ulysses_sequence_parallel_size", "sp_size", "train_cp"), "控制上下文/序列并行，主要用于长序列场景降低激活和注意力显存。"),
        (("gpu_memory_utilization", "rollout_gpu_mem_util"), "控制 rollout engine 可使用的显存比例，影响 KV cache 容量、吞吐和 OOM 风险。"),
        (("rollout.n", "rollout_n", "n_samples", "n_resp_per_prompt"), "控制每个 prompt 生成多少条响应，增加探索和训练信号，但 rollout 成本近似线性上升。"),
        (("model.path", "model_path", "hf_model_path"), "指定模型权重或模型 ID，是模型规模、结构、显存占用和任务能力的来源。"),
        (("train_files", "val_files", "train_file", "test_file"), "指定训练/验证数据来源，影响任务分布、评测口径和数据加载路径。"),
        (("max_prompt_length",), "控制 prompt 最大长度，增大可覆盖更长输入，但会增加激活、注意力和数据处理成本。"),
        (("max_response_length",), "控制 response 最大长度，增大可给模型更多输出空间，但会显著增加 rollout KV cache 和耗时。"),
        (("train_batch_size",), "控制训练全局 batch，影响样本吞吐、梯度稳定性和单步耗时。"),
        (("mini_batch", "micro_batch"), "控制 PPO/反向传播分块大小，是显存占用和 step 时间的核心旋钮。"),
        (("optim.lr", "actor_lr", "learning_rate"), "控制学习率，主要影响收敛速度、稳定性和最终精度。"),
        (("kl_loss_coef", "kl_coef"), "控制 KL 惩罚强度，影响策略偏离参考模型的程度和训练稳定性。"),
        (("entropy_coeff",), "控制熵正则强度，影响采样探索和输出多样性。"),
        (("temperature", "top_p", "top_k"), "控制采样分布，直接影响探索、多样性、精度波动和可复现性。"),
        (("offload",), "把参数、梯度或优化器状态卸载到 CPU/主机侧，降低 HBM 压力但可能拖慢训练。"),
        (("gradient_checkpointing", "recompute"), "用重算换激活显存，适合长序列或大模型，但会增加计算时间。"),
        (("profiler", "global_profiler", "profile_"), "控制 profiling 采集范围和开销，用于定位耗时/显存问题，通常不直接提升精度。"),
        (("trainer.nnodes", "nnodes", "n_gpus_per_node", "npus_per_node"), "控制分布式资源规模，影响并行度、吞吐和通信开销。"),
        (("filter_overlong", "truncation"), "控制超长样本过滤或截断策略，影响有效数据量、训练稳定性和任务准确性。"),
    ]
    for needles, text in rules:
        if any(n in p for n in needles):
            return text
    return "待补充：该参数来自 Verl examples，尚未完成官方文档或仓库 docs 复核。"


def perf_impact(parameter: str) -> str:
    p = parameter.lower().lstrip("+")
    if p.endswith("rollout.name"):
        return "机制推断：不同推理后端会改变生成吞吐、显存管理、启动开销和 NPU 兼容性。"
    if any(x in p for x in ("max_prompt_length", "max_response_length", "max_model_len", "max_num_batched_tokens")):
        return "机制推断：长度越大，显存、KV cache 和单步/生成耗时通常上升。"
    if p.endswith("rollout.n") or any(x in p for x in ("batch_size", "micro_batch", "mini_batch")):
        return "机制推断：增大通常提高有效吞吐或样本量，但会增加显存和单步时间。"
    if any(x in p for x in ("tensor_model_parallel", "pipeline_model_parallel", "context_parallel", "offload", "checkpoint", "recompute", "gpu_memory_utilization", "async", "compile", "eager", "graph")):
        return "机制推断：主要改变显存、通信、计算图或调度开销之间的取舍。"
    if any(x in p for x in ("profiler", "profile")):
        return "机制推断：开启 profiling 会增加采集和落盘开销。"
    if any(x in p for x in ("logger", "project_name", "experiment_name", "save_freq", "test_freq", "file", "path", "name")):
        return "通常不直接影响计算性能；保存、评测或日志频率可能影响端到端耗时。"
    return "待补充：需要官方文档、仓库 docs 或实测数据确认性能影响。"


def accuracy_impact(parameter: str) -> str:
    p = parameter.lower().lstrip("+")
    if any(x in p for x in ("temperature", "top_p", "top_k", "do_sample")):
        return "机制推断：直接改变采样分布，影响探索、多样性和评测波动。"
    if any(x in p for x in ("kl", "entropy", "adv_estimator", "reward", "loss", "clip")):
        return "机制推断：直接改变 RL 目标、约束或优势估计，可能影响稳定性和最终精度。"
    if any(x in p for x in ("train_batch_size", "mini_batch", "micro_batch", "lr", "total_epochs", "ppo_epochs")):
        return "机制推断：影响优化动态、稳定性和收敛速度。"
    if any(x in p for x in ("max_prompt_length", "max_response_length", "truncation", "filter_overlong")):
        return "机制推断：改变有效上下文、输出空间或样本保留策略，可能影响任务准确率。"
    return "通常不直接影响精度，除非通过性能瓶颈、数据口径或训练稳定性间接影响。"


def add_feature(features: dict[str, ParamFeature], parameter: str, value: str, rel: str, line_no: int, text: str, env_var: str | None, saw_npu: bool) -> None:
    parameter = parameter.strip()
    if not parameter or parameter in {"python3", "ray"}:
        return
    key = parameter.lstrip("+")
    feature = features.get(key)
    if feature is None:
        feature = ParamFeature(parameter=key, category=category_for(key))
        features[key] = feature
    feature.count += 1
    if value:
        feature.values.add(normalize_value(value))
    if env_var:
        feature.env_vars.add(env_var)
    feature.scripts.add(rel)
    feature.saw_npu = feature.saw_npu or saw_npu
    if len(feature.evidence) < 5:
        feature.evidence.append(Evidence(rel, line_no, text.strip()[:260]))


def scan(repo: Path, roots: list[str]) -> dict:
    features: dict[str, ParamFeature] = {}
    ci_text = ""
    for ci_root in ("tests", ".github/workflows"):
        base = repo / ci_root
        if base.exists():
            chunks = []
            for path in base.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".py", ".sh", ".yaml", ".yml", ".md"}:
                    chunks.extend(read_lines(path)[:2000])
            ci_text += "\n".join(chunks).lower()

    files = list(iter_example_files(repo, roots))
    for path in files:
        rel = path.relative_to(repo).as_posix()
        rel_lower = rel.lower()
        file_saw_npu = any(token in rel_lower for token in NPU_TOKENS)
        env_defaults: dict[str, tuple[str, str]] = {}
        for line_no, line in enumerate(read_lines(path), start=1):
            lower = line.lower()
            saw_npu = file_saw_npu or any(token in lower for token in NPU_TOKENS)

            env_match = ENV_DEFAULT_RE.match(line)
            if env_match:
                local_var = env_match.group("var")
                env_name = env_match.group("env")
                default = env_match.group("default")
                env_defaults[local_var] = (env_name, default)
                add_feature(features, env_name, default, rel, line_no, line, env_name, saw_npu)

            assign_match = ASSIGN_RE.match(line)
            if assign_match and not env_match:
                local_var = assign_match.group("var")
                value = normalize_value(complete_shell_value(line, assign_match.start("value"), assign_match.group("value")))
                env_defaults.setdefault(local_var, ("", value))

            for match in HYDRA_RE.finditer(line):
                param = match.group("key")
                value = normalize_value(complete_shell_value(line, match.start("value"), match.group("value")))
                env_var = None
                var_match = re.fullmatch(r"\$\{([^}]+)\}", value)
                if var_match:
                    local = var_match.group(1)
                    env_var, default = env_defaults.get(local, ("", value))
                    if default:
                        value = default
                add_feature(features, param, value, rel, line_no, line, env_var or None, saw_npu)

            for match in FLAG_RE.finditer(line):
                flag = match.group("flag")
                value = normalize_value(complete_shell_value(line, match.start("value"), match.group("value") or "")) if match.group("value") else ""
                add_feature(features, flag, value, rel, line_no, line, None, saw_npu)

    for feature in features.values():
        feature.saw_ci = feature.parameter.lower() in ci_text or any(Path(s).name.lower() in ci_text for s in feature.scripts)

    dirty = git_value(repo, "status", "--short")
    now = dt.datetime.now().astimezone().isoformat(timespec="seconds")
    rows = []
    for feature in sorted(features.values(), key=lambda f: (-len(f.scripts), f.category, f.parameter)):
        npu = "部分" if feature.saw_npu else "未知"
        if feature.parameter.lower() in {"trainer.device", "device"} and any("npu" in v.lower() for v in feature.values):
            npu = "是"
        ci = "部分" if feature.saw_ci else "未知"
        rows.append(
            {
                "parameter": feature.parameter,
                "category": feature.category,
                "chinese_explanation": explain(feature.parameter),
                "common_values": sorted(feature.values)[:12],
                "source_env_vars": sorted(v for v in feature.env_vars if v)[:12],
                "example_scripts": sorted(feature.scripts)[:20],
                "script_count": len(feature.scripts),
                "hit_count": feature.count,
                "perf_impact": perf_impact(feature.parameter),
                "accuracy_impact": accuracy_impact(feature.parameter),
                "npu_support": npu,
                "ci_watch": ci,
                "evidence": [ev.__dict__ for ev in feature.evidence],
                "list_file": feature_filename(feature.parameter),
            }
        )
    return {
        "schema_version": 3,
        "generated_at": now,
        "repo": str(repo),
        "branch": git_value(repo, "rev-parse", "--abbrev-ref", "HEAD"),
        "commit": git_value(repo, "rev-parse", "--short", "HEAD"),
        "dirty": bool(dirty),
        "dirty_summary": dirty.splitlines()[:20],
        "roots": roots,
        "example_files_scanned": len(files),
        "features": rows,
    }


def md_escape(text: str) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def parse_existing_feature_doc(path: Path) -> dict[str, str]:
    text = read_text(path)
    result: dict[str, str] = {}
    for key, label in (
        ("chinese_explanation", "中文解释"),
        ("perf_impact", "性能影响"),
        ("accuracy_impact", "精度影响"),
    ):
        match = re.search(rf"^- \*\*{label}\*\*[:：]\s*(.+)$", text, re.MULTILINE)
        if match:
            result[key] = match.group(1).strip()
    return result


def row_needs_research(row: dict) -> bool:
    return any(
        str(row[key]).startswith("待补充")
        for key in ("chinese_explanation", "perf_impact", "accuracy_impact")
    )


def has_manual_explanation(fields: dict[str, str]) -> bool:
    return any(value and not value.startswith("待补充") for value in fields.values())


def update_needs_marker(path: Path, needs_research: bool) -> None:
    text = read_text(path)
    if not text:
        return
    desired = f"- **需要子代理补证**：{'是' if needs_research else '否'}"
    if re.search(r"^- \*\*需要子代理补证\*\*[:：].*$", text, re.MULTILINE):
        text = re.sub(r"^- \*\*需要子代理补证\*\*[:：].*$", desired, text, flags=re.MULTILINE)
    else:
        text = text.rstrip() + "\n" + desired + "\n"
    path.write_text(text)


def feature_doc(row: dict) -> str:
    values = "、".join(row["common_values"]) or "未提取"
    env_vars = "、".join(row["source_env_vars"]) or "无"
    scripts = "\n".join(f"- `{script}`" for script in row["example_scripts"][:20]) or "- 未记录"
    evidence = "\n".join(
        f"- `{item['path']}:{item['line']}` {item['text']}"
        for item in row["evidence"][:5]
    ) or "- 未记录"
    needs_research = "是" if row_needs_research(row) else "否"
    return f"""# {row['parameter']}

- **参数名**：`{row['parameter']}`
- **分类**：{row['category']}
- **中文解释**：{row['chinese_explanation']}
- **常见值**：{values}
- **来源环境变量**：{env_vars}
- **性能影响**：{row['perf_impact']}
- **精度影响**：{row['accuracy_impact']}
- **NPU/Ascend 证据**：{row['npu_support']}
- **CI 看护**：{row['ci_watch']}
- **示例数**：{row['script_count']}
- **需要子代理补证**：{needs_research}

## 示例脚本

{scripts}

## 证据片段

{evidence}

## 子代理补证要求

如果 `需要子代理补证` 为“是”，子代理应先搜索 `docs/verl/features/lists/` 中是否已有同名解释文件；若没有或内容仍是占位符，再联网搜索 Verl 官方文档，并搜索目标 Verl 仓的 `docs/`，最后回写本文件。
"""


def apply_feature_docs(rows: list[dict], lists_dir: Path) -> list[str]:
    lists_dir.mkdir(parents=True, exist_ok=True)
    needs_research = []
    for row in rows:
        path = lists_dir / row["list_file"]
        existing = parse_existing_feature_doc(path) if path.exists() else {}
        for key, value in existing.items():
            if value and not value.startswith("待补充"):
                row[key] = value
        needs = row_needs_research(row)
        if needs:
            needs_research.append(row["parameter"])
        if path.exists() and has_manual_explanation(existing):
            update_needs_marker(path, needs)
        else:
            path.write_text(feature_doc(row))
    return needs_research


def markdown(data: dict, limit: int) -> str:
    features = data["features"]
    category_counts: dict[str, int] = {}
    for row in features:
        category_counts[row["category"]] = category_counts.get(row["category"], 0) + 1

    lines = [
        f"# Verl examples 参数特性报告 {data['generated_at'][:10]}",
        "",
        "## 扫描对象",
        "",
        f"- 仓库：`{data['repo']}`",
        f"- 分支/提交：`{data['branch']}` / `{data['commit']}`",
        f"- 工作区 dirty：`{data['dirty']}`",
        f"- 扫描根目录：`{', '.join(data['roots'])}`",
        f"- 扫描 examples 文件数：`{data['example_files_scanned']}`",
        f"- 参数特性数：`{len(features)}`",
        "",
        "## 参数总览",
        "",
        "| 分类 | 参数数 |",
        "|---|---:|",
    ]
    for category, count in sorted(category_counts.items(), key=lambda item: (-item[1], item[0])):
        lines.append(f"| {category} | {count} |")

    lines.extend([
        "",
        "## Top 参数特性",
        "",
        "| 参数 | 分类 | 中文解释 | 常见值 | 性能影响 | 精度影响 | 示例数 |",
        "|---|---|---|---|---|---|---:|",
    ])
    for row in features[:limit]:
        values = ", ".join(row["common_values"][:4]) or "未提取"
        lines.append(
            "| {parameter} | {category} | {explain} | {values} | {perf} | {acc} | {count} |".format(
                parameter=md_escape(row["parameter"]),
                category=row["category"],
                explain=md_escape(row["chinese_explanation"]),
                values=md_escape(values),
                perf=md_escape(row["perf_impact"]),
                acc=md_escape(row["accuracy_impact"]),
                count=row["script_count"],
            )
        )

    lines.extend([
        "",
        "## 输出文件",
        "",
        "- `process/example-parameter-features.json`：扫描过程与全量结构化结果。",
        "- `process/example-parameter-features.md`：本报告。",
        "- `lists/*.md`：每个参数的同名解释文件。",
        "- `verl-example-parameters.xlsx`：最终 Excel 汇总。",
    ])
    return "\n".join(lines) + "\n"


def excel_col(index: int) -> str:
    name = ""
    while index:
        index, rem = divmod(index - 1, 26)
        name = chr(65 + rem) + name
    return name


def sheet_xml(rows: list[list[str]]) -> str:
    out = ['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>']
    out.append('<worksheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><sheetData>')
    for r_idx, row in enumerate(rows, start=1):
        out.append(f'<row r="{r_idx}">')
        for c_idx, value in enumerate(row, start=1):
            ref = f"{excel_col(c_idx)}{r_idx}"
            out.append(f'<c r="{ref}" t="inlineStr"><is><t>{escape(str(value))}</t></is></c>')
        out.append("</row>")
    out.append("</sheetData></worksheet>")
    return "".join(out)


def write_xlsx(path: Path, rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        zf.writestr("[Content_Types].xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
</Types>""")
        zf.writestr("_rels/.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
</Relationships>""")
        zf.writestr("xl/workbook.xml", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets><sheet name="verl参数特性" sheetId="1" r:id="rId1"/></sheets>
</workbook>""")
        zf.writestr("xl/_rels/workbook.xml.rels", """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
</Relationships>""")
        zf.writestr("xl/worksheets/sheet1.xml", sheet_xml(rows))


def write_outputs(data: dict, out_dir: Path, limit: int) -> dict[str, Path]:
    process_dir = out_dir / "process"
    lists_dir = out_dir / "lists"
    process_dir.mkdir(parents=True, exist_ok=True)
    lists_dir.mkdir(parents=True, exist_ok=True)

    needs_research = apply_feature_docs(data["features"], lists_dir)
    report = markdown(data, limit)

    json_path = process_dir / "example-parameter-features.json"
    md_path = process_dir / "example-parameter-features.md"
    needs_path = process_dir / "needs-research.txt"
    excel_path = out_dir / "verl-example-parameters.xlsx"

    json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    md_path.write_text(report)
    needs_path.write_text("\n".join(needs_research) + ("\n" if needs_research else ""))

    excel_rows = [EXCEL_COLUMNS]
    for row in data["features"]:
        excel_rows.append(
            [
                row["parameter"],
                row["category"],
                row["chinese_explanation"],
                "；".join(row["common_values"]),
                row["perf_impact"],
                row["accuracy_impact"],
                str(row["script_count"]),
            ]
        )
    write_xlsx(excel_path, excel_rows)
    return {
        "json": json_path,
        "markdown": md_path,
        "needs_research": needs_path,
        "excel": excel_path,
        "lists_dir": lists_dir,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="扫描 Verl examples 参数特性，生成解释库和 Excel。")
    parser.add_argument("--repo", required=True, help="Verl 仓路径")
    parser.add_argument("--out", default="docs/verl/features", help="输出目录，默认 docs/verl/features")
    parser.add_argument("--roots", default="examples", help="逗号分隔扫描根目录，默认 examples")
    parser.add_argument("--limit", type=int, default=80, help="Markdown Top 表行数")
    args = parser.parse_args()

    repo = Path(args.repo).expanduser().resolve()
    if not repo.exists():
        raise SystemExit(f"仓库不存在：{repo}")
    roots = [item.strip() for item in args.roots.split(",") if item.strip()]
    out_dir = Path(args.out).expanduser()
    if not out_dir.is_absolute():
        out_dir = Path.cwd() / out_dir
    out_dir = out_dir.resolve()

    data = scan(repo, roots)
    paths = write_outputs(data, out_dir, args.limit)
    for path in paths.values():
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
