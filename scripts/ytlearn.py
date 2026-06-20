#!/usr/bin/env python3
"""
ytlearn — YouTube 技术视频学习管道（确定性部分）

只做机械活：下载元数据 + 字幕 -> 清洗 -> 输出干净 .txt。
语义层的总结/打分由 Claude 在对话里读 clean/*.txt 完成（baseline 不需要 API key）。

用法:
    python ytlearn.py fetch              # 处理 urls.txt 里所有未处理的视频
    python ytlearn.py fetch <URL>...     # 只处理指定 URL
    python ytlearn.py status             # 看哪些已下载/已清洗/已总结/待总结
"""
import html
import json
import re
import subprocess
import sys
import time
from pathlib import Path

# 让中文输出在 Windows 控制台不乱码，免去手动设 PYTHONUTF8
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
URLS_FILE = ROOT / "urls.txt"
RAW_DIR = ROOT / "raw"        # 原始 .vtt + .info.json
CLEAN_DIR = ROOT / "clean"    # 清洗后的 .txt（喂给 Claude）
NOTES_DIR = ROOT / "notes"    # Claude 产出的总结
for d in (RAW_DIR, CLEAN_DIR, NOTES_DIR):
    d.mkdir(parents=True, exist_ok=True)

# 字幕语言：AI coding 视频绝大多数是英文，只抓英文以减少请求、降低 429。
# 需要中文时把 zh-Hans 加回来。
SUB_LANGS = "en,en-US,en-GB,en-orig"


def read_urls():
    if not URLS_FILE.exists():
        return []
    out = []
    for line in URLS_FILE.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        out.append(line)
    return out


def video_id(url):
    """从 URL 抽 11 位视频 id；抽不到就退回用 yt-dlp 查。"""
    m = re.search(r"(?:v=|youtu\.be/|/shorts/|/embed/)([A-Za-z0-9_-]{11})", url)
    if m:
        return m.group(1)
    try:
        r = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--get-id", "--no-warnings", url],
            capture_output=True, text=True, timeout=60,
        )
        vid = r.stdout.strip().splitlines()
        if vid:
            return vid[0]
    except Exception:
        pass
    return None


# --- VTT 清洗 -------------------------------------------------------------

_TS = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s*-->")
_INLINE = re.compile(r"<\d{2}:\d{2}:\d{2}\.\d{3}>")          # 内联 timing
_TAG = re.compile(r"</?c[^>]*>")                              # <c> 着色标签
# 行内/整行的音效标记，如 [music] [Applause] [laughter]（自动字幕常见）
_CUE = re.compile(r"\[(music|applause|laughter|inaudible|noise)\]", re.I)


def clean_vtt(text):
    """把自动/人工 VTT 变成连续干净文本，去时间戳、去标签、去滚动重复行。"""
    lines = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if line == "WEBVTT" or line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        if _TS.match(line) or "-->" in line:
            continue
        if line.isdigit():  # cue 序号
            continue
        line = _INLINE.sub("", line)
        line = _TAG.sub("", line)
        line = _CUE.sub("", line)            # 去行内 [music] 等
        line = html.unescape(line)           # &gt; &amp; &#39; → > & '
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        lines.append(line)

    # 去自动字幕的滚动重复。只在“真重叠”时合并，避免误删短句：
    #  - 完全相同；或
    #  - 一条是另一条的前缀/后缀（滚动字幕的典型形态），且较短那条够长
    deduped = []
    for line in lines:
        if deduped:
            prev = deduped[-1]
            short, long = sorted((line, prev), key=len)
            rolling = long.startswith(short) or long.endswith(short)
            if line == prev or (rolling and len(short) >= 12):
                if len(line) > len(prev):
                    deduped[-1] = line
                continue
        deduped.append(line)

    # 拼成段落（句末标点后换行，便于阅读）
    joined = " ".join(deduped)
    joined = re.sub(r"([.!?。！？])\s+", r"\1\n", joined)
    return joined.strip()


def find_vtt(vid):
    cands = sorted(RAW_DIR.glob(f"{vid}*.vtt"))
    # 优先人工字幕（文件名不含语言自动后缀差异时，取第一个英文）
    for c in cands:
        if ".en" in c.name:
            return c
    return cands[0] if cands else None


