---
title: "What I've learned from training an LLM"
date: '2026-10-23T09:01:31+01:00'
draft: true
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

It's been a while since I've done any sort of model training, so it's been really exciting to finally get to build and train an LLM from scratch. This blog post will mostly be a list of things I've learned from building and training this model.


## The Setup

- Built LLM
- Tiny Stories dataset
- Talk about the 3 stages of training: pre-training, fine tuning and alignment (RL)
- Next word prediction

For this project, I've built an LLM and trained it on a small dataset of short stories. The goal was to get an intuition of the architecture of LLMs, how they are built and trained.



## Lessons Learned




- LLM architecture is surprisingly simple, perhaps even more than LSTMs. Originally I thought they were going to be a lot more complex because of their capabilities, but in the end it is just 4 blocks.

1) token encoding
2) Positional embeddings (learned)
3) Attention Block + MLP
4) output head.

[add illustration]

- Models can be composed to a single fn: all the model layers can be combined into a single function. This is probably something I learned back in the day, but I forgot about the intuition then.

[add illustration]

Resolve this:

```
E → xw + zw + b
E → Cw + Dw + b
E → w₁(Aw₂ + C) + w₃(
```

- If you don't add non-linearity the model resolves to a simple linear function. Non-linearity (Relu, Gelu etc) is what makes the lines squiggly

[add illustration]

*Add example with and without Relu. Example should show final "line" function in graph compared for both*

- Attention intuition makes sense. I originally thought that the QKV matrices didn't really make sense. I did get the intuition of the attn mechanism: we multiply each token embedding by all other words in the sentence to find out how important each word in the sentence is to the current word.

  The QKV matrices are a way to split responsibilities in the model. You could in theory skip QKV and multiply the token embeddings directly to get the attention scores. The embedding would then update accordingly. However, the token embeddings in this case would be doing to many things. It's job would be both, capturing the "meaning" of a word as well as capturing the "context" of a word as compared to others.

  By creating the attention matrix, we separate responsibilities. The token embeddings capture the meaning of a word, without any context. The attention matrix is then purely in charge of capturing the context of a word. Split responsibilities.

- Multi-head attention is surprisingly simple. What I originally thought a complex thing, simply consists of slicing the QKV into n vectors, as per number of heads and compute them simultaneously. At the end all the vectors are concatenated into a full vector again.

[add illustration]

- LLMs makes building models easy. If you know what you want to build you can use LLMs to build a SOTA model of any kind. Of course if you don't have the overall intuition of what you're building you will come across many issues that are easily learned in ML 101: train/val split, contamination, validation etc. So really, ML now really comes down to 1) Having good data 2) Knowing how to deploy the models (MLOps/LLMOps). Everything else (the code) the model can do. I'm no longer limited by my pytorch knowledge or my ability to understand and implement SOTA papers into a model. As long as I have the intuition I can prompt away

  eg: update LLM architecture to use RoPE embeddings instead of current learned embeddings.

[add illustration]

  → Side note → really excited about building self-training harness for building and training models.

- It's all about Data size and Model size (not entirely). After having built a model myself, I've seen how simple LLM architecture is. Considering it's amazing capabilities. It really all comes down to how much data you have available and how many parameters you can build your model. Of course that's not everything. As we're seeing in recent models, there's a limit to how much data and how big you can make the model before not getting any more gains. That's why a lot of effort goes into test time compute, that is doing fine tuning and reinforcement learning on pre-trained models to instill further capabilities such as chain of thought or tool usage which greatly increases the capabilities of LLMs.
