---
title: 'Difference between Fine Tuning and RL'
date: '2026-10-25T12:13:26Z'
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

For the past few weeks I’ve been going through the motions of training an LLM. LLMs typically go through three stages: pre-training, fine tuning and alignment, some of which use classical supervised learning and others, such as alignment, use Reinforcement Learning. I was having a bit of trouble fully understanding the need for the Reinforcement Learning stage, which is the reason for writing this blog.

The first time I asked the LLAMA 7B model to make a prediction, I was expecting a tidy output in question answering style, like I was used to from ChatGPT.

What I got instead was a model doing autocomplete on whatever input I was giving it. The answers looked more like a stackoverflow extract, cut off half way, unstructured, hard to read, and didn’t necessarily provide any useful information regarding my query.

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


The thing is that this was intended. In the pre-training stage, huge datasets of the whole internet (reddit, stackoverflow, social media etc.) are collected, and for each word in the text, the model is simply trained to predict the next word. That’s the whole training setup.

What you get is what I saw: a model that can produce grammatically correct text, without any regard for readable output or a helpful answer. It has been trained on texts that use different formats: forums (Q&A), blog posts, books, poetry, documentation and so on, so it doesn’t know the expected format of the conversation and will just replicate the most likely format based on the input you give it.

The idea with pre-training is that by training the model on huge amounts of data, something magical starts to happen - it learns to generalise about tasks we have never explicitly taught it, such as how to write code or translate between languages. But to harness these capabilities out of the model, we need to further fine tune it.

The fine tuning stage is where we teach the model the format and structure of the answer. For each fine tuning sample, we are telling the model the exact answer we expect out of it. For a question answering model like ChatGPT, we gather a dataset of questions and answers and further train the model on it, so it learns that every time we ask a question it needs to return an answer in the same format. For a coding model we might gather a dataset of coding questions with answers that are exclusively code. This stage does not take too much training, nor does it require a very large dataset.


Q&A dataset (ChatGPT style)

```json

{"question": "How do I reverse a list in Python?",
 "answer": "You can reverse a list in two ways:\n\n1. `my_list[::-1]` returns a new, reversed list.\n2. `my_list.reverse()` reverses the original list in place.\n\nUse slicing if you want to keep the original list unchanged."}

{"question": "What is the capital of France?",
 "answer": "The capital of France is Paris."}
 ```

Q&A for a coding model

```json

{"question": "How do I reverse a list in Python?",
 "answer": "def reverse_list(my_list):\n    return my_list[::-1]"}

{"question": "Write a function that checks if a number is even.",
 "answer": "def is_even(n):\n    return n % 2 == 0"}
```


Finally, there’s the alignment stage. At this point the model has learned how to format its answers, but it doesn’t necessarily provide helpful answers and is likely to ignore many of our instructions. To align the model to how we want it to behave, we further train it using Reinforcement Learning.

During both pre-training and fine tuning the model is trained word by word: we have a ‘labelled’ dataset of what the next word should be, and we check if the model has predicted the correct word. Based on the result the model learns until it is able to replicate the training dataset into human-like outputs. With Reinforcement Learning we don’t have a labelled dataset; instead we let the model produce a full answer and score it based on specific criteria.

![Examplel of how the model produces an answer and then we have some criteria we evaluate it on]

For a Q&A model like ChatGPT, we may score answers based on criteria such as: did the response answer the actual question? Was it easily readable? Was the markdown correctly formatted? Answers that match the criteria get a higher score, and we take points away when some or all of the criteria isn’t met.

Notice how we don’t tell the model exactly what it needs to do. Its only goal is to maximise the score for every answer, so it starts identifying patterns that produce answers that get high scores.

This is called the alignment stage because we are ranking every answer based on how helpful it is, not just scoring the format, but also the content and anything else that might be relevant for the use case. For ChatGPT, some of the criteria might be an actual person ranking answers based on how they ‘feel’ and whether they are easily readable and useful. This human in the loop is the evaluator, which is what is known as Reinforcement Learning with Human in the Loop. Over time the model learns to create answers that ‘humans’ find agreeable.

But humans don’t always need to be involved. For a coding LLM, the criteria might be things like: Does the code run? Does the code achieve the task that was asked of it? Is the code broken down into functions? You may also decide to have an LLM judging some of the criteria, such as whether the answer actually answered the original question.

In short, what’s the difference between fine tuning and reinforcement learning?

Fine tuning is about showing the model what ‘good’ answers might look like, word by word. The model learns the structure of how it should answer, but may be very unreliable in the helpfulness of its answers.

With reinforcement learning, we let the model produce a full answer and evaluate it based on some criteria. We don’t tell the model the exact answer we would have liked, but rather what we liked and didn’t like about it, and the model learns to maximise the score.
