#!/usr/bin/env python3
"""
triage_inbox.py  –  Weekly research helper (v2)

• Fetches article text or YouTube transcript (fallback: your note)
• Summarises into 3 paragraphs (~150 words) focused on AI-Book thesis
• Adds Tag + Stance metadata
• Skips irrelevant sources
• Writes markdown note → research/processed/
• Comments "Processed ✅" on Issue, relabels to processed
"""

import os, re, datetime, textwrap, requests, html2text
from pathlib import Path
from readability import Document
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from github import Github
from openai import OpenAI

# ── 1. ENV VARS ──────────────────────────────────────────────────────────────
REPO   = os.environ["GITHUB_REPOSITORY"]          # e.g. ninadnaik/ninadnaik.github.io
GH_PAT = os.environ["GH_PAT"]
OA_KEY = os.environ["OPENAI_API_KEY"]

gh  = Github(GH_PAT).get_repo(REPO)
ai  = OpenAI(api_key=OA_KEY)

# ── 2. URL helpers ───────────────────────────────────────────────────────────
URL_RE     = re.compile(r"https?://\S+")
YOUTUBE_RE = re.compile(r"(?:youtu\.be/|youtube\.com/watch\?v=)([\w-]{11})")

def fetch_article(url: str) -> str | None:
    try:
        html = requests.get(url, timeout=10).text
        text = html2text.html2text(Document(html).summary())
        return text.strip()[:8000]
    except Exception:
        return None

def fetch_youtube(url: str) -> str | None:
    vid = YOUTUBE_RE.search(url)
    if not vid:
        return None
    try:
        caps = YouTubeTranscriptApi.get_transcript(vid.group(1), ["en"])
        return " ".join(c["text"] for c in caps)[:8000]
    except TranscriptsDisabled:
        return None
    except Exception:
        return None

# ── 3. GPT-4o summariser ─────────────────────────────────────────────────────
def summarise(text: str) -> tuple[str, str, str] | None:
    """
    Returns (paragraphs, tag, stance) or None if model says SKIP.
    """
    prompt = (
        "You are building a knowledge base for a first-principles book on intelligence and AI.\n"
        "Core questions:\n"
        "A. What is intelligence?   B. How does human cognition work?\n"
        "C. Implications for machine intelligence.\n"
        "D. Can neural-net / LLM tech reach meaningful AGI?\n"
        "E. What should AGI mean & how to benchmark it?\n"
        "F. Societal/business impact only when it illuminates A-E.\n\n"
        "TASK\n"
        "1. Read the SOURCE below.\n"
        "2. Write THREE paragraphs (100–250 words total):\n"
        "   • ¶1  – Key claim or finding (cite a concrete fact/number/name).\n"
        "   • ¶2  – Implication for questions A-E (prefix with 'Implication:').\n"
        "   • ¶3  – One open question or contradiction this raises.\n"
        "3. End with two lines exactly:\n"
        "   Tag: essay:<slug-case-tag>\n"
        "   Stance: supportive | critical | neutral\n\n"
        "CONSTRAINTS\n"
        "- No filler phrases. Each paragraph must include at least one specific detail.\n"
        "- If SOURCE offers nothing relevant to A-E, reply exactly: SKIP — not relevant.\n\n"
        f"SOURCE (truncated 8 000 chars):\n<<<{text}>>>\nEND SOURCE"
    )

    rsp = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=380,
        temperature=0.4,
    )

    out = rsp.choices[0].message.content.strip()

    if out.startswith("SKIP"):
        return None

    *paras, tag_line, stance_line = out.splitlines()
    paragraphs = "\n".join(p.strip("•- ").rstrip() for p in paras if p.strip())
    tag    = tag_line.replace("Tag:", "").strip().lstrip("#")
    stance = stance_line.replace("Stance:", "").strip()

    return paragraphs, tag, stance

# ── 4. Main triage loop ──────────────────────────────────────────────────────
def main() -> None:
    for issue in gh.get_issues(labels=["inbox"], state="open"):
        raw = issue.body or ""
        link_match = URL_RE.search(raw)
        link = link_match.group(0) if link_match else ""

        fetched = None
        if link:
            fetched = fetch_youtube(link) if YOUTUBE_RE.search(link) else fetch_article(link)

        note_only   = URL_RE.sub("", raw).strip()
        source_text = fetched or note_only or "(no content fetched)"

        summary = summarise(source_text)
        if summary is None:
            issue.create_comment("Skipped – not relevant to book thesis.")
            issue.set_labels("skipped")
            continue

        paragraphs, tag, stance = summary

        # write MD
        filename = f"{datetime.date.today()}_{issue.number}.md"
        md_path  = Path("research/processed") / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_text = f"""---
source: {issue.html_url}
link: {link}
tags: [{tag}]
stance: {stance}
---
{paragraphs}
"""
        md_path.write_text(textwrap.dedent(md_text))

        # comment & relabel
        issue.create_comment(f"Processed ✅\n\n{paragraphs[:500]}…")
        issue.set_labels("processed")

if __name__ == "__main__":
    main()
