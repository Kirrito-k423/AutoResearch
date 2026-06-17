# -*- coding: utf-8 -*-
"""Generate the AutoResearch architecture diagram as an SVG."""

from pathlib import Path

W, H = 2000, 1580
OUT = Path(__file__).with_name("autoresearch_arch.svg")

BG = "#F6F8FB"
TITLE_BG_A = "#1E3A8A"
TITLE_BG_B = "#3B82F6"

YELLOW_FILL = "#FEF3C7"
YELLOW_LINE = "#F59E0B"
YELLOW_TEXT = "#92400E"

BLUE_FILL = "#DBEAFE"
BLUE_LINE = "#3B82F6"
BLUE_TEXT = "#1E3A8A"

CARD_FILL = "#FFFFFF"
CARD_LINE = "#93C5FD"
CARD_TEXT = "#1F2937"

SUB_FILL = "#EFF6FF"
SUB_LINE = "#60A5FA"
SUB_TEXT = "#1E40AF"

GRAY_FILL = "#F1F5F9"
GRAY_LINE = "#94A3B8"
GRAY_TEXT = "#0F172A"

PINK_FILL = "#FEE2E2"
PINK_LINE = "#EF4444"
PINK_TEXT = "#991B1B"

ORANGE_FILL = "#FFEDD5"
ORANGE_LINE = "#F97316"
ORANGE_TEXT = "#9A3412"

GREEN_FILL = "#D1FAE5"
GREEN_LINE = "#10B981"
GREEN_TEXT = "#065F46"

ARROW = "#475569"
ARROW_SOFT = "#94A3B8"

FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC',sans-serif"

parts: list[str] = []


def add(svg: str) -> None:
    parts.append(svg)


def esc(value: str) -> str:
    return value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str = CARD_FILL,
    stroke: str = CARD_LINE,
    rx: float = 10,
    ry: float | None = None,
    sw: float = 1.4,
    opacity: float = 1.0,
    dash: str | None = None,
    extra: str = "",
) -> str:
    ry = rx if ry is None else ry
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{ry}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"{dash_attr}{extra}/>'
    )


def text(
    x: float,
    y: float,
    value: str,
    *,
    size: int = 12,
    color: str = CARD_TEXT,
    anchor: str = "middle",
    weight: int = 400,
    line_height: int | None = None,
    extra: str = "",
) -> str:
    line_height = line_height or size + 4
    lines = value.split("\n")
    return "\n".join(
        f'<text x="{x}" y="{y + i * line_height}" font-family="{FONT}" font-size="{size}" '
        f'fill="{color}" text-anchor="{anchor}" font-weight="{weight}"{extra}>{esc(line)}</text>'
        for i, line in enumerate(lines)
    )


def pill(
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    *,
    fill: str = SUB_FILL,
    stroke: str = SUB_LINE,
    color: str = SUB_TEXT,
    size: int = 10,
    weight: int = 700,
    rx: float = 4,
) -> str:
    return "\n".join(
        [
            rect(x, y, w, h, fill=fill, stroke=stroke, rx=rx, sw=1.0),
            text(x + w / 2, y + h / 2 + size / 2 - 1, label, size=size, color=color, weight=weight),
        ]
    )


def section_title(x: float, y: float, title: str, *, color: str = BLUE_TEXT) -> str:
    return text(x, y, f"▎{title}", size=12, color=color, anchor="start", weight=700)


def skill_card(
    x: float,
    y: float,
    w: float,
    h: float,
    name: str,
    desc_lines: list[str] | None = None,
    *,
    status: str = "solid",
    accent: str = SUB_LINE,
    accent_fill: str = SUB_FILL,
) -> str:
    desc_lines = desc_lines or []
    dashed = status == "dashed"
    out = [
        rect(
            x,
            y,
            w,
            h,
            fill=DASH_FILL if dashed else CARD_FILL,
            stroke=DASH_LINE if dashed else accent,
            sw=1.2,
            dash="4 3" if dashed else None,
        ),
        rect(x + 10, y + 10, 44, 16, fill=accent_fill, stroke=accent, sw=0.8, rx=3),
        text(x + 32, y + 22, "SKILL", size=9, color=accent, weight=700),
        text(x + w / 2, y + 48, name, size=11, color=CARD_TEXT, weight=700),
    ]
    for index, line in enumerate(desc_lines[:3]):
        out.append(text(x + w / 2, y + 66 + index * 14, line, size=9, color="#475569"))
    return "\n".join(out)


