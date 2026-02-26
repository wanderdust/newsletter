#!/usr/bin/env python3
import os
import sys
import re
import shutil
from pathlib import Path

VALID_TAGS = {
    "ai", "aws", "career", "certifications", "data-engineering",
    "kubernetes", "postgres", "reflections", "security", "serverless",
    "testing", "tooling",
}

def validate_tags(post_dir):
    """Warn about unknown or missing tags in a post."""
    index_file = post_dir / "index.md"
    if not index_file.exists():
        return

    content = index_file.read_text()
    match = re.search(r'^tags:\s*\[([^\]]*)\]', content, re.MULTILINE)
    if not match:
        return

    raw = match.group(1)
    tags = [t.strip().strip("'\"") for t in raw.split(",") if t.strip()]

    if not tags:
        print(f"⚠️  Warning: Post has no tags. Valid tags: {', '.join(sorted(VALID_TAGS))}")
        return

    unknown = [t for t in tags if t not in VALID_TAGS]
    if unknown:
        print(f"⚠️  Warning: Unknown tag(s): {', '.join(unknown)}")
        print(f"   Valid tags: {', '.join(sorted(VALID_TAGS))}")

    if len(tags) > 4:
        print(f"⚠️  Warning: Post has {len(tags)} tags (max 4 recommended)")

def move_post(post_identifier, from_section="drafts", to_section="posts"):
    """
    Moves a post from one section to another (e.g., drafts to posts).
    Post identifier can be the full directory name or just the post number.
    """
    from_dir = Path(f"content/{from_section}")
    to_dir = Path(f"content/{to_section}")
    
    # Ensure directories exist
    if not from_dir.exists():
        print(f"Error: Source directory {from_dir} does not exist.")
        sys.exit(1)
    
    if not to_dir.exists():
        print(f"Error: Destination directory {to_dir} does not exist.")
        sys.exit(1)
    
    # Find the post directory
    post_dirs = [d for d in from_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    # Match by post number or full name
    matching_dir = None
    for post_dir in post_dirs:
        if post_dir.name.startswith(post_identifier) or post_dir.name == post_identifier:
            matching_dir = post_dir
            break
    
    if not matching_dir:
        print(f"Error: Could not find post matching '{post_identifier}' in {from_section}/")
        print(f"Available posts:")
        for post_dir in post_dirs:
            print(f"  - {post_dir.name}")
        sys.exit(1)
    
    # Move the post
    destination = to_dir / matching_dir.name
    
    if destination.exists():
        print(f"Error: Destination {destination} already exists.")
        sys.exit(1)
    
    try:
        validate_tags(matching_dir)
        shutil.move(str(matching_dir), str(destination))
        print(f"Successfully moved: {matching_dir.name}")
        print(f"From: {from_section}/")
        print(f"To:   {to_section}/")
    except Exception as e:
        print(f"Error moving post: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python move_post.py <post-number-or-name> [from-section] [to-section]")
        print("Example: python move_post.py 001 drafts posts")
        sys.exit(1)
    
    post_identifier = sys.argv[1]
    from_section = sys.argv[2] if len(sys.argv) > 2 else "drafts"
    to_section = sys.argv[3] if len(sys.argv) > 3 else "posts"
    
    move_post(post_identifier, from_section, to_section)
