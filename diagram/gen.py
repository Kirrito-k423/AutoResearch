# -*- coding: utf-8 -*-
"""Generate a polished, aligned architecture diagram (SVG) for the auto-ML system."""
import math

W, H = 2000, 1380
OUT = "/Users/Zhuanz/Documents/autoresearch/diagram/autoresearch_arch.svg"

# ---------- Colors ----------
BG          = "#F6F8FB"
TITLE_BG_A  = "#1E3A8A"
TITLE_BG_B  = "#3B82F6"

YELLOW_FILL = "#FEF3C7"
YELLOW_LINE = "#F59E0B"
YELLOW_TEXT = "#92400E"

BLUE_FILL   = "#DBEAFE"
BLUE_LINE   = "#3B82F6"
BLUE_TEXT   = "#1E3A8A"

CARD_FILL   = "#FFFFFF"
CARD_LINE   = "#93C5FD"
CARD_TEXT   = "#1F2937"

SUB_FILL    = "#EFF6FF"
SUB_LINE    = "#60A5FA"
SUB_TEXT    = "#1E40AF"

GRAY_FILL   = "#F1F5F9"
GRAY_LINE   = "#94A3B8"
GRAY_TEXT   = "#0F172A"

PINK_FILL   = "#FEE2E2"
PINK_LINE   = "#EF4444"
PINK_TEXT   = "#991B1B"

ORANGE_FILL = "#FFEDD5"
ORANGE_LINE = "#F97316"

GREEN_FILL  = "#D1FAE5"
GREEN_LINE  = "#10B981"
GREEN_TEXT  = "#065F46"

SIDEBAR_FILL = "#E2E8F0"
SIDEBAR_LINE = "#64748B"
SIDEBAR_TEXT = "#0F172A"

DASH_FILL   = "#FFFFFF"
DASH_LINE   = "#60A5FA"

ARROW       = "#475569"
ARROW_SOFT  = "#94A3B8"

FONT = "'PingFang SC','Hiragino Sans GB','Microsoft YaHei','Noto Sans CJK SC','Source Han Sans SC',sans-serif"

parts = []
def add(s): parts.append(s)
def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def rect(x,y,w,h, fill=CARD_FILL, stroke=CARD_LINE, rx=10, ry=10, sw=1.4, opacity=1.0, dash=None, extra=""):
    da = f' stroke-dasharray="{dash}"' if dash else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" opacity="{opacity}"{da}{extra}/>'

def text(x,y,s, size=12, color="#1F2937", anchor="middle", weight=400, extra=""):
    lines = s.split("\n")
    out = []
    for i,line in enumerate(lines):
        dy = i * (size + 2)
        out.append(f'<text x="{x}" y="{y+dy}" font-family="{FONT}" font-size="{size}" fill="{color}" text-anchor="{anchor}" font-weight="{weight}"{extra}>{esc(line)}</text>')
    return "\n".join(out)

def pill(x,y,w,h,label, fill=SUB_FILL, stroke=SUB_LINE, color=SUB_TEXT, size=11, weight=600, rx=4):
    return rect(x,y,w,h,fill=fill,stroke=stroke,rx=rx,ry=rx,sw=1.0) + \
        text(x+w/2, y+h/2+4, label, size=size, color=color, weight=weight)

def skill_card(x,y,w,h, name, desc_lines=None, status="solid", accent=SUB_LINE, accent_fill=SUB_FILL):
    if status == "dashed":
        bg = DASH_FILL; ln = DASH_LINE; sw = 1.3
        da = "4 3"
    else:
        bg = CARD_FILL; ln = accent; sw = 1.2
        da = None
    out = [rect(x,y,w,h, fill=bg, stroke=ln, sw=sw, dash=da)]
    chip_w = 44
    out.append(rect(x+8, y+8, chip_w, 16, fill=accent_fill, stroke=accent, sw=0.8, rx=3, ry=3))
    out.append(text(x+8+chip_w/2, y+8+12, "SKILL", size=9, color=accent, weight=700))
    out.append(text(x+w/2, y+30, name, size=11, color=CARD_TEXT, weight=700))
    if desc_lines:
        for i, line in enumerate(desc_lines):
            out.append(text(x+w/2, y+30+14+i*12, line, size=10, color="#475569"))
    return "\n".join(out)