def small_card(
    x: float,
    y: float,
    w: float,
    h: float,
    title: str,
    subtitle: str | None = None,
    *,
    fill: str = CARD_FILL,
    stroke: str = SUB_LINE,
    title_color: str = BLUE_TEXT,
) -> str:
    out = [
        rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.0),
        text(x + w / 2, y + h / 2 - (2 if subtitle else -4), title, size=11, color=title_color, weight=700),
    ]
    if subtitle:
        out.append(text(x + w / 2, y + h / 2 + 16, subtitle, size=9, color="#475569"))
    return "\n".join(out)


def path(
    d: str,
    *,
    color: str = ARROW,
    sw: float = 1.4,
    dashed: bool = False,
    marker: str = "arrowSlate",
    opacity: float = 1.0,
) -> str:
    dash = ' stroke-dasharray="5 4"' if dashed else ""
    marker_attr = f' marker-end="url(#{marker})"' if marker else ""
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{sw}" opacity="{opacity}"'
        f'{dash}{marker_attr}/>'
    )


def line_arrow(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    *,
    color: str = ARROW,
    sw: float = 1.4,
    dashed: bool = False,
    marker: str = "arrowSlate",
) -> str:
    return path(f"M{x1},{y1} L{x2},{y2}", color=color, sw=sw, dashed=dashed, marker=marker)


def route(
    points: list[tuple[float, float]],
    *,
    color: str = ARROW,
    sw: float = 1.4,
    dashed: bool = False,
    marker: str = "arrowSlate",
) -> str:
    first, *rest = points
    commands = [f"M{first[0]},{first[1]}"] + [f"L{x},{y}" for x, y in rest]
    return path(" ".join(commands), color=color, sw=sw, dashed=dashed, marker=marker)


DASH_FILL = CARD_FILL
DASH_LINE = SUB_LINE


add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add("<defs>")
add('  <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">')
add(f'    <stop offset="0%" stop-color="{TITLE_BG_A}"/>')
add(f'    <stop offset="100%" stop-color="{TITLE_BG_B}"/>')
add("  </linearGradient>")
add('  <linearGradient id="pinkGrad" x1="0" y1="0" x2="0" y2="1">')
add('    <stop offset="0%" stop-color="#FEE2E2"/>')
add('    <stop offset="100%" stop-color="#FECACA"/>')
add("  </linearGradient>")
for marker_id, color in [
    ("arrowSlate", ARROW),
    ("arrowBlue", BLUE_LINE),
    ("arrowGreen", GREEN_LINE),
    ("arrowOrange", ORANGE_LINE),
    ("arrowSoft", ARROW_SOFT),
]:
    add(
        f'  <marker id="{marker_id}" viewBox="0 0 10 10" refX="8.6" refY="5" '
        f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
    )
    add(f'    <path d="M0,0 L10,5 L0,10 z" fill="{color}"/>')
    add("  </marker>")
add("</defs>")

add(rect(0, 0, W, H, fill=BG, stroke="none", sw=0, rx=0))
add(rect(0, 0, W, 70, fill="url(#titleGrad)", stroke="none", sw=0, rx=0))
add(text(W / 2, 30, "AutoResearch · 自驱式训练 & 调试系统架构", size=21, color="#FFFFFF", weight=700))
add(text(W / 2, 54, "数据 / 代码 / 评测 / 决策 一体化 · Cline + GLM-5 + wandb", size=12, color="#DBEAFE"))

# Three clean lanes. Arrows between lanes stay in the gutters.
MAIN_X, MAIN_W = 120, 720
PI_X, PI_W = 910, 340
DATA_X, DATA_W = 1320, 560
MAIN_C = MAIN_X + MAIN_W / 2
PI_C = PI_X + PI_W / 2
DATA_C = DATA_X + DATA_W / 2

HDR_Y = 98
add(text(MAIN_C, HDR_Y, "① 主工作区 · 模型与训练链路", size=14, color=BLUE_TEXT, weight=700))
add(text(PI_C, HDR_Y, "② PI Agent · 智能体层", size=14, color="#334155", weight=700))
add(text(DATA_C, HDR_Y, "③ 数据湖 · 记忆与决策", size=14, color=GREEN_TEXT, weight=700))

# Top inputs.
TOP_Y = 120
GH_X, GH_W = MAIN_X, 170
ENV_X, ENV_W = MAIN_X + 220, MAIN_W - 220
ART_X, ART_W = DATA_X, DATA_W

