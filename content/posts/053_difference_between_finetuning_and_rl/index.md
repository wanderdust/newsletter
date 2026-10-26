---
title: 'Difference between Fine Tuning and RL for LLMs'
date: '2026-10-26T12:13:26Z'
draft: false
summary: ''
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: [ai]
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

For the past few weeks I’ve been going through the motions of training an LLM. LLMs typically go through three stages: pre-training, fine tuning and alignment.

I was having a bit of trouble fully understanding how Reinforcement Learning stage helps with alignment, and how it differs from the fine tuning stage, which is the reason for writing this blog.

A few years ago, I was doing a contracting job as an ML engineer for an early stage startup. The founders had managed access to the brand new LLAMA 7B and 13B parameter models, and wanted me to fine tune it to better understand the capabilities of the model.

When I first got my hands in the model, I was expecting it to behave like ChatGPT. I'd give it a question, and it would give me a nice helpful answer.

What I got instead, was something like this:

Prompt:
```
How do I reverse a list in Python?
```

Output (including prompt):

```html
How do I reverse a list in Python?</title>
<meta name="description" content="Python list reverse">
</head>
<body>
<div class="question">
<p>I have a list <code>[1, 2, 3, 4]</code> and I want to get <code>[4, 3, 2, 1]</code>. I tried using a for loop but it's not working. Any ideas?</p>
<p>Thanks in advance!</p>
<span class="tags">python list</span>
</div>
<div class="answer">
<p>asked 3 years ago by user2918</p>
<p>You can use the <code>reverse()</code> method or slicing with <code>[::-1]</code>. The difference is that <code>reverse()</code> changes the original list while
```
Basically a not very useful autocomplete model.

But this was intended. In the pre-training stage, huge datasets of the whole internet (reddit, stackoverflow, social media etc.) are collected, and for each word in the text, the model is simply trained to predict the next word. That’s the whole training setup.


{{< figure src="./llm-sft.png" alt="Supervised learning process" caption="During Supervised training the model is tasked with predicting the next word" >}}

What you get is what I saw: a model that can produce grammatically correct text and code, without any regard for readable output or helpful answers.

It has been trained on texts that use different formats: forums (Q&A), blog posts, books, poetry, documentation and so on. It doesn’t know the expected format of the conversation and will just replicate the most likely format based on the input you give it.

The idea with pre-training is that by training the model on huge amounts of data, something magical starts to happen --- it learns to generalise about tasks we have never explicitly taught it, such as how to write code or translate between languages. But to harness these capabilities and make it useful, we need to further fine tune it.

The fine tuning stage is where we teach the model the format and structure of our interactions.

For each fine tuning training sample, we tell the model the exact answer we expect out of it. For a question answering model like ChatGPT, we gather a dataset of questions and answers and further train the model on it. Over time it learns that every time we ask a question it needs to return an answer in the same format.

Q&A dataset (ChatGPT style)

```json

{"question": "How do I reverse a list in Python?",
 "answer": "You can reverse a list in two ways:\n\n1. `my_list[::-1]` returns a new, reversed list.\n2. `my_list.reverse()` reverses the original list in place.\n\nUse slicing if you want to keep the original list unchanged."}

{"question": "What is the capital of France?",
 "answer": "The capital of France is Paris."}
 ```

 For a coding model we might gather a dataset of coding questions with answers that are exclusively code.

Q&A for a coding model

```json

{"question": "How do I reverse a list in Python?",
 "answer": "def reverse_list(my_list):\n    return my_list[::-1]"}

{"question": "Write a function that checks if a number is even.",
 "answer": "def is_even(n):\n    return n % 2 == 0"}
```

This stage does not take too much training, nor does it require a very large dataset.

Finally, there’s the alignment stage. At this point the model has learned how to format its answers, but it doesn’t necessarily provide helpful answers and is likely to ignore many of our instructions. To align the model to how we want it to behave, we further train it using Reinforcement Learning.

During both the pre-training and fine tuning stages the model is trained word by word: we have a ‘labelled’ dataset of what the next word should be, and we check if the model has predicted the correct word. The model learns until it is able to replicate responses with the same format as the training dataset.

With Reinforcement Learning we don’t have a labelled dataset; instead we let the model produce a full answer and score it based on specific criteria.

{{< figure src="./rl-llms.png" alt="Reinforcement learning process" caption="Reinforcement learning process" >}}

For a Q&A model like ChatGPT, we may score answers based on criteria such as: _did the response answer the actual question? Was it easily readable? Was the markdown correctly formatted?_ Answers that match the criteria get a higher score, and we take points away when some or all of the criteria isn’t met.

Notice how we don’t tell the model exactly what it needs to predict or how. The model learns this itself based on the scores it gets. Its only goal is to maximise the score for every answer, so it starts identifying patterns that produce answers that get high scores.


This is called the alignment stage because we are ranking every answer based on how helpful it is. We don't just score the format, but also the content and anything else that might be relevant for the use case.

For ChatGPT, some of the criteria might be an actual person ranking answers based on how they ‘feel’ and whether they are easily readable and useful. This human in the loop is the evaluator, which is what's known as Reinforcement Learning with Human Feedback. Over time the model learns to create answers that ‘humans’ find helpful and agreeable.

But humans don’t always need to be involved. For a coding LLM, the criteria might be things like: _Does the code run? Does the code achieve the task that was asked of it? Is the code broken down into functions?_ You may also decide to have an LLM judging some of the criteria, such as whether the answer actually answered the original question.

To summarise, what’s the difference between fine tuning and reinforcement learning?

Fine tuning is about teaching the model about how we want our answers structured, word by word. It will still be very unreliable and won't follow any instructions. Given that it's been trained on twitter, stackoverflow and reddit data, it is also likely to be very mean.

With reinforcement learning, we let the model produce a full answer and evaluate it based on some criteria. We don’t tell the model the exact answer we would have liked, but rather we give the answer a score based on what like about it. The model wants to maximise the score, so it learns patterns to create high scoring answers, therefore converging in a model that produces answers that are correct and helpful.
