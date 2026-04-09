#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from pathlib import Path


def get_next_post_number():
    """
    Determines the next post number by finding the highest existing post number
    across both posts/ and drafts/ and incrementing it by 1.
    """
    highest_num = 0
    pattern = re.compile(r"^(\d+)_")

    for section in ("posts", "drafts"):
        section_dir = Path(f"content/{section}")
        if not section_dir.exists():
            continue
        for d in section_dir.iterdir():
            if d.is_dir():
                match = pattern.match(d.name)
                if match:
                    highest_num = max(highest_num, int(match.group(1)))

    return f"{highest_num + 1:03d}"


def slugify(text):
    """
    Convert a title to a slug format (lowercase with underscores).
    """
    # Remove special characters and convert spaces to underscores
    slug = re.sub(r"[^\w\s]", "", text.lower())
    slug = re.sub(r"\s+", "_", slug)
    return slug


def create_new_post(post_name, section="drafts"):
    """
    Creates a new Hugo post with the provided name and the next sequential number.
    """
    next_number = get_next_post_number()
    slug = slugify(post_name)
    post_dir_name = f"{next_number}_{slug}"
    post_path = f"content/{section}/{post_dir_name}"

    # Create the post using uv and Hugo
    command = ["uv", "run", "hugo", "new", "content", f"{post_path}/index.md"]

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(f"Successfully created new post: {post_path}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error creating post: {e}")
        print(e.stderr)
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python create_post.py <post-name> [section]")
        sys.exit(1)

    post_name = sys.argv[1]
    section = sys.argv[2] if len(sys.argv) > 2 else "drafts"
    create_new_post(post_name, section)
