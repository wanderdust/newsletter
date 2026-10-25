---
title: '053_difference_between_finetuning_and_rl'
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


For the past few weeks I've been going through the motions of training an LLM. An LLM typically goes through three stages: pre-training, fine tuning and alignment.

I remember the first time I was working with the LLAMA 7B model. When I first asked it to make a prediction, I was expecting a tidy output in question answering style, like I was used to from using ChatGPT. What I got instead, was more like an autocompletion model, and the answer of the model looked more like a stackoverflow extract, with the answer cut off half way before it was finished. In short, the model at that stage was pretty much useless

[Example prormt here]

The thing is that this was intended. LLMs first go through a pre-training stage. Huge datasets of the whole internet are collected, and the model is simply trained to predict the next word. Imagine you train it on unstructured text from the internet, reddit, stackoverflow, social media etc. The model is simply going to replicate that format. At this point it has no other purpose that blindly predicting a most likely next word. It doesn't know that it is meant to provide helpful answers, or that they need to be provided in format that it is easy to consume.

The idea with pre-training, is that by training the model on huge amounts of data, something magical happens during training - it learns to generalise. This is where the model learns how write code, how to translate between languages etc, without us explicitly having to teach it. But to harness these capabilities out of the model, we need to further fine tuning.

The fine tuninng stage is where we teach the model about the format of how we expect it to answer. For a question answering model, we gather a dataset of questions and answers, and further train the model on it. By doing this, the model lears about the structure of our conversations with it. For Q&A model, it knows that every time we ask a question it needs to return an answer in the same format as provided in the fine tuning set. THe fine tuning stage does not take too much training, nor it requires a very large dataset.

![Example]

Finally, there's the alingment stage. At this point the model 'knows' how to format its answers every time we give it a prompt. The model is perfectly usable at this point, and will give you uselful answers. But there is a trick to make the model even more alinged with the users, so that it can learn about answers that are more useful than others, preferred structures, answer lenghts etc.

THis is where Reinforcement Learning comes in. During pre-training and fine tuning, the model is trained based on each next word prediction. Every time the model predicts a word, we check against the real label, and check if the model predicted the same word. Essentially, the model learns to memorise the training set.

During Reinforcement learning, on the other hand we let the model predict a full answer. Once the answer is complete we have a set of criteria we use to evaluate if the answer was according to the format we expected. For example for a Q&A model we might want to evaluate things like: was the answer concise or was it long? Did it use short paragraphs? Did the answer actually answered the question? and any ather criteria



## So what's the difference beteewn fine tuning and reinforcement ltearning?
