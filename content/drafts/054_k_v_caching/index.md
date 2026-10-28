---
title: 'Key Value Caching in LLMs'
date: '2026-10-27T13:07:45Z'
draft: false
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: ['ai']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

{{< figure src="./kv-whiteboard.jpg" width="700" align="center" alt="K,V caching mechanism on my whiteboard" caption="K,V caching mechanism on my whiteboard. The token under the dotted line represents the newest token" >}}

If you've been following my previous blogs, you might have seen that I've been going on an LLM training journey.

I started with building an LLM from scratch (training is still ongoing, by the way), and now I'm digging deeper into other topics such as K,V caching, Mixture of Experts, Reinforcement Learning, etc.

In this blog post I want to write down the intuition behind K,V caching and how it can be used to speed up inference once the model has been trained.

When you make predictions with an LLM, you predict each new token one by one. On each iteration, you give the model all previous tokens plus the newest one and use them to predict the next token.

Because of how LLMs work, the model doesn't just predict the token after the last one. For each token in the sequence, it predicts the next token. This is useful during training, but during inference we only care about the prediction for the last token. This means that on every iteration we re-compute a lot of the same operations that we then discard at the end.

{{< animation src="animations/kv-iterations.html" title="Every iteration redoes the whole sentence" >}}

So there's an opportunity to save ourselves some expensive compute by only calculating what we need each time. More specifically, in the attention mechanism we only need to calculate the attention scores once for each token. On any subsequent prediction, we only need to compute the attention scores for the new token.

{{< animation src="animations/kv-cache-runs.html" title="K,V caching: two runs, one cache" >}}

Skipping the re-computation of attention scores for the previous tokens is already a big resource saver! If we had a million tokens, we'd only need to calculate the attention scores for the last one. Think of the compute savings!

But there's one catch. Even though we don't need to re-calculate the previous attention scores when a new token comes in, we still need the keys and values of the previous tokens to compute the output of the new token. This is where K,V caching helps. Since the keys and values of previous tokens don't change from run to run, we can cache them instead of re-computing them each time, so they're readily available for the newest token.

This works because we use a mask on the attention scores to hide any tokens ahead of the current token. So even though the attention matrix changes (new values are added), the mask makes sure it doesn't affect the outputs of the previous tokens (attention scores × value vectors), because the new token always comes after them.

{{< animation src="animations/kv-cache-mask.html" title="Why the mask keeps old outputs fixed" >}}

This mask is the reason we can cache the keys and values instead of re-computing them each time.

Isn't this neat?
