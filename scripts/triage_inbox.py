#!/usr/bin/env python3
"""
triage_inbox.py  –  weekly helper for AI-Book project

• Looks for GitHub Issues labelled 'inbox'
• Summarises each Issue with GPT-4o-mini
• Saves a markdown note into research/processed/
• Relabels the Issue to 'processed' and leaves a comment
"""

import os, datetime, textwrap
from pathlib import Path

# --- 3rd-party libs installed by the workflow ---
from github import Github        # PyGithub
from openai import OpenAI        # official client

# --------------------------------------------------------------------
# 1) Auth keys come from GitHub Action secrets
# --------------------------------------------------------------------
REPO_NAME = os.environ["GITHUB_REPOSITORY"]   # e.g. "ninad/personal_website"
GH_PAT    = os.environ["GH_PAT"]
OPENAI_KEY = os.environ["OPENAI_API_KEY"]

gh      = Github(GH_PAT).get_repo(REPO_NAME)
openai  = OpenAI(api_key=OPENAI_KEY)

# --------------------------------------------------------------------
def summarise(text: str) -> tuple[str, str]:
    """
    Call GPT-4o to get 2 bullets + 1 tag.
    Returns (bullets, tag)
    """
    resp = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": (
                "Summarise the text below in **exactly two bullets**. "
                "Then propose **one essay tag** that starts with 'essay:'. "
                "Return three lines: bullet1, bullet2, tag.\n\n"
                f"{text}"
            )
        }],
        max_tokens=120,
    )
    lines = resp.choices[0].message.content.strip().split("\n")
    bullets = "\n".join(lines[:2]).lstrip("-• ").strip()
    tag     = lines[2].strip().lstrip("#")
    return bullets, tag or "essay:untagged"

# --------------------------------------------------------------------
def main():
    for issue in gh.get_issues(labels=["inbox"], state="open"):
        body = issue.body or "(no body)"
        bullets, tag = summarise(body[:4000])   # safeguard length

        # Path: research/processed/YYYY-MM-DD_<issue#>.md
        filename = f"{datetime.date.today()}_{issue.number}.md"
        md_path  = Path("research/processed") / filename
        md_path.parent.mkdir(parents=True, exist_ok=True)

        md_path.write_text(textwrap.dedent(f"""\
            ---
            source: {issue.html_url}
            tags: [{tag}]
            ---
            • {bullets.replace('\n', '\n• ')}
        """))

        # Comment & relabel on the Issue
        issue.create_comment(f"Processed ✅\n\n• {bullets.replace(chr(10), '\n• ')}")
        issue.set_labels("processed")

if __name__ == "__main__":
    main()
