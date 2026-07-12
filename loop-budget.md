# AutoResearch Loop Budget

## L1 report-only

- Cadence: 手动；稳定后最多每日一次。
- Max candidate hypotheses: 1 / run。
- Max sub-agents: 0。
- Remote compute: 0。
- Local command budget: 只读检查与轻量测试，总计不超过 15 分钟。
- `loop-cost` 以每日一次估算：现实混合约 23k tokens/day，完整分诊约 50k，最坏动作型运行 200k；每日硬上限取 100k，达到 80% 即停止。

## L2 assisted experiment

- Max attempts: 3 / hypothesis。
- Max roles: 1 maker + 1 independent verifier。
- Max remote experiments: 1 / approved run。
- Time cap: 30 分钟本地验证；远程训练预算必须由人在运行前单独给出。
- Stop on: 两次相同失败签名、指标不可比、证据缺失、权限不清、预算达到 80%。

## Kill switch

根目录出现 `.loop-paused`，或 `STATE.md` 的 `Status` 设为 `paused` 时，循环必须立即停止动作并仅生成状态报告。