def load_info(vid):
    f = RAW_DIR / f"{vid}.info.json"
    if not f.exists():
        # yt-dlp 有时按标题命名，兜底搜一下
        for cand in RAW_DIR.glob("*.info.json"):
            try:
                if json.loads(cand.read_text(encoding="utf-8")).get("id") == vid:
                    return json.loads(cand.read_text(encoding="utf-8"))
            except Exception:
                continue
        return {}
    try:
        return json.loads(f.read_text(encoding="utf-8"))
    except Exception:
        return {}


def fetch_one(url):
    vid = video_id(url)
    if not vid:
        print(f"  ! 无法解析视频 id: {url}")
        return
    clean_path = CLEAN_DIR / f"{vid}.txt"
    if clean_path.exists():
        print(f"  - 跳过（已清洗）: {vid}")
        return

    print(f"  ↓ 下载: {vid}")
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--skip-download",
        "--write-info-json",
        "--write-subs", "--write-auto-subs",
        "--sub-langs", SUB_LANGS,
        "--sub-format", "vtt",
        "--sleep-requests", "1",       # 请求间隔 1s，降低 429 概率
        "--retries", "5", "--retry-sleep", "exp=2:60",  # yt-dlp 内置指数退避
        "--no-overwrites", "--no-warnings",
        "-o", str(RAW_DIR / "%(id)s.%(ext)s"),
        url,
    ]
    # 撞 429 时再做一层脚本级退避重试
    r = None
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode == 0 or find_vtt(vid):
            break
        if "429" in r.stderr or "Too Many Requests" in r.stderr:
            wait = 30 * (attempt + 1)
            print(f"  ~ 撞到 429，等 {wait}s 后重试 ({attempt + 1}/3)…")
            time.sleep(wait)
            continue
        break

    # 容错：只要拿到字幕就继续清洗，不因某个语言/info.json 失败而整体放弃。
    vtt = find_vtt(vid)
    if not vtt:
        last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else r.returncode
        print(f"  ! 无字幕可用: {last}")
        return
    if r.returncode != 0:
        print(f"  ~ 部分失败但已拿到字幕，继续清洗（{r.returncode}）")

    info = load_info(vid)
    title = info.get("title", "")
    channel = info.get("channel") or info.get("uploader", "")
    dur = info.get("duration", 0)
    upload = info.get("upload_date", "")
    body = clean_vtt(vtt.read_text(encoding="utf-8", errors="ignore"))

    header = (
        f"# {title}\n"
        f"- video_id: {vid}\n"
        f"- channel: {channel}\n"
        f"- duration: {dur // 60}m{dur % 60}s\n"
        f"- upload_date: {upload}\n"
        f"- url: https://youtu.be/{vid}\n"
        f"- words: {len(body.split())}\n\n"
        "---\n\n"
    )
    clean_path.write_text(header + body, encoding="utf-8")
    print(f"  ✓ 清洗完成: {vid}  ({len(body.split())} 词)  {title[:50]}")


def cmd_fetch(args):
    urls = args if args else read_urls()
    if not urls:
        print("没有 URL。把 YouTube 链接加到 urls.txt（每行一个），或作为参数传入。")
        return
    print(f"待处理 {len(urls)} 个视频：")
    for u in urls:
        fetch_one(u)
    print("\n完成。接下来对 Claude 说：'总结 clean 目录里待总结的视频'。")


def noted_ids():
    """从 notes/ 里抽出已总结的 video_id。
    笔记文件名是 `<评分>-<slug>.md`，video_id 存在正文里，所以靠内容判重而非文件名。"""
    ids = set()
    if NOTES_DIR.exists():
        for p in NOTES_DIR.glob("*.md"):
            txt = p.read_text(encoding="utf-8", errors="ignore")
            for m in re.findall(r"(?:video_id:\s*|youtu\.be/|v=)([A-Za-z0-9_-]{11})", txt):
                ids.add(m)
    return ids


def cmd_status(_args):
    cleaned = {p.stem for p in CLEAN_DIR.glob("*.txt")}
    noted = noted_ids()
    pending = sorted(cleaned - noted)
    print(f"已清洗: {len(cleaned)}   已总结: {len(noted)}   待总结: {len(pending)}")
    if pending:
        print("\n待总结（喂给 Claude）:")
        for vid in pending:
            first = (CLEAN_DIR / f"{vid}.txt").read_text(encoding="utf-8").splitlines()[0]
            print(f"  {vid}  {first.lstrip('# ')[:60]}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    args = sys.argv[2:]
    if cmd == "fetch":
        cmd_fetch(args)
    elif cmd == "status":
        cmd_status(args)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
