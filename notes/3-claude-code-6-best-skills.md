# Claude Code 最值得装的 6 个 Skill / Plugin

`Nate Herk · 13m39s` · video_id: `eRS3CmvrOvA` · [原片](https://youtu.be/eRS3CmvrOvA)

> ### 🟡 3/5 — 建议 SKIP，读这篇即可
> 干货 = 下面一张工具清单。视频 60% 在讲"怎么把 AI 自动化卖给中小企业"，对你无意义。

| 维度 | 评级 |
|------|------|
| 新颖度 | ★★☆☆☆ 概念你都懂，新的只是"具体哪些工具" |
| 可操作性 | ★★★★☆ 6 个都能直接装来用 |
| 深度 | ★★☆☆☆ 只有 what/why，几乎没讲机制 |

---

## 📦 6+1 个工具

| 工具 | 是什么 | 解决什么问题 |
|------|--------|------------|
| **Skill Creator** <br>`官方` | 自然语言/SOP → Claude 自动起草·测试·打包 skill | 免去手写 `SKILL.md`、调 trigger 的学习曲线 |
| **Superpowers** <br>`社区 ~150k★` | 强制 Claude 走资深流程：plan → 先写测试 → 隔离环境 → 两段自审 | 一把过质量从 ~60% 拉到 ~80%，少 debug 轮次 |
| **GSD** (Get Shit Done) | 每个任务 spawn 干净 context 的 sub-agent + quality gate + autonomous 模式 | **context rot**：长 session 中途退化、忘需求 |
| **`/review` · `/ultra review`** <br>`内置` | review 本地快审；ultra 上传云端多 agent 并行攻，bug 须独立复现才报 | 合并前抓 Claude 自己漏的 bug，少假阳性 |
| **Context Mode** <br>`MCP+hooks` | tool call 走 sandbox 只回必要结果；本地 SQL 记 session，compact 时重注入 | tool 输出撑爆 context、compact 后失忆 |
| **ClaudeMem** | 跨 session 记忆：hook 进生命周期，语义摘要存 SQLite+向量检索，自动写 `CLAUDE.md` | 每开新 session 重新解释项目的"启动税" |
| **Front-end Design** <br>`官方·bonus` | 让产出 UI 不那么"AI 味" | —（建议全局装） |

---

## ✅ 能直接搬进你工作流的

- **组合拳**(全片唯一有结构的洞见)：
  `Superpowers 出流程` → `GSD 给每任务干净 context` → 合并前 `/ultra review` 终审。三者解决正交问题。
- **通用 skill 装 user/global scope**(skill-creator、design)，随处自动可用。
- **`/ultra review` 使用门槛**：需 CC ≥ 2.1.86 + Claude 账号登录(纯 API key 不行)、跑 10–20 分钟(后台)、Pro/Max 3 次免费后约 \$5–20/次。→ 只在大重构 / 碰 payment·auth·DB migration 时用，平时用 `/review`。

## 💡 值得内化的判断框架

> **"省时间 ≠ 省 token"**。Superpowers/GSD 费 token 但省返工；Context Mode/ClaudeMem 才真省 token(靠裁剪进 context 的量)。评估任何工具时套这个区分。

## ⚠️ 待你自测(数字均来自各 repo 自报)

Superpowers 150k★ · Context Mode 315KB→5KB · ClaudeMem 10× 检索节省 · ultra review 价格(作者自己说"可能已变")。

`#claude-code` `#skills` `#plugins` `#context-engineering` `#subagents` `#code-review` `#memory`