add(rect(GH_X, TOP_Y, GH_W, 84, fill=GRAY_FILL, stroke=GRAY_LINE, sw=1.2))
add(text(GH_X + GH_W / 2, TOP_Y + 30, "GitHub 私仓", size=13, color=GRAY_TEXT, weight=700))
add(text(GH_X + GH_W / 2, TOP_Y + 52, "代码备份 / 同步", size=10, color="#475569", weight=600))

add(rect(ENV_X, TOP_Y, ENV_W, 108, fill=YELLOW_FILL, stroke=YELLOW_LINE, sw=1.5))
add(text(ENV_X + 24, TOP_Y + 28, "黄区虚拟环境", size=15, color=YELLOW_TEXT, anchor="start", weight=700))
add(text(ENV_X + 24, TOP_Y + 52, "venv / docker 隔离运行容器", size=11, color="#78350F", anchor="start"))
add(text(ENV_X + 24, TOP_Y + 72, "镜像内置 verl + 训练脚本", size=11, color="#78350F", anchor="start"))
add(text(ENV_X + 24, TOP_Y + 92, "提供端到端一致的执行底座", size=11, color="#78350F", anchor="start"))

add(rect(ART_X, TOP_Y, ART_W, 108, fill=YELLOW_FILL, stroke=YELLOW_LINE, sw=1.5))
add(text(ART_X + 24, TOP_Y + 28, "运行日志 & Debug 数据", size=15, color=YELLOW_TEXT, anchor="start", weight=700))
add(text(ART_X + 24, TOP_Y + 52, "训练运行 log（成功 / 失败）", size=11, color="#78350F", anchor="start"))
add(text(ART_X + 24, TOP_Y + 72, "profiling · 内存快照", size=11, color="#78350F", anchor="start"))
add(text(ART_X + 24, TOP_Y + 92, "plog / debug info / artifact", size=11, color="#78350F", anchor="start"))
add(pill(ART_X + ART_W - 120, TOP_Y + 18, 88, 22, "数据备份", fill=CARD_FILL, stroke=YELLOW_LINE, color=YELLOW_TEXT))

add(line_arrow(GH_X + GH_W + 10, TOP_Y + 42, ENV_X - 12, TOP_Y + 42, sw=1.2))
add(text(GH_X + GH_W + 85, TOP_Y + 32, "拉取", size=10, color="#475569", weight=600))

# Main workspace column.
DFX_Y, DFX_H = 260, 135
add(rect(MAIN_X, DFX_Y, MAIN_W, DFX_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MAIN_X + 18, DFX_Y + 24, "verl-DFX · 训练/推理能力底座", size=14, color=BLUE_TEXT, anchor="start", weight=700))
add(rect(MAIN_X + 24, DFX_Y + 48, 140, 70, fill=CARD_FILL, stroke=CARD_LINE, sw=1.2))
add(text(MAIN_X + 94, DFX_Y + 75, "putils", size=12, color=BLUE_TEXT, weight=700))
add(text(MAIN_X + 94, DFX_Y + 96, "工具集 / Path Util", size=10, color="#475569"))

REPO_X = MAIN_X + 186
REPO_W = MAIN_W - 210
add(rect(REPO_X, DFX_Y + 48, REPO_W, 70, fill=SUB_FILL, stroke=SUB_LINE, sw=1.0))
add(text(REPO_X + REPO_W / 2, DFX_Y + 68, "verl 原仓（verl 原生能力 · mode=x 切换）", size=11, color=SUB_TEXT, weight=700))
tool_w = (REPO_W - 46) / 4
for index, label in enumerate(["FSDP", "x-bridge", "vllm", "sglang…"]):
    bx = REPO_X + 14 + index * (tool_w + 6)
    add(small_card(bx, DFX_Y + 82, tool_w, 28, label, stroke=SUB_LINE, title_color=BLUE_TEXT))

MODE_Y = DFX_Y + DFX_H + 16
add(rect(MAIN_C - 190, MODE_Y, 380, 26, fill=CARD_FILL, stroke="#CBD5E1", sw=0.8, rx=5))
add(text(MAIN_C, MODE_Y + 17, "通过 mode=x 使能不同 skill 与场景代码", size=10, color="#475569", weight=600))
add(line_arrow(MAIN_C, DFX_Y + DFX_H, MAIN_C, MODE_Y - 2, sw=1.1, marker="arrowSoft", color=ARROW_SOFT))

