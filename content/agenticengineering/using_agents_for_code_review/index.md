---
title: 'Chapter 8 - Using agents for code review'
date: '2026-03-06T13:50:36Z'
draft: true
summary: ''
tags: ['ai', 'tooling']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
params:
  showtoc: true
  tocOpen: false

---

## Resources
- [There Is an AI Code Review Bubble](https://www.greptile.com/blog/ai-code-review-bubble) - Honest take on why most AI code review tools are fundamentally limited. Shallow diff-only reviews produce noise, not signal. ([HN discussion, 351 points](https://news.ycombinator.com/item?id=46766961))
- [How We Made Our AI Code Review Bot Stop Leaving Nitpicky Comments](https://www.greptile.com/blog/make-llms-shut-up) - Practical deep-dive into the #1 problem: LLMs leave too many low-value comments. Details what worked and what didn't to reduce noise. ([HN discussion, 257 points](https://news.ycombinator.com/item?id=42451968))
- [Google Engineers Launch Sashiko for Agentic AI Code Review of the Linux Kernel](https://www.phoronix.com/news/Sashiko-Linux-AI-Code-Review) - AI code review applied to one of the most demanding environments: high-stakes, low-level C code with strict quality standards. ([HN discussion](https://news.ycombinator.com/item?id=47427647))
- [Get an AI Code Review in 10 Seconds](https://oldmanrahul.com/2025/12/19/ai-code-review-trick/) - DIY, no-nonsense approach to lightweight AI code reviews using existing tools. ([HN discussion, 142 points](https://news.ycombinator.com/item?id=46346391))
- [Benchmarking GPT-5 on 400 Real-World Code Reviews](https://www.qodo.ai/blog/benchmarking-gpt-5-on-real-world-code-reviews-with-the-pr-benchmark/) - Systematic benchmark of LLM performance on real pull requests, not synthetic examples. ([HN discussion](https://news.ycombinator.com/item?id=44833929))
