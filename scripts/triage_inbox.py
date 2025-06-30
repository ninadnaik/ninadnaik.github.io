#!/usr/bin/env python3
"""
triage_inbox.py  –  Weekly research helper

• Finds Issues labelled `inbox`
• Fetches either:
    – the full readable text of a web article, OR
    – the auto-generated transcript of a YouTube video,
  falling back to your own note if fetching fails
• Sends that text to GPT-4o-mini:
    → returns 2 concise bullets + 1 essay tag
• Writes a markdown evidence file to research/processed/
• Comments “Processed ✅” on the Issue, relabels to `processed`
"""

import os, re, datetime, textwrap, requests, html2text
from pathlib import Path
from readability import Document
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from github import Github
from openai import OpenAI

# --------------------------------------------------------------------
# 1) Environment vars injected by the GitHub Action
# --------------------------------------------------------------------
REPO_NAME      = os.environ["GITHUB_REPOSITORY"]          # e.g. "ninadnaik/ninadnaik.github.io"
GH_PAT         = os.environ["GH_PAT"]
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

gh  = Github(GH_PAT).get_repo(REPO_NAME)
ai  = OpenAI(api_key=OPENAI_API_KEY)

# --------------------------------------------------------------------
# 2) Helpers to detect & fetch source content
# --------------------------------------------------------------------
URL_RE      = re.compile(r"https?://\S+")
YOUTUBE_RE  = re.compile(r"(?:youtu\.be/|youtube\.com/watch\?v=)([\w-]{11})")

def fetch_article(url: str) -> str | None:
    """Return cleaned article text or None on failure."""
    try:
        html = requests.get(url, timeout=10).text
        text = html2text.html2text(Document(html).summary())
        return text.strip()[:8000]          # cap to ~2k tokens
    except Exception:
        return None

def fetch_youtube(url: str) -> str | None:
    """Return YouTube transcript or None if unavailable."""
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

# --------------------------------------------------------------------
# 3) GPT-4o summary helper
# --------------------------------------------------------------------
def summarise(text: str) -> tuple[str, str]:
    """Return (two-bullet string, essay_tag)."""
    rsp = ai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                "Summarise the text below in EXACTLY two bullets (≤30 words each). "
                "Then suggest ONE essay tag that starts with 'essay:'. "
                "Return the three lines in that order.\n\n"
                f"{text}"
            )
        }],
        max_tokens=150,
    )
    lines   = rsp.choices[0].message.content.strip().splitlines()
    bullets = "\n".join(lines[:2]).lstrip("-• ").strip()
    tag     = lines[2].strip().lstrip("#") if len(lines) > 2 else "essay:untagged"
    return bullets, tag

# --------------------------------------------------------------------
# 4) Main triage loop
# --------------------------------------------------------------------
def main() -> None:
    for issue in gh.get_issues(labels=["inbox"], state="open"):
        raw_body = issue.body or ""
        url_match = URL_RE.search(raw_body)
        link      = url_match.group(0) if url_match else ""

        # ----- decide what content to summarise -----
        fetched = None
        if link:
            if YOUTUBE_RE.search(link):
                fetched = fetch_youtube(link)
            else:
                fetched = fetch_article(link)

        note_only   = URL_RE.sub("", raw_body).strip()
        source_text = fetched or note_only or "(no content fetched)"

        bullets, tag = summarise(source_text)

        # ----- format bullet list -----
        bullet_lines = "• " + bullets.replace("\n", "\n• ")

        # ----- write markdown evidence file -----
        filename = f"{datetime.date.today()}_{issue.number}.md"
        md_path  = Path("research/processed") / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)
        md_text = f"""---
source: {issue.html_url}
link: {link}
tags: [{tag}]
---
{bullet_lines}
"""
        md_path.write_text(textwrap.dedent(md_text))

        # ----- update Issue -----
        issue.create_comment(f"Processed ✅\n\n{bullet_lines}")
        issue.set_labels("processed")

if __name__ == "__main__":
    main()
