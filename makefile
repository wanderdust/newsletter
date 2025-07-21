serve:
	uv run hugo server --buildDrafts --disableFastRender --cleanDestinationDir --ignoreCache

# Create a new blog post with automatic numbering
# Usage: make post name=my-post-name
post:
	@if [ -z "$(name)" ]; then \
		echo "Error: Post name is required. Usage: make post name=my-post-name"; \
		exit 1; \
	fi
	@python scripts/create_post.py "$(name)"

