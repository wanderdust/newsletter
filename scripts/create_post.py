#!/usr/bin/env python3
import os
import sys
import re
import subprocess
from pathlib import Path

def get_next_post_number():
    """
    Determines the next post number by finding the highest existing post number
    and incrementing it by 1.
    """
    posts_dir = Path("content/posts")
    
    # Ensure the posts directory exists
    if not posts_dir.exists():
        print(f"Error: Posts directory {posts_dir} does not exist.")
        sys.exit(1)
    
    # Get all directories in the posts directory
    post_dirs = [d for d in posts_dir.iterdir() if d.is_dir() and not d.name.startswith('.')]
    
    # Extract post numbers using regex
    highest_num = 0
    pattern = re.compile(r'^(\d+)_')
    
    for post_dir in post_dirs:
        match = pattern.match(post_dir.name)
        if match:
            num = int(match.group(1))
            highest_num = max(highest_num, num)
    
    # Return next number formatted as 3-digit string
    return f"{highest_num + 1:03d}"

def slugify(text):
    """
    Convert a title to a slug format (lowercase with underscores).
    """
    # Remove special characters and convert spaces to underscores
    slug = re.sub(r'[^\w\s]', '', text.lower())
    slug = re.sub(r'\s+', '_', slug)
    return slug

def create_new_post(post_name):
    """
    Creates a new Hugo post with the provided name and the next sequential number.
    """
    next_number = get_next_post_number()
    slug = slugify(post_name)
    post_dir_name = f"{next_number}_{slug}"
    post_path = f"content/posts/{post_dir_name}"
    
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
        print("Usage: python create_post.py <post-name>")
        sys.exit(1)
    
    post_name = sys.argv[1]
    create_new_post(post_name)
