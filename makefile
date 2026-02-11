serve:
	uv run hugo server --buildDrafts --disableFastRender --cleanDestinationDir --ignoreCache

# Create a new blog post with automatic numbering in drafts
# Usage: make post name=my-post-name
post:
	@if [ -z "$(name)" ]; then \
		echo "Error: Post name is required. Usage: make post name=my-post-name"; \
		exit 1; \
	fi
	@python scripts/create_post.py "$(name)"

# Move a post from drafts to posts (publish it)
# Usage: make ready post=001
ready:
	@if [ -z "$(post)" ]; then \
		echo "Error: Post identifier is required. Usage: make ready post=001"; \
		exit 1; \
	fi
	@python scripts/move_post.py "$(post)"

