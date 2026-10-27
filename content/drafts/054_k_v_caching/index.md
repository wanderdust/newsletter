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

In this blog post, I want to write down the intuition for K,V caching and how it can be used to speed up inference once the model has been trained.


Essentially, when you are making predictions with an LLM, you predict each new word one by one. For each iteration, you give the model all previous words in the sentence plus the newest one and use that to predict the next new word.

Because of how LLMs work, the LLM doesn't just predict the last word. For each word in the sentence, it predicts a next word. This is useful during training, but during inference, we only care about the last word. What this means is that for every iteration, we re-compute a lot of the same operations that we then discard at the end.

{{< animation src="animations/kv-iterations.html" title="Every iteration redoes the whole sentence" >}}


So there's an opportunity to save ourselves some expensive compute by only calculating the values that we need each time. More specifically, in the attention mechanism, we only need to calculate the scores once for each word/token. On any subsequent prediction, we only need to compute the attention score for the new word.


{{< animation src="animations/kv-cache-runs.html" title="K,V caching: two runs, one cache" >}}

By skipping having to re-compute the attention score for the previous tokens, it is already a big saver resource-wise! If we had a million tokens to compute, we'd only need to calculate the attention score for the last one. Think of the compute savings!

But there's one catch. Even though we don't need to calculate the previous attention scores when a new word comes in, we still need the keys and values to compute the results of the new token. This is where K,V caching helps.

Since the Keys and Values from previous tokens do not change from run to run, we can cache them to save us from re-computing them each time. Then they are readily accessible to calculate the attention scores of the newest word.

The reason this works is because we use a mask in the attention scores to hide any tokens ahead of the current token. That means that even though the attention matrix changes its values (new values are added), the mask makes sure it does not affect the updated values * attention vector, because the new token always comes after the earlier words.

{{< animation src="animations/kv-cache-mask.html" title="Why the mask keeps old outputs fixed" >}}

This mask is the reason why we can skip computing the values each time.

Isn't this neat?
