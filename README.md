# yt-learn

把 YouTube 上的 AI coding 技术视频压成「精华笔记」的个人学习管道。
面向资深工程师 —— 目标是**替你决策"这视频值不值得花时间看"**，并萃取真正有信息量的部分。

## 流程

```
urls.txt ──▶ ytlearn.py fetch ──▶ clean/*.txt ──▶ Claude 读文本总结 ──▶ notes/*.md ──▶ index.md
            (yt-dlp 下载+清洗，确定性)         (按 SUMMARY_SCHEMA，无需 API key)
```

- **脚本只做确定性的活**：下载字幕、清洗 VTT（去时间戳/标签/滚动重复/HTML 实体）、增量跳过、归档。
- **总结由 Claude 在对话里做**：读 `clean/*.txt`，按 [SUMMARY_SCHEMA.md](SUMMARY_SCHEMA.md) 输出中英混合笔记并打分（信噪比 1–5）。

## 用法

```bash
# 1. 把 YouTube 链接贴进 urls.txt（每行一个）
# 2. 下载 + 清洗
python scripts/ytlearn.py fetch
# 3. 看进度（哪些待总结）
python scripts/ytlearn.py status
# 4. 对 Claude 说："总结待总结的视频"
```

## 目录

| 路径 | 内容 | 入库 |
|------|------|:---:|
| `scripts/ytlearn.py` | 下载+清洗 CLI | ✅ |
| `notes/` | 单篇精华笔记 | ✅ |
| `knowledge/` `rejected/` | 高分(≥4) / 低分(≤2) 归档 | ✅ |
| `index.md` | 按评分排序的总表 | ✅ |
| `SUMMARY_SCHEMA.md` | 总结模板与排版规范 | ✅ |
| `raw/` `clean/` | 字幕原文与清洗产物 | ❌ 可重新生成 |

## 依赖

- Python 3.12+
- `yt-dlp`（`pip install -U yt-dlp`）