def arrow(x1,y1,x2,y2, color=ARROW, sw=1.4, dashed=False, head=True):
    path = f"M{x1},{y1} L{x2},{y2}"
    da = ' stroke-dasharray="5 4"' if dashed else ""
    head_def = ""
    if head:
        ang = math.atan2(y2-y1, x2-x1)
        ah = 8
        ax1 = x2 - ah*math.cos(ang - math.pi/7)
        ay1 = y2 - ah*math.sin(ang - math.pi/7)
        ax2 = x2 - ah*math.cos(ang + math.pi/7)
        ay2 = y2 - ah*math.sin(ang + math.pi/7)
        head_def = f'<path d="M{ax1:.1f},{ay1:.1f} L{x2:.2f},{y2:.2f} L{ax2:.1f},{ay2:.1f}" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linejoin="round"/>'
    return f'<path d="{path}" fill="none" stroke="{color}" stroke-width="{sw}"{da}/>{head_def}'

# Header & defs
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="{FONT}">')
add(f'<defs>')
add(f'  <linearGradient id="titleGrad" x1="0" y1="0" x2="1" y2="0">')
add(f'    <stop offset="0%" stop-color="{TITLE_BG_A}"/>')
add(f'    <stop offset="100%" stop-color="{TITLE_BG_B}"/>')
add(f'  </linearGradient>')
add(f'  <linearGradient id="pinkGrad" x1="0" y1="0" x2="0" y2="1">')
add(f'    <stop offset="0%" stop-color="#FEE2E2"/>')
add(f'    <stop offset="100%" stop-color="#FECACA"/>')
add(f'  </linearGradient>')
add(f'</defs>')
add(rect(0,0,W,H, fill=BG, stroke="none", sw=0))

# Title strip
add(rect(0,0,W,64, fill="url(#titleGrad)", stroke="none", sw=0))
add(text(W/2, 28, "AutoResearch · 自驱式训练 & 调试系统架构", size=20, color="#FFFFFF", weight=700))
add(text(W/2, 50, "数据 / 代码 / 评测 / 决策 一体化 · Cline + GLM-5 + wandb", size=12, color="#DBEAFE", weight=400))

# Column layout
PAD = 30
SIDEBAR_W = 80
GAP = 12
x_sideL = PAD
x_main  = x_sideL + SIDEBAR_W + GAP
x_pi    = x_main + 720 + GAP
x_wandb = x_pi + 360 + GAP
x_sideR = W - PAD - SIDEBAR_W

# Column headers
HDR_Y = 80
add(text((x_main + x_pi - GAP)/2, HDR_Y, "① 主工作区 · 模型与训练链路", size=13, color=BLUE_TEXT, weight=700))
add(text((x_pi + x_wandb - GAP)/2, HDR_Y, "② PI Agent · 智能体层", size=13, color="#334155", weight=700))
add(text((x_wandb + x_sideR - GAP)/2, HDR_Y, "③ 数据湖 · 记忆与决策", size=13, color=GREEN_TEXT, weight=700))

# Top yellow row
TOP_Y = 110
TOP_H = 100
add(rect(x_main, TOP_Y, 720, TOP_H, fill=YELLOW_FILL, stroke=YELLOW_LINE, sw=1.5))
add(text(x_main+24, TOP_Y+24, "🏠  黄区虚拟环境", size=14, color=YELLOW_TEXT, weight=700, anchor="start"))
add(text(x_main+24, TOP_Y+44, "venv / docker 隔离运行容器", size=11, color="#78350F", anchor="start"))
add(text(x_main+24, TOP_Y+62, "镜像内置 verl + 训练脚本", size=11, color="#78350F", anchor="start"))
add(text(x_main+24, TOP_Y+80, "提供端到端一致的执行底座", size=11, color="#78350F", anchor="start"))

add(rect(x_wandb, TOP_Y, x_sideR - x_wandb, TOP_H, fill=YELLOW_FILL, stroke=YELLOW_LINE, sw=1.5))
add(text(x_wandb+24, TOP_Y+24, "📦  运行日志 & Debug 数据", size=14, color=YELLOW_TEXT, weight=700, anchor="start"))
add(text(x_wandb+24, TOP_Y+44, "· 训练运行 log（成功 / 失败）", size=11, color="#78350F", anchor="start"))
add(text(x_wandb+24, TOP_Y+62, "· profiling · 内存快照", size=11, color="#78350F", anchor="start"))
add(text(x_wandb+24, TOP_Y+80, "· plog / debug info / artifact", size=11, color="#78350F", anchor="start"))

# 从私仓拉取 label
add(text(x_main-6, TOP_Y+TOP_H/2-4, "从私仓", size=10, color="#475569", weight=600, anchor="end"))
add(text(x_main-6, TOP_Y+TOP_H/2+10, "拉取", size=10, color="#475569", weight=600, anchor="end"))
add(arrow(x_main-2, TOP_Y+TOP_H/2, x_main+2, TOP_Y+TOP_H/2, color=ARROW, sw=1.2, head=True))

# Arrow from right yellow down to wandb
add(arrow(x_wandb + (x_sideR-x_wandb)/2, TOP_Y+TOP_H, x_wandb + (x_sideR-x_wandb)/2, 240, color=ARROW, sw=1.4, head=True))

