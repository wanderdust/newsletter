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

The thing is that this was intended. LLMs first go through a pre-training stage. Huge datasets of the whole internet are collected, and the model is simply trained to predict the next word. Imagine you train it on unstructured text from the internet, reddit, stackoverflow, social media etc. The model is simply going to replicate that format.

At this point it has no other purpose that blindly predicting a most likely next word. It doesn't know that it is meant to provide answers to question, let alone to provide helpful answers, or that they need to be provided in format that it is easy to consume.

The idea with pre-training, is that by training the model on huge amounts of data, something magical happens during training - it learns to generalise. This is where the model learns how write code, how to translate between languages etc, without us explicitly having to teach it. But to harness these capabilities out of the model, we need to further fine tuning.

The fine tuninng stage is where we teach the model about the format and structure of the answer. For a question answering model, we gather a dataset of questions and answers, and further train the model on it. For a coding model we might gather a dataset of coding questions with answers that are exclusively code.

By doing this, the model lears about the structure of our conversations with it. For Q&A model, it knows that every time we ask a question it needs to return an answer in the same format as provided in the fine tuning set. THe fine tuning stage does not take too much training, nor it requires a very large dataset.

![Example]

Finally, there's the alingment stage. At this point the model 'knows' how to format its answers every time we give it a prompt, but it doesn't necessarily provide helpful answers and it is likely that it will ignore many of our instructions. In order to aling the model to how we want it to behave, we can further train it using Reinforcement Learning.


During both the pre-training and fine tuning stages the model is trained word by word. We have a 'labelled' dataset of what the next word should be, and we check if the model has predicted the correct word or not. Based on the result the model learns until it is able to replicate the training dataset word for word.

With Reinforcement Learning we don't have a labelled dataset, instead we let the model produce an answer and we score it based on specific criteria. For a Q&A model, like chatGPT, we may score answers based on whether they respond to the actual question, whether the answer was easily readable, whether the markdown was correctly formatted etc. We give a higher score for answers that match the criteria, and take points away when some or all of the criteria isn't met. The goal of the model in this case is to maximise the score for every answer. Notice how we don't tell the model exactly what it needs to do, but rather we let it figure it out based on the scores it recieves. 'Good' answers that meet the criteria get good results, 'bad' answers get porrer results. THe model might start identifying patterns and ways to start producing good answers every time.

This is called the alignment stage, because we are ranking every answer based on how helpful each answer is. We are not just scoring the format, but also the content, and anything else that might be relevant for the use case. For a Q&A model like ChatGPT, we may use Reinforcement Learning with Human in the Loop. THis means that for each answer the model gives, the 'criteria' we rank it on is a person deciding if an answer is helpful or not. Over time the model learns patterns to create answers that 'humans' like.

But humans don't always need to be involved. For a coding LLM, the criteria might be things like: Does the code run? Does the code achive the task that was asked of it? Is the code broken down into functions? etc etc. The criteria depends on the use case. You may also decide to have an LLM judging some of the criteria, such as whether the answer actually answered the original question.



## In short, what's the difference beteewn fine tuning and reinforcement ltearning?

Fine tuning is about showing the model what 'good' answers might look like, word by word. The model learns the structure of how it should answer, but the model may be very unreliable in the helpfulness of the answers.

With reinforcement learning, we let the model produce a full answer each time and we evaluate it based on some criteria. We don't tell the model the exact answer we would have liked, but rather we tell the model what we liked and didn't like about the answer, and the model learns to maximise the score so that it can get good answers.
