.PHONY: help serve post ready

help: ## Show this help message
	@echo "Available commands:"
	@echo ""
	@echo "  make serve        - Start Hugo development server with drafts"
	@echo "  make post name=X  - Create a new post in drafts/ (e.g., make post name=my-post)"
	@echo "  make ready post=X - Move a post from drafts/ to posts/ (e.g., make ready post=001)"
	@echo "  make help         - Show this help message"
	@echo ""

serve: ## Start Hugo development server
	uv run hugo server --buildDrafts --disableFastRender --cleanDestinationDir --ignoreCache

post: ## Create a new blog post with automatic numbering in drafts (usage: make post name=my-post-name)
	@if [ -z "$(name)" ]; then \
		echo "Error: Post name is required. Usage: make post name=my-post-name"; \
		exit 1; \
	fi
	@python scripts/create_post.py "$(name)"

ready: ## Move a post from drafts to posts (usage: make ready post=001)
	@if [ -z "$(post)" ]; then \
		echo "Error: Post identifier is required. Usage: make ready post=001"; \
		exit 1; \
	fi
	@python scripts/move_post.py "$(post)"