# Sidebars
SB_TOP = 230
SB_H = 600
add(rect(x_sideL, SB_TOP, SIDEBAR_W, SB_H, fill=SIDEBAR_FILL, stroke=SIDEBAR_LINE, sw=1.2))
add(text(x_sideL+SIDEBAR_W/2, SB_TOP+24, "☁️", size=18, color=SIDEBAR_TEXT, weight=700))
add(text(x_sideL+SIDEBAR_W/2, SB_TOP+46, "GitHub", size=12, color=SIDEBAR_TEXT, weight=700))
add(text(x_sideL+SIDEBAR_W/2, SB_TOP+62, "备份", size=12, color=SIDEBAR_TEXT, weight=700))
add(f'<g transform="translate({x_sideL+SIDEBAR_W/2},{SB_TOP+SB_H/2})">')
add(f'  <path d="M-22,-30 L22,-30 M22,-30 L12,-36 M22,-30 L12,-24" fill="none" stroke="{SIDEBAR_LINE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'  <path d="M22,30 L-22,30 M-22,30 L-12,24 M-22,30 L-12,36" fill="none" stroke="{SIDEBAR_LINE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'</g>')

add(rect(x_sideR, SB_TOP, SIDEBAR_W, SB_H, fill=SIDEBAR_FILL, stroke=SIDEBAR_LINE, sw=1.2))
add(text(x_sideR+SIDEBAR_W/2, SB_TOP+24, "💾", size=18, color=SIDEBAR_TEXT, weight=700))
add(text(x_sideR+SIDEBAR_W/2, SB_TOP+46, "数据", size=12, color=SIDEBAR_TEXT, weight=700))
add(text(x_sideR+SIDEBAR_W/2, SB_TOP+62, "备份", size=12, color=SIDEBAR_TEXT, weight=700))
add(f'<g transform="translate({x_sideR+SIDEBAR_W/2},{SB_TOP+SB_H/2})">')
add(f'  <path d="M-22,-30 L22,-30 M22,-30 L12,-36 M22,-30 L12,-24" fill="none" stroke="{SIDEBAR_LINE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'  <path d="M22,30 L-22,30 M-22,30 L-12,24 M-22,30 L-12,36" fill="none" stroke="{SIDEBAR_LINE}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
add(f'</g>')

# verl-DFX
MD_X = x_main
MD_W = 720
DFX_Y = 240
DFX_H = 130
add(rect(MD_X, DFX_Y, MD_W, DFX_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MD_X+16, DFX_Y+20, "verl-DFX  ·  训练/推理能力底座", size=13, color=BLUE_TEXT, weight=700, anchor="start"))
putils_w = 130
add(rect(MD_X+24, DFX_Y+40, putils_w, 70, fill=CARD_FILL, stroke=CARD_LINE, sw=1.2))
add(text(MD_X+24+putils_w/2, DFX_Y+62, "putils", size=12, color=BLUE_TEXT, weight=700))
add(text(MD_X+24+putils_w/2, DFX_Y+82, "工具集", size=10, color="#475569"))
add(text(MD_X+24+putils_w/2, DFX_Y+98, "Path Util", size=10, color="#475569"))
inner_x = MD_X+170
inner_w = MD_W - 170 - 20
add(rect(inner_x, DFX_Y+40, inner_w, 70, fill=SUB_FILL, stroke=SUB_LINE, sw=1.0))
add(text(inner_x+inner_w/2, DFX_Y+56, "verl 原仓  (verl 原生能力 · mode=x 切换)", size=11, color=SUB_TEXT, weight=700))
sub_y = DFX_Y+66
sub_h = 36
sub_w = (inner_w - 30) / 4
sub_xs = [inner_x+10 + i*(sub_w+6) for i in range(4)]
for sx, label in zip(sub_xs, ["FSDP", "x-bridge", "vllm", "sglang…"]):
    add(rect(sx, sub_y, sub_w, sub_h, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(text(sx+sub_w/2, sub_y+sub_h/2+4, label, size=11, color=BLUE_TEXT, weight=600))

add(text(x_sideL+SIDEBAR_W+6, DFX_Y+DFX_H/2-4, "同步到", size=10, color="#475569", weight=600, anchor="start"))
add(text(x_sideL+SIDEBAR_W+6, DFX_Y+DFX_H/2+10, "私仓", size=10, color="#475569", weight=600, anchor="start"))
add(arrow(MD_X-2, DFX_Y+DFX_H/2, MD_X+2, DFX_Y+DFX_H/2, color=ARROW, sw=1.2))

ADAP_Y = DFX_Y + DFX_H + 30
add(rect(MD_X+MD_W/2-180, DFX_Y+DFX_H+6, 360, 18, fill="#FFFFFF", stroke="#CBD5E1", sw=0.8, rx=4, ry=4))
add(text(MD_X+MD_W/2, DFX_Y+DFX_H+18, "通过 mode=x 使能不同 skill 且场景需要的代码", size=10, color="#475569"))
add(arrow(MD_X + MD_W/2, DFX_Y+DFX_H+24, MD_X + MD_W/2, ADAP_Y-4, color=ARROW, sw=1.2, head=True))

# workspace-adapter
ADAP_H = 220
add(rect(MD_X, ADAP_Y, MD_W, ADAP_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MD_X+16, ADAP_Y+20, "workspace-adapter  ·  场景经验 / 治理与约束", size=13, color=BLUE_TEXT, weight=700, anchor="start"))
add(text(MD_X+MD_W-16, ADAP_Y+20, "(对接 DFX · 训练全流程 Skill 集)", size=11, color="#475569", weight=500, anchor="end"))

sk_y = ADAP_Y+38
gap_x = 8
n_skills = 6
sk_w = (MD_W - 32 - gap_x*(n_skills-1)) / n_skills
skill_data = [
    ("环境搭建 (verl)",   ["沉淀脚本 / JSON", "验收条件自检"]),
    ("verl-env-doctor",   ["检查代理 · NPU", "CANN · torch_npu", "Ray · 依赖 / 数据集"]),
    ("任务运行",          ["拉起训练任务", "收集过程数据"]),
    ("性能采集",          ["推理 & 训练", "指标 · timeline"]),
    ("显存采集",          ["峰值 · 曲线", "OOM 风险提示"]),
    ("下游评测",          ["任务级指标", "结果回写"]),
    ("训练一致性分析",    ["对比多 run", "偏差定位"]),
    ("自动分析",          ["异常归因", "建议方案"]),
]
for i, (name, desc) in enumerate(skill_data[:6]):
    sx = MD_X + 16 + i*(sk_w+gap_x)
    add(skill_card(sx, sk_y, sk_w, 90, name, desc, status="solid", accent=SUB_LINE, accent_fill=SUB_FILL))

sk2_y = sk_y + 98
sk2_w = (MD_W - 32 - gap_x) / 2
for i, (name, desc) in enumerate(skill_data[6:]):
    sx = MD_X + 16 + i*(sk2_w+gap_x)
    add(skill_card(sx, sk2_y, sk2_w, 80, name, desc, status="dashed", accent=DASH_LINE, accent_fill=DASH_FILL))

# workspace-core
WC_Y = ADAP_Y + ADAP_H + 30
WC_H = 400
add(rect(MD_X, WC_Y, MD_W, WC_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.6))
add(text(MD_X+16, WC_Y+20, "workspace-core  ·  工具接口与协议", size=13, color=BLUE_TEXT, weight=700, anchor="start"))
add(text(MD_X+MD_W-16, WC_Y+20, "(统一的 Skill 容器 / Session 编排)", size=11, color="#475569", weight=500, anchor="end"))

area_x = MD_X + 16
area_y = WC_Y + 40
area_w = MD_W - 32
area_h = 230

sub_w2 = (area_w - 16) / 2
sub_h2 = (area_h - 12) / 2

# (1) 执行环境与沙箱
ax1, ay1 = area_x, area_y
add(rect(ax1, ay1, sub_w2, sub_h2, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(ax1+12, ay1+18, "▎执行环境与沙箱", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
mini_w = (sub_w2 - 30) / 3
mini_data1 = [("园区网络", "配置管理"), ("环境搭建", "(数据库)"), ("远程连接", "SSH/隧道")]
for i, (a, b) in enumerate(mini_data1):
    mx = ax1 + 12 + i*(mini_w+6)
    my = ay1 + 30
    add(rect(mx, my, mini_w, 46, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(pill(mx+mini_w/2-22, my+5, 44, 13, "SKILL", size=8, rx=3))
    add(text(mx+mini_w/2, my+27, a, size=10, color=CARD_TEXT, weight=700))
    add(text(mx+mini_w/2, my+40, b, size=8, color="#64748B"))
# banner under
ban_y = ay1 + sub_h2 - 26
add(rect(ax1+12, ban_y, sub_w2-24, 20, fill=GREEN_FILL, stroke=GREEN_LINE, sw=1.0, rx=4, ry=4))
add(text(ax1+sub_w2/2, ban_y+14, "沉淀 / 脚本 / 验收条件（前/后置 hook 实现）", size=10, color=GREEN_TEXT, weight=600))

# (2) 工具接口与协议
ax2, ay2 = area_x + sub_w2 + 16, area_y
add(rect(ax2, ay2, sub_w2, sub_h2, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(ax2+12, ay2+18, "▎工具接口与协议", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
mini_data2 = [("执行", "会话上下文\n管理"), ("性能采集", "带/不带堆栈\n有限大小"), ("显存采集", "峰值/趋势\nOOM 提示")]
mini_w2 = (sub_w2 - 30) / 3
for i, (n, sub) in enumerate(mini_data2):
    mx = ax2 + 12 + i*(mini_w2+6)
    my = ay2 + 30
    add(rect(mx, my, mini_w2, 56, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(pill(mx+mini_w2/2-22, my+5, 44, 13, "SKILL", size=8, rx=3))
    add(text(mx+mini_w2/2, my+27, n, size=10, color=CARD_TEXT, weight=700))
    sub_lines = sub.split("\n")
    add(text(mx+mini_w2/2, my+40, sub_lines[0], size=8, color="#475569"))
    if len(sub_lines) > 1:
        add(text(mx+mini_w2/2, my+50, sub_lines[1], size=8, color="#475569"))

# (3) 可观测性
ax3, ay3 = area_x, area_y + sub_h2 + 12
add(rect(ax3, ay3, sub_w2, sub_h2, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(ax3+12, ay3+18, "▎可观测性", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
mini_data3 = [("对比可视化", "生成图表"), ("关键信息提取", "字段抽取/对齐")]
mini_w3 = (sub_w2 - 24) / 2
for i, (n, sub) in enumerate(mini_data3):
    mx = ax3 + 12 + i*(mini_w3+6)
    my = ay3 + 30
    add(rect(mx, my, mini_w3, 56, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(pill(mx+mini_w3/2-22, my+5, 44, 13, "SKILL", size=8, rx=3))
    add(text(mx+mini_w3/2, my+27, n, size=10, color=CARD_TEXT, weight=700))
    add(text(mx+mini_w3/2, my+45, sub, size=9, color="#475569"))

# (4) 生命周期与编排
ax4, ay4 = area_x + sub_w2 + 16, area_y + sub_h2 + 12
add(rect(ax4, ay4, sub_w2, sub_h2, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(ax4+12, ay4+18, "▎生命周期与编排", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
ax4_in = ax4 + 12
ay4_in = ay4 + 30
add(rect(ax4_in, ay4_in, sub_w2-24, 56, fill=DASH_FILL, stroke=DASH_LINE, sw=1.2, dash="4 3"))
add(pill(ax4_in+12, ay4_in+6, 44, 13, "SKILL", size=8, rx=3, fill=ORANGE_FILL, stroke=ORANGE_LINE, color="#9A3412"))
add(text(ax4_in+sub_w2/2-12, ay4_in+28, "自动研究", size=11, color=CARD_TEXT, weight=700))
add(text(ax4_in+sub_w2/2-12, ay4_in+42, "已完成 / 未完成 → 启动 / 成功 /", size=8, color="#475569"))
add(text(ax4_in+sub_w2/2-12, ay4_in+52, "失败 / 重启 / 收敛", size=8, color="#475569"))

# Run/Session layer
rs_y = WC_Y + WC_H - 50
add(rect(MD_X+16, rs_y, MD_W-32, 40, fill="#FFFFFF", stroke=BLUE_LINE, sw=1.4, rx=8, ry=8))
add(pill(MD_X+24, rs_y+6, 100, 14, "Run / Session 层", size=10, color=BLUE_TEXT, fill=BLUE_FILL, stroke=BLUE_LINE, weight=700, rx=3))
add(text(MD_X+MD_W/2, rs_y+18, "(完全托管给强大的工具层实现)  ·  日志 / 进程 / 资源 lease / 远程同步", size=10, color="#475569"))
add(text(MD_X+MD_W/2, rs_y+32, "为上层 PI Agent 提供可复现的执行环境", size=9, color="#64748B"))

# PI Agent column
PI_X = x_pi
PI_W = 360
PI_Y = DFX_Y

PI_HDR_H = 70
add(rect(PI_X, PI_Y, PI_W, PI_HDR_H, fill=GRAY_FILL, stroke=GRAY_LINE, sw=1.4))
add(pill(PI_X+12, PI_Y+10, 56, 16, "工具层", size=10, color=GRAY_TEXT, fill="#FFFFFF", stroke=GRAY_LINE, weight=700, rx=3))
add(text(PI_X+12+28, PI_Y+22, "Cline", size=10, color="#334155", weight=600, anchor="start"))
add(pill(PI_X+72, PI_Y+10, 56, 16, "模型层", size=10, color=GRAY_TEXT, fill="#FFFFFF", stroke=GRAY_LINE, weight=700, rx=3))
add(text(PI_X+72+28, PI_Y+22, "GLM-5", size=10, color="#334155", weight=600, anchor="start"))
add(pill(PI_X+12, PI_Y+34, 96, 16, "生命周期与编排", size=10, color=PINK_TEXT, fill=PINK_FILL, stroke=PINK_LINE, weight=700, rx=3))
add(text(PI_X+PI_W-12, PI_Y+22, "📡  Agent 引擎", size=12, color=GRAY_TEXT, weight=700, anchor="end"))

PI_CORE_Y = PI_Y + PI_HDR_H + 12
PI_CORE_H = 110
add(rect(PI_X, PI_CORE_Y, PI_W, PI_CORE_H, fill="#FFFFFF", stroke=BLUE_LINE, sw=2.0, rx=14, ry=14))
add(text(PI_X+PI_W/2, PI_CORE_Y+34, "🧠  PI Agent", size=18, color=BLUE_TEXT, weight=800))
add(text(PI_X+PI_W/2, PI_CORE_Y+58, "Oh-My-Pi", size=14, color="#1E40AF", weight=700))
add(text(PI_X+PI_W/2, PI_CORE_Y+82, "阅读理解代码 · 修复 Bug · 开关特性", size=10, color="#475569"))
add(text(PI_X+PI_W/2, PI_CORE_Y+98, "任务 → 决策 → 行动  ↻", size=10, color="#475569", weight=600))

WF_Y = PI_CORE_Y + PI_CORE_H + 14
WF_H = 220
add(rect(PI_X, WF_Y, PI_W, WF_H, fill=GRAY_FILL, stroke=GRAY_LINE, sw=1.2))
add(text(PI_X+12, WF_Y+18, "▎核心工作循环", size=12, color=GRAY_TEXT, weight=700, anchor="start"))
mini_box_w = 92
mini_box_h = 50
mini_gap_x = (PI_W - 24 - mini_box_w*3) / 2
mini_gap_y = 16
loop = ["测试运行", "日志", "分析报告", "分析代码", "修改代码", "目标"]
for i, name in enumerate(loop):
    r = i // 3
    c = i % 3
    bx = PI_X + 12 + c*(mini_box_w + mini_gap_x)
    by = WF_Y + 36 + r*(mini_box_h + mini_gap_y + 12)
    add(rect(bx, by, mini_box_w, mini_box_h, fill="#FFFFFF", stroke=GRAY_LINE, sw=1.1, rx=6, ry=6))
    add(pill(bx+mini_box_w/2-22, by+6, 44, 14, f"#{i+1}", size=9, color=GRAY_TEXT, fill="#E2E8F0", stroke=GRAY_LINE, weight=700, rx=3))
    add(text(bx+mini_box_w/2, by+mini_box_h-10, name, size=11, color="#1F2937", weight=700))

add(text(PI_X+PI_W+8, WF_Y+WF_H/2-8, "遵循 skills 规格", size=10, color="#475569", anchor="start"))
add(text(PI_X+PI_W+8, WF_Y+WF_H/2+6, "维护数据信息", size=10, color="#475569", anchor="start"))
add(arrow(PI_X+PI_W, WF_Y+WF_H/2, x_wandb-2, WF_Y+WF_H/2, color=ARROW, sw=1.2))

# brace between PI and main modules
add(text(PI_X-8, WC_Y+WC_H/2-8, "遵循与", size=10, color="#475569", weight=600, anchor="end"))
add(text(PI_X-8, WC_Y+WC_H/2+6, "消化", size=10, color="#475569", weight=600, anchor="end"))
add(f'<path d="M{PI_X-4},{WC_Y+20} Q{PI_X-12},{WC_Y+WC_H/2} {PI_X-4},{WC_Y+WC_H-20}" fill="none" stroke="#94A3B8" stroke-width="1.2"/>')
add(f'<path d="M{PI_X-4},{WC_Y+20} l-4,-3 M{PI_X-4},{WC_Y+20} l-4,3" fill="none" stroke="#94A3B8" stroke-width="1.2"/>')
add(f'<path d="M{PI_X-4},{WC_Y+WC_H-20} l-4,-3 M{PI_X-4},{WC_Y+WC_H-20} l-4,3" fill="none" stroke="#94A3B8" stroke-width="1.2"/>')

# wandb data lake
WB_X = x_wandb
WB_W = x_sideR - x_wandb
WB_Y = DFX_Y

WB_HDR_H = 30
add(rect(WB_X, WB_Y, WB_W, WB_HDR_H, fill=BLUE_FILL, stroke=BLUE_LINE, sw=1.4))
add(text(WB_X+WB_W/2, WB_Y+20, "wandb / 数据湖  ·  上下文 & 记忆管理", size=13, color=BLUE_TEXT, weight=700))

raw_y = WB_Y + WB_HDR_H + 8
raw_h = 90
add(rect(WB_X, raw_y, WB_W, raw_h, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(WB_X+12, raw_y+18, "▎原始数据", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
raw_card_w = (WB_W - 36) / 3
raw_cards = [("运行 log", "成功 / 失败"), ("profiling", "性能画像"), ("历史会话", "上下文回放")]
for i, (n, sub) in enumerate(raw_cards):
    bx = WB_X + 12 + i*(raw_card_w+6)
    by = raw_y + 32
    add(rect(bx, by, raw_card_w, 50, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(text(bx+raw_card_w/2, by+22, n, size=11, color=BLUE_TEXT, weight=700))
    add(text(bx+raw_card_w/2, by+38, sub, size=10, color="#475569"))

kp_y = raw_y + raw_h + 10
kp_h = 96
add(rect(WB_X, kp_y, WB_W, kp_h, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(WB_X+12, kp_y+18, "▎关键字段解析 & 预处理", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
kp_card_w = (WB_W - 30) / 2
kp_cards = [("采集信息 + 初步建议", "性能 · 内存 · 精度 · 效果"), ("脚本提取", "可复现的最小步骤")]
for i, (n, sub) in enumerate(kp_cards):
    bx = WB_X + 12 + i*(kp_card_w+6)
    by = kp_y + 32
    add(rect(bx, by, kp_card_w, 56, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
    add(text(bx+kp_card_w/2, by+22, n, size=11, color=BLUE_TEXT, weight=700))
    add(text(bx+kp_card_w/2, by+40, sub, size=10, color="#475569"))
add(arrow(WB_X+WB_W*0.78, kp_y+kp_h-12, WB_X+WB_W*0.22, kp_y+kp_h-12, color=ORANGE_LINE, sw=1.2, head=True))

er_y = kp_y + kp_h + 10
er_h = 50
add(rect(WB_X, er_y, WB_W, er_h, fill="url(#pinkGrad)", stroke=PINK_LINE, sw=1.6, rx=8, ry=8))
add(pill(WB_X+12, er_y+8, 120, 16, "Experiment Registry", size=10, color=PINK_TEXT, fill="#FFFFFF", stroke=PINK_LINE, weight=700, rx=3))
add(text(WB_X+WB_W-12, er_y+er_h/2+4, "实验进度表 · 长期记忆 · 指导任务的下一步", size=10, color=PINK_TEXT, weight=600, anchor="end"))

rp_y = er_y + er_h + 10
rp_h = 90
add(rect(WB_X, rp_y, WB_W, rp_h, fill=SUB_FILL, stroke=SUB_LINE, sw=1.2))
add(text(WB_X+12, rp_y+18, "▎报告  (LLM 可读 md)", size=12, color=BLUE_TEXT, weight=700, anchor="start"))
llm_x = WB_X + WB_W/2 - 40
llm_y = rp_y + 32
llm_w = 80
llm_h = 50
add(rect(llm_x, llm_y, llm_w, llm_h, fill=DASH_FILL, stroke=DASH_LINE, sw=1.2, dash="4 3"))
add(text(llm_x+llm_w/2, llm_y+20, "LLM", size=12, color="#1E40AF", weight=700))
add(text(llm_x+llm_w/2, llm_y+36, "分析", size=12, color="#1E40AF", weight=700))
out1_x = WB_X + 12
out1_w = llm_x - out1_x - 20
add(rect(out1_x, llm_y+6, out1_w, 18, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
add(text(out1_x+out1_w/2, llm_y+18, "md 分析报告（AI 交互）", size=10, color="#1F2937", weight=600))
add(rect(out1_x, llm_y+28, out1_w, 18, fill=CARD_FILL, stroke=SUB_LINE, sw=1.0))
add(text(out1_x+out1_w/2, llm_y+40, "自动研究进度", size=10, color="#1F2937", weight=600))
add(arrow(llm_x, llm_y+llm_h/2, out1_x+out1_w+2, llm_y+15, color=ARROW, sw=1.0))
add(arrow(llm_x, llm_y+llm_h/2, out1_x+out1_w+2, llm_y+37, color=ARROW, sw=1.0))

# Bottom dashboards
DB_Y = WC_Y + WC_H + 30
DB_H = 110
db_w = (MD_W + 360 + WB_W - 16) / 3
db1_x = MD_X
db2_x = db1_x + db_w + 8
db3_x = db2_x + db_w + 8
dbs = [
    ("📊  任务进度看板", "监控各阶段流程的拆解与完成情况\n（参考 AgentHub）", BLUE_FILL, BLUE_LINE, BLUE_TEXT),
    ("📈  数据指标分析看板", "wandb 集成：loss / acc / 吞吐\n指标趋势 / 异常告警", GREEN_FILL, GREEN_LINE, GREEN_TEXT),
    ("🖥️  运行时资源看板", "Prometheus + Grafana\nGPU / 内存 / 网络 / 队列", ORANGE_FILL, ORANGE_LINE, "#9A3412"),
]
for i, (title, body, fill, line, color) in enumerate(dbs):
    bx = [db1_x, db2_x, db3_x][i]
    add(rect(bx, DB_Y, db_w, DB_H, fill=fill, stroke=line, sw=1.5))
    add(text(bx+db_w/2, DB_Y+26, title, size=14, color=color, weight=700))
    add(text(bx+db_w/2, DB_Y+58, body, size=12, color="#1F2937", weight=500))

# small "可视化" arrow from wandb (rp end) to dashboards
add(text(WB_X+WB_W/2, DB_Y-8, "↓  可视化 · 全过程监控", size=10, color=GREEN_TEXT, weight=600))
# dotted line
add(f'<line x1="{WB_X+WB_W/2}" y1="{rp_y+rp_h+2}" x2="{WB_X+WB_W/2}" y2="{DB_Y-16}" stroke="{GREEN_LINE}" stroke-width="1.2" stroke-dasharray="4 3"/>')

# Footer
FT_Y = DB_Y + DB_H + 24
FT_H = 70
ar_w = 460
ar_x = MD_X
add(rect(ar_x, FT_Y, ar_w, FT_H, fill="#FFFFFF", stroke=BLUE_LINE, sw=1.6, rx=10, ry=10))
add(pill(ar_x+16, FT_Y+10, 96, 18, "⚙️ 自动研究", size=11, color=BLUE_TEXT, fill=BLUE_FILL, stroke=BLUE_LINE, weight=700, rx=3))
add(text(ar_x+ar_w/2, FT_Y+30, "(定时任务 + 提示词：)", size=10, color="#475569", weight=600))
add(text(ar_x+ar_w/2, FT_Y+48, "任务队列 → 生成提议 → 创建 session → 调用技能", size=10, color="#1F2937"))
add(text(ar_x+ar_w/2, FT_Y+62, "→ 跑训练 → 生成简报", size=10, color="#1F2937"))

dev_w = 460
dev_x = x_wandb + (WB_W - dev_w)/2
add(rect(dev_x, FT_Y, dev_w, FT_H, fill="#FFFFFF", stroke=GREEN_LINE, sw=1.6, rx=10, ry=10))
add(pill(dev_x+16, FT_Y+10, 96, 18, "👤  开发人员", size=11, color=GREEN_TEXT, fill=GREEN_FILL, stroke=GREEN_LINE, weight=700, rx=3))
add(text(dev_x+dev_w/2, FT_Y+38, "需求评审 · 异常介入 · 验收", size=12, color="#1F2937", weight=600))
add(text(dev_x+dev_w/2, FT_Y+56, "查看看板 · 决策干预", size=10, color="#475569"))

add(arrow(dev_x, FT_Y+FT_H/2, ar_x+ar_w+2, FT_Y+FT_H/2, color=ARROW, sw=1.2))
add(arrow(ar_x+ar_w/2, FT_Y-2, ar_x+ar_w/2, WC_Y+WC_H+8, color=BLUE_LINE, sw=1.4, head=True, dashed=True))
add(rect(ar_x+ar_w/2-50, FT_Y-22, 100, 16, fill="#FFFFFF", stroke="#CBD5E1", sw=0.8, rx=4, ry=4))
add(text(ar_x+ar_w/2, FT_Y-10, "派发 / 调用", size=10, color="#475569", weight=600))

# Legend
LG_X = W - 360
LG_Y = H - 60
LG_W = 330
LG_H = 46
add(rect(LG_X, LG_Y, LG_W, LG_H, fill="#FFFFFF", stroke=GRAY_LINE, sw=1.0, rx=8, ry=8))
add(text(LG_X+14, LG_Y+16, "图例 · Legend", size=11, color=GRAY_TEXT, weight=700, anchor="start"))
legend_items = [
    (YELLOW_FILL, YELLOW_LINE, "数据 / 制品", None),
    (BLUE_FILL, BLUE_LINE, "主工作区", None),
    ("url(#pinkGrad)", PINK_LINE, "关键记忆", None),
    (DASH_FILL, DASH_LINE, "规划中 Skill", "4 3"),
]
for i, (f, l, t, da) in enumerate(legend_items):
    cx = LG_X + 16 + i*78
    add(rect(cx, LG_Y+24, 12, 12, fill=f, stroke=l, sw=1.0, dash=da))
    add(text(cx+18, LG_Y+33, t, size=10, color="#475569", anchor="start"))

add("</svg>")

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(parts))

print(f"Wrote {OUT} ({sum(len(p) for p in parts)} chars)")