ADAP_Y, ADAP_H = 450, 245
add(line_arrow(MAIN_C, MODE_Y + 28, MAIN_C, ADAP_Y - 8, sw=1.2))
add(rect(MAIN_X, ADAP_Y, MAIN_W, ADAP_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MAIN_X + 18, ADAP_Y + 24, "workspace-adapter · 场景经验 / 治理与约束", size=14, color=BLUE_TEXT, anchor="start", weight=700))
add(text(MAIN_X + MAIN_W - 18, ADAP_Y + 24, "对接 DFX · 训练全流程 Skill 集", size=11, color="#475569", anchor="end", weight=500))

skill_data = [
    ("环境搭建 (verl)", ["沉淀脚本 / JSON", "验收条件自检"]),
    ("verl-env-doctor", ["代理 · NPU", "CANN · torch_npu", "Ray · 数据集"]),
    ("任务运行", ["拉起训练任务", "收集过程数据"]),
    ("性能采集", ["推理 & 训练", "指标 · timeline"]),
    ("显存采集", ["峰值 · 曲线", "OOM 风险提示"]),
    ("下游评测", ["任务级指标", "结果回写"]),
    ("训练一致性分析", ["对比多 run", "偏差定位"]),
    ("自动分析", ["异常归因", "建议方案"]),
]
SK_GAP = 10
SK_W = (MAIN_W - 36 - SK_GAP * 3) / 4
for index, (name, desc) in enumerate(skill_data[:4]):
    sx = MAIN_X + 18 + index * (SK_W + SK_GAP)
    add(skill_card(sx, ADAP_Y + 48, SK_W, 82, name, desc))
for index, (name, desc) in enumerate(skill_data[4:]):
    sx = MAIN_X + 18 + index * (SK_W + SK_GAP)
    add(skill_card(sx, ADAP_Y + 140, SK_W, 82, name, desc, status="dashed", accent=SUB_LINE, accent_fill=CARD_FILL))

WC_Y, WC_H = 730, 360
add(line_arrow(MAIN_C, ADAP_Y + ADAP_H + 4, MAIN_C, WC_Y - 8, sw=1.2))
add(rect(MAIN_X, WC_Y, MAIN_W, WC_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MAIN_X + 18, WC_Y + 24, "workspace-core · 工具接口与协议", size=14, color=BLUE_TEXT, anchor="start", weight=700))
add(text(MAIN_X + MAIN_W - 18, WC_Y + 24, "统一的 Skill 容器 / Session 编排", size=11, color="#475569", anchor="end", weight=500))

AREA_X, AREA_Y = MAIN_X + 18, WC_Y + 50
AREA_W = MAIN_W - 36
SUB_W = (AREA_W - 18) / 2
SUB_H = 124

