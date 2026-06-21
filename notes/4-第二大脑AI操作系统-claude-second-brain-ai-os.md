# 把 Claude 搭成"第二大脑 / AI 操作系统"(Four C's 框架)

`Nate Herk · 34m20s` · video_id: `8QQ_INxAhRs` · [原片](https://youtu.be/8QQ_INxAhRs)

## 📺 这视频在讲什么

一个博主把自己生活和公司的所有资料——笔记、会议记录、客户名单、账目——全都喂给 Claude Code，让它变成一个特别懂他的私人助手：什么都能问，还能帮他自动干活。他给这套东西起名叫"第二大脑"。这期视频不教你敲代码，主要讲他是**怎么一步步把这套助手搭起来、平时怎么管**，以及出过的大乱子（有一次 AI 自作主张把优惠券群发给了二十万人）。

---

> ### 🟢 4/5 — SKIM(读笔记 + 略看中段文件结构演示即可)
> 价值是一套**可复用的心智框架**和一个真实的权限事故教训,不是具体工具。34 分钟有水分(反复推免费课),但框架本身值得内化。

| 维度 | 评级 |
|------|------|
| 新颖度 | ★★★☆☆ Four C's / "keys not prompts" 是好框架,非技术突破 |
| 可操作性 | ★★★★☆ 路由式 CLAUDE.md、skill 迭代、scoped key 都能直接用 |
| 深度 | ★★★☆☆ 概念/心态为主,无代码级机制 |

---

## 🧠 核心框架:两层 + Four C's

**两层**:`第二大脑(知识)` 是地基 → 上面才搭 `AI OS(行动)`。

| C | 属于 | 是什么 | 关键做法 |
|---|------|--------|---------|
| **Context** | 第二大脑 | 你是谁/业务/流程的**静态**知识 | **CLAUDE.md 当路由器**:不塞满内容,而是指向 files/rules/skills/wikis 的路径 |
| **Connections** | 第二大脑 | **常变**的实时数据 | 优先用 **API / CLI**(比 MCP 更可控、更便宜);tier-1 先接:营收、客户、日历、通讯、任务、会议 |
| **Capabilities** | AI OS | 能做什么:skills / agents / 自动化 | skill 可以只是一个 prompt;**每次用完都 "update the skill"** 迭代 |
| **Cadence** | AI OS | 让它自己跑(睡觉时也跑) | 触发器:手动 / 事件 / 定时;部署成 routine、loop、确定性脚本、n8n |

> 顺序很重要:先有知识(Context+Connections)才谈行动(Capabilities+Cadence)。

---

## ✅ 能直接搬进你工作流的

- **CLAUDE.md = 路由树**。别当 dump,当"地图":指向规则/引用/skills/其他项目/wiki 的路径。健康检查:**你和 agent 都能凭直觉快速找到文件**;agent 找一个你秒知位置的文件却搜了 5 分钟 → 该重构目录了。
- **"Other worlds" 文件夹**:把常用的其他 CC 项目**嵌进主项目**。好处:① 一次 `git push` 同步全部(换机器 `pull` 即可)② 主 OS 能跨项目拿 context、`cd` 过去改东西。
- **skill 迭代闭环**:skill 第一次几乎不会完美;每次用 = 一份数据 →"我喜欢这个/不喜欢那个,update skill,再跑"。四个月前建的 skill 也持续在改。
- **流水线式分工 + `/clear`**:一个 agent 只做一件事做到极致(研究→`/clear`→把输出喂给草稿→`/clear`→润色),避免单 session context rot。
- **并行委派降本**:贵模型(Fable)做主脑,并行子任务甩给 **Sonnet/Haiku**,只收一份干净汇总(dynamic workflows)。
- **"grill me" 技能**(源自 Matt PCO):让 Claude 反过来**连环追问你 15–30 个问题**,把你脑子里的知识抽进 OS。作者连这期视频的提纲都是 grill 出来的。
- **让它自检**:用 dynamic workflow / Playwright 点一遍,按多种 persona(新手/工程师/老板)验证。把首过质量从 ~70% 拉到 ~92%。

## 💡 反共识 / 值得内化的判断框架

- **"Keys, not prompts" — prompt 永远不是权限层**。假设"只要它能,它就会"(能发邮件就可能真发)。血泪教训:一个 agent 误把折扣码群发给 **~15–20 万**邮件列表 → 公开道歉。解法:**scoped API key**(比如只读会议转录,不能改/删)。真正的护栏是"它根本没有那把钥匙",不是你 prompt 里写了"别做"。
- **你建的是"自己的 OS",不是"Claude Code 的 OS"**。底层只是 folders + markdown + skills + 路由逻辑。所以同时留 `CLAUDE.md` 和 `AGENTS.md`(codex)→ 换 harness/模型成本极低。"新模型发布要不要重建?不用,你学的是搭系统,不是学某个工具。"——这个视角能消解"追新焦虑"。
- **架构工程是新手艺**。继 prompt/context/harness engineering 之后,"architecture engineering"(目录/文件怎么组织)没有标准答案,判据就一条:对你直觉,且不浪费 token。
- **大项目 ≠ 爆 context**:深度嵌套的大项目,主目录 `/context` 起步仍只 ~40k token(多数是 system tools)。markdown 文件本身短期内不是瓶颈。

## ⚠️ 待你自测(视频含创作者口径,非客观事实)

- 视频把模型称作 "Claude Fable / Mythos 5" 并给了限时可用窗口与"2× Opus 价格(\$10/M in、\$50/M out)、压测 1 小时吃光 \$200 max 的 5 小时额度"——这些是 **2026-06 当时的创作者说法**,价格/可用性以你当前实际为准。(Fable 5 = `claude-fable-5` 确为真实模型。)
- Karpathy 的好评引用是营销背书,自行判断。

`#claude-code` `#second-brain` `#ai-operating-system` `#context-engineering` `#skills` `#permissions` `#subagents` `#mental-models`