core_sections = [
    ("执行环境与沙箱", [("园区网络", "配置管理"), ("环境搭建", "数据库"), ("远程连接", "SSH / 隧道")]),
    ("工具接口与协议", [("执行", "会话上下文"), ("性能采集", "有限大小"), ("显存采集", "OOM 提示")]),
    ("可观测性", [("对比可视化", "生成图表"), ("关键信息提取", "字段抽取")]),
    ("生命周期与编排", [("自动研究", "启动 / 成功 / 失败"), ("重启收敛", "状态推进")]),
]
for index, (title, cards) in enumerate(core_sections):
    col = index % 2
    row = index // 2
    sx = AREA_X + col * (SUB_W + 18)
    sy = AREA_Y + row * (SUB_H + 18)
    add(rect(sx, sy, SUB_W, SUB_H, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
    add(section_title(sx + 12, sy + 20, title))
    card_gap = 8
    card_w = (SUB_W - 24 - card_gap * (len(cards) - 1)) / len(cards)
    for card_index, (title_text, sub_text) in enumerate(cards):
        cx = sx + 12 + card_index * (card_w + card_gap)
        add(small_card(cx, sy + 44, card_w, 54, title_text, sub_text))

HOOK_Y = WC_Y + WC_H - 54
add(rect(MAIN_X + 34, HOOK_Y, MAIN_W - 68, 30, fill=GREEN_FILL, stroke=GREEN_LINE, sw=1.0, rx=5))
add(text(MAIN_C, HOOK_Y + 20, "沉淀 / 脚本 / 验收条件（前置 hook / 后置 hook 实现）", size=11, color=GREEN_TEXT, weight=600))

RS_Y, RS_H = 1110, 62
add(line_arrow(MAIN_C, WC_Y + WC_H + 4, MAIN_C, RS_Y - 8, sw=1.2))
add(rect(MAIN_X, RS_Y, MAIN_W, RS_H, fill=CARD_FILL, stroke=BLUE_LINE, sw=1.5, rx=8))
add(pill(MAIN_X + 18, RS_Y + 14, 120, 20, "Run / Session 层", fill=BLUE_FILL, stroke=BLUE_LINE, color=BLUE_TEXT))
add(text(MAIN_C + 60, RS_Y + 26, "日志 / 进程 / 资源 lease / 远程同步", size=11, color="#475569", weight=600))
add(text(MAIN_C + 60, RS_Y + 44, "为上层 PI Agent 提供可复现的执行环境", size=10, color="#64748B"))

# PI Agent column.
PI_TOP_Y, PI_HDR_H = 260, 92
add(rect(PI_X, PI_TOP_Y, PI_W, PI_HDR_H, fill=GRAY_FILL, stroke=GRAY_LINE, sw=1.4))
add(text(PI_X + 18, PI_TOP_Y + 24, "Agent 引擎", size=13, color=GRAY_TEXT, anchor="start", weight=700))
add(pill(PI_X + 18, PI_TOP_Y + 42, 64, 20, "工具层", fill=CARD_FILL, stroke=GRAY_LINE, color=GRAY_TEXT))
add(text(PI_X + 94, PI_TOP_Y + 56, "Cline", size=11, color="#334155", anchor="start", weight=600))
add(pill(PI_X + 170, PI_TOP_Y + 42, 64, 20, "模型层", fill=CARD_FILL, stroke=GRAY_LINE, color=GRAY_TEXT))
add(text(PI_X + 246, PI_TOP_Y + 56, "GLM-5", size=11, color="#334155", anchor="start", weight=600))
add(pill(PI_X + 18, PI_TOP_Y + 66, 130, 18, "生命周期与编排", fill=PINK_FILL, stroke=PINK_LINE, color=PINK_TEXT, size=9))

PI_CORE_Y, PI_CORE_H = 376, 130
add(line_arrow(PI_C, PI_TOP_Y + PI_HDR_H + 4, PI_C, PI_CORE_Y - 8, sw=1.2, marker="arrowSoft", color=ARROW_SOFT))
add(rect(PI_X, PI_CORE_Y, PI_W, PI_CORE_H, fill=CARD_FILL, stroke=BLUE_LINE, sw=2.0, rx=14))
add(text(PI_C, PI_CORE_Y + 38, "PI Agent", size=21, color=BLUE_TEXT, weight=800))
add(text(PI_C, PI_CORE_Y + 65, "Oh-My-Pi", size=14, color=SUB_TEXT, weight=700))
add(text(PI_C, PI_CORE_Y + 94, "阅读理解代码 · 修复 Bug · 开关特性", size=10, color="#475569"))
add(text(PI_C, PI_CORE_Y + 112, "任务 → 决策 → 行动 → 复盘", size=10, color="#475569", weight=600))

WF_Y, WF_H = 532, 320
add(line_arrow(PI_C, PI_CORE_Y + PI_CORE_H + 4, PI_C, WF_Y - 8, sw=1.2, marker="arrowSoft", color=ARROW_SOFT))
add(rect(PI_X, WF_Y, PI_W, WF_H, fill=GRAY_FILL, stroke=GRAY_LINE, sw=1.2))
add(section_title(PI_X + 14, WF_Y + 22, "核心工作循环", color=GRAY_TEXT))
loop = [
    ("#1", "测试运行"),
    ("#2", "读取日志"),
    ("#3", "分析报告"),
    ("#4", "分析代码"),
    ("#5", "修改代码"),
    ("#6", "目标收敛"),
]
LOOP_W = (PI_W - 42) / 2
for index, (num, name) in enumerate(loop):
    col = index % 2
    row = index // 2
    bx = PI_X + 14 + col * (LOOP_W + 14)
    by = WF_Y + 52 + row * 76
    add(rect(bx, by, LOOP_W, 56, fill=CARD_FILL, stroke=GRAY_LINE, sw=1.1, rx=7))
    add(pill(bx + 12, by + 10, 42, 16, num, fill="#E2E8F0", stroke=GRAY_LINE, color=GRAY_TEXT, size=9, rx=3))
    add(text(bx + LOOP_W / 2 + 22, by + 35, name, size=11, color=CARD_TEXT, weight=700))

add(rect(PI_X, WF_Y + WF_H + 24, PI_W, 105, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(section_title(PI_X + 14, WF_Y + WF_H + 46, "约束与输出"))
add(text(PI_X + 24, WF_Y + WF_H + 72, "遵循 skills 规格", size=11, color="#475569", anchor="start", weight=600))
add(text(PI_X + 24, WF_Y + WF_H + 94, "维护数据信息", size=11, color="#475569", anchor="start", weight=600))
add(text(PI_X + 24, WF_Y + WF_H + 116, "把结论写回报告 / Registry", size=11, color="#475569", anchor="start", weight=600))

# Cross-lane relationships placed in gutters.
add(text(875, WC_Y + 120, "遵循与消化", size=10, color="#475569", anchor="middle", weight=600))
add(path(f"M{PI_X - 26},{WC_Y + 45} C{PI_X - 54},{WC_Y + 120} {PI_X - 54},{WC_Y + 250} {PI_X - 26},{WC_Y + 315}", color=ARROW_SOFT, sw=1.2, marker="arrowSoft"))

ARROW_Y = WF_Y + 155
add(text((PI_X + PI_W + DATA_X) / 2, ARROW_Y - 12, "观察 / 记忆 / 建议", size=10, color="#475569", weight=600))
add(route([(PI_X + PI_W + 8, ARROW_Y), (DATA_X - 12, ARROW_Y)], sw=1.2))

RS_LINK_Y = RS_Y + RS_H / 2
add(text((MAIN_X + MAIN_W + PI_X) / 2, RS_LINK_Y - 14, "执行反馈", size=10, color="#475569", weight=600))
add(route([(MAIN_X + MAIN_W + 8, RS_LINK_Y), (PI_X - 12, RS_LINK_Y)], sw=1.2, marker="arrowSoft", color=ARROW_SOFT))

# Data lake column.
WB_Y, WB_HDR_H = 260, 40
add(line_arrow(DATA_C, TOP_Y + 108 + 8, DATA_C, WB_Y - 10, sw=1.2, marker="arrowSoft", color=ARROW_SOFT))
add(rect(DATA_X, WB_Y, DATA_W, WB_HDR_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.4))
add(text(DATA_C, WB_Y + 26, "wandb / 数据湖 · 上下文 & 记忆管理", size=14, color=BLUE_TEXT, weight=700))

RAW_Y, RAW_H = 318, 105
add(rect(DATA_X, RAW_Y, DATA_W, RAW_H, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(section_title(DATA_X + 14, RAW_Y + 23, "原始数据"))
raw_cards = [("运行 log", "成功 / 失败"), ("profiling", "性能画像"), ("历史会话", "上下文回放")]
RAW_W = (DATA_W - 44) / 3
for index, (title_text, sub_text) in enumerate(raw_cards):
    bx = DATA_X + 14 + index * (RAW_W + 8)
    add(small_card(bx, RAW_Y + 44, RAW_W, 48, title_text, sub_text))

KP_Y, KP_H = 444, 112
add(line_arrow(DATA_C, RAW_Y + RAW_H + 4, DATA_C, KP_Y - 8, sw=1.1, marker="arrowSoft", color=ARROW_SOFT))
add(rect(DATA_X, KP_Y, DATA_W, KP_H, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(section_title(DATA_X + 14, KP_Y + 23, "关键字段解析 & 预处理"))
KP_W = (DATA_W - 36) / 2
for index, (title_text, sub_text) in enumerate(
    [("采集信息 + 初步建议", "性能 · 内存 · 精度 · 效果"), ("脚本提取", "可复现的最小步骤")]
):
    bx = DATA_X + 14 + index * (KP_W + 8)
    add(small_card(bx, KP_Y + 46, KP_W, 50, title_text, sub_text))
add(path(f"M{DATA_X + DATA_W - 90},{KP_Y + KP_H - 8} L{DATA_X + 90},{KP_Y + KP_H - 8}", color=ORANGE_LINE, sw=1.2, marker="arrowOrange"))

REG_Y, REG_H = 578, 64
add(line_arrow(DATA_C, KP_Y + KP_H + 4, DATA_C, REG_Y - 8, sw=1.1, marker="arrowSoft", color=ARROW_SOFT))
add(rect(DATA_X, REG_Y, DATA_W, REG_H, fill="url(#pinkGrad)", stroke=PINK_LINE, sw=1.6, rx=8))
add(pill(DATA_X + 16, REG_Y + 16, 142, 20, "Experiment Registry", fill=CARD_FILL, stroke=PINK_LINE, color=PINK_TEXT, size=10))
add(text(DATA_X + DATA_W - 20, REG_Y + 38, "实验进度表 · 长期记忆 · 指导任务下一步", size=11, color=PINK_TEXT, anchor="end", weight=600))

RP_Y, RP_H = 666, 128
add(line_arrow(DATA_C, REG_Y + REG_H + 4, DATA_C, RP_Y - 8, sw=1.1, marker="arrowSoft", color=ARROW_SOFT))
add(rect(DATA_X, RP_Y, DATA_W, RP_H, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(section_title(DATA_X + 14, RP_Y + 23, "报告（LLM 可读 md）"))
LLM_X, LLM_Y, LLM_W, LLM_H = DATA_X + DATA_W - 128, RP_Y + 46, 92, 58
add(rect(LLM_X, LLM_Y, LLM_W, LLM_H, fill=CARD_FILL, stroke=SUB_LINE, sw=1.2, dash="4 3"))
add(text(LLM_X + LLM_W / 2, LLM_Y + 24, "LLM", size=12, color=SUB_TEXT, weight=700))
add(text(LLM_X + LLM_W / 2, LLM_Y + 43, "分析", size=12, color=SUB_TEXT, weight=700))
OUT_X, OUT_W = DATA_X + 18, LLM_X - DATA_X - 48
add(small_card(OUT_X, LLM_Y + 2, OUT_W, 24, "md 分析报告（AI 交互）", stroke=SUB_LINE, title_color=CARD_TEXT))
add(small_card(OUT_X, LLM_Y + 34, OUT_W, 24, "自动研究进度", stroke=SUB_LINE, title_color=CARD_TEXT))
add(route([(LLM_X - 8, LLM_Y + 22), (OUT_X + OUT_W + 10, LLM_Y + 14)], sw=1.0))
add(route([(LLM_X - 8, LLM_Y + 42), (OUT_X + OUT_W + 10, LLM_Y + 46)], sw=1.0))

MEM_Y, MEM_H = 826, 118
add(line_arrow(DATA_C, RP_Y + RP_H + 4, DATA_C, MEM_Y - 8, sw=1.1, marker="arrowSoft", color=ARROW_SOFT))
add(rect(DATA_X, MEM_Y, DATA_W, MEM_H, fill=GREEN_FILL, stroke=GREEN_LINE, sw=1.2))
add(section_title(DATA_X + 14, MEM_Y + 25, "长期沉淀", color=GREEN_TEXT))
MEM_W = (DATA_W - 44) / 3
for index, (title_text, sub_text) in enumerate(
    [("实验轨迹", "版本 / 参数"), ("评测结果", "指标 / 对比"), ("上下文索引", "可回放")]
):
    bx = DATA_X + 14 + index * (MEM_W + 8)
    add(small_card(bx, MEM_Y + 50, MEM_W, 48, title_text, sub_text, stroke=GREEN_LINE, title_color=GREEN_TEXT))

# Dashboards.
DB_Y, DB_H = 1228, 118
DB_W = (DATA_X + DATA_W - MAIN_X - 40) / 3
dashboards = [
    ("任务进度看板", "监控各阶段流程的拆解与完成情况\n参考 AgentHub", BLUE_FILL, BLUE_LINE, BLUE_TEXT),
    ("数据指标分析看板", "wandb 集成：loss / acc / 吞吐\n指标趋势 / 异常告警", GREEN_FILL, GREEN_LINE, GREEN_TEXT),
    ("运行时资源看板", "Prometheus + Grafana\nGPU / 内存 / 网络 / 队列", ORANGE_FILL, ORANGE_LINE, ORANGE_TEXT),
]
for index, (title_text, body, fill, stroke, color) in enumerate(dashboards):
    bx = MAIN_X + index * (DB_W + 20)
    add(rect(bx, DB_Y, DB_W, DB_H, fill=fill, stroke=stroke, sw=1.5))
    add(text(bx + DB_W / 2, DB_Y + 34, title_text, size=15, color=color, weight=700))
    add(text(bx + DB_W / 2, DB_Y + 68, body, size=12, color=CARD_TEXT, weight=500, line_height=18))

add(text(DATA_C, DB_Y - 18, "可视化 · 全过程监控", size=10, color=GREEN_TEXT, weight=600))
add(route([(DATA_C, MEM_Y + MEM_H + 8), (DATA_C, DB_Y - 26)], color=GREEN_LINE, sw=1.2, dashed=True, marker="arrowGreen"))

# Footer controls.
FT_Y, FT_H = 1380, 86
AUTO_X, AUTO_W = MAIN_X, 520
DEV_W, DEV_X = 520, DATA_X + DATA_W - 520
add(rect(AUTO_X, FT_Y, AUTO_W, FT_H, fill=CARD_FILL, stroke=BLUE_LINE, sw=1.6))
add(pill(AUTO_X + 18, FT_Y + 14, 104, 22, "自动研究", fill=BLUE_FILL, stroke=BLUE_LINE, color=BLUE_TEXT, size=11))
add(text(AUTO_X + AUTO_W / 2 + 28, FT_Y + 35, "定时任务 + 提示词", size=10, color="#475569", weight=600))
add(text(AUTO_X + AUTO_W / 2 + 28, FT_Y + 56, "任务队列 → 生成提议 → 创建 session → 调用技能", size=10, color=CARD_TEXT))
add(text(AUTO_X + AUTO_W / 2 + 28, FT_Y + 72, "跑训练 → 生成简报", size=10, color=CARD_TEXT))

add(rect(DEV_X, FT_Y, DEV_W, FT_H, fill=CARD_FILL, stroke=GREEN_LINE, sw=1.6))
add(pill(DEV_X + 18, FT_Y + 14, 104, 22, "开发人员", fill=GREEN_FILL, stroke=GREEN_LINE, color=GREEN_TEXT, size=11))
add(text(DEV_X + DEV_W / 2 + 28, FT_Y + 43, "需求评审 · 异常介入 · 验收", size=12, color=CARD_TEXT, weight=600))
add(text(DEV_X + DEV_W / 2 + 28, FT_Y + 64, "查看看板 · 决策干预", size=10, color="#475569"))

add(text(W / 2, FT_Y + 28, "人工反馈", size=10, color="#475569", weight=600))
add(route([(DEV_X - 16, FT_Y + FT_H / 2), (AUTO_X + AUTO_W + 16, FT_Y + FT_H / 2)], sw=1.2))

DISPATCH_X = MAIN_X - 44
DISPATCH_Y = RS_Y + RS_H / 2
add(text(DISPATCH_X, FT_Y - 18, "派发 / 调用", size=10, color="#475569", weight=600))
add(
    route(
        [
            (AUTO_X + 60, FT_Y - 8),
            (DISPATCH_X, FT_Y - 8),
            (DISPATCH_X, DISPATCH_Y),
            (MAIN_X - 10, DISPATCH_Y),
        ],
        color=BLUE_LINE,
        sw=1.2,
        dashed=True,
        marker="arrowBlue",
    )
)

# Legend.
LG_X, LG_Y, LG_W, LG_H = 1430, 1500, 450, 50
add(rect(LG_X, LG_Y, LG_W, LG_H, fill=CARD_FILL, stroke=GRAY_LINE, sw=1.0, rx=8))
add(text(LG_X + 16, LG_Y + 19, "图例 · Legend", size=11, color=GRAY_TEXT, anchor="start", weight=700))
legend_items = [
    (YELLOW_FILL, YELLOW_LINE, "数据 / 制品", None),
    (BLUE_FILL, BLUE_LINE, "主工作区", None),
    ("url(#pinkGrad)", PINK_LINE, "关键记忆", None),
    (GREEN_FILL, GREEN_LINE, "长期沉淀", None),
    (CARD_FILL, SUB_LINE, "规划中 Skill", "4 3"),
]
for index, (fill, stroke, label, dash) in enumerate(legend_items):
    lx = LG_X + 18 + index * 84
    add(rect(lx, LG_Y + 28, 12, 12, fill=fill, stroke=stroke, sw=1.0, rx=3, dash=dash))
    add(text(lx + 18, LG_Y + 38, label, size=10, color="#475569", anchor="start"))

add("</svg>")

OUT.write_text("\n".join(parts), encoding="utf-8")
print(f"Wrote {OUT} ({sum(len(part) for part in parts)} chars)")
