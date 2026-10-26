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


For the past few weeks I've been going through the motions of training an LLM. LLMs typically go through three stages: pre-training, fine tuning and alignment. Some of which use classical supervised learning and others, such as the alingment stage use Reinforcement Learning. I was having a bit of trouble fully understanding the need for the Reinforcement Learning stage, which is the reason for writing this blog.

I remember the first time I was working with the LLAMA 7B model. When I first asked it to make a prediction, I was expecting a tidy output in question answering style, like I was used to from using ChatGPT.

What I got instead, was more like an autocompletion model, and the answer of the model looked more like a stackoverflow extract, with the answer cut off half way before it was finished. The model was basically doing autocomplete on whatever input I was giving it, giving unstructured answers that were hard to read and din't necessarily provide any useful information regarding my query.


[Example prormt here and the 'ugly' output (html tags etc)]

The thing is that this was intended. LLMs first go through a pre-training stage. Huge datasets of the whole internet are collected, and the model is simply trained to predict the next word.

Imagine you train it on text from the internet: reddit, stackoverflow, social media etc. And for each word in the text, you task the model with predicting the next word. That's the whole traning setup.

As an output what you get is what I saw, a model that simply predicts the more likely word without any regard for how to give readable output or providing a helpful answer.

The model doesn't know the expected format of the conversation. After all it has been trained on texts that use different formats: forums (Q&A), blog posts, books, poetry, documentation and so on. It will just replicate the most likely format based on the input you give it.

The idea with pre-training, is that by training the model on huge amounts of data, something magical starts to happen - it learns to generalise about tasks its never been taught about before. This is where the model learns how write code, how to translate between languages etc, without us explicitly having to teach it. But to harness these capabilities out of the model, we need to further fine tune it.

The fine tuninng stage is where we teach the model about the format and structure of the answer. Essentially, for each fine tuning sample, we are telling the model the exact answer we expect out of it.

For a question answering model like chatGPT, we gather a dataset of questions and answers, and further train the model on it. For a coding model we might gather a dataset of coding questions with answers that are exclusively code.

By doing this, the model lears about the structure of our conversations. For a ChatGPT style model, it learns that every time we ask a question it needs to return an answer in the same format as provided in the fine tuning set. THe fine tuning stage does not take too much training, nor it requires a very large dataset.

![Illustrated example for ChatGPT of Q&A set. Same example for a Q&Code answers dataset. One illustrated example]

Finally, there's the alingment stage. At this point the model has learned via fine-tuning how to format its answers every time we give it a prompt, but it doesn't necessarily provide helpful answers and it is likely that it will ignore many of our instructions. In order to aling the model to how we want it to behave, we can further train it using Reinforcement Learning.


During both the pre-training and fine tuning stages the model is trained word by word. We have a 'labelled' dataset of what the next word should be, and we check if the model has predicted the correct word or not. Based on the result the model learns until it is able to replicate the training dataset into human-like outputs.

With Reinforcement Learning we don't have a labelled dataset, instead we let the model produce a full answer and we score it based on specific criteria.

![Examplel of how the model produces an answer and then we have some criteria we evaluate it on]

For a Q&A model like chatGPT, we may score answers based on criteria such as: did the response asnswer the actual question?, was it easily readable? was the markdown was correctly formatted? etc, and give a higher score for answers that match the criteria, and take points away when some or all of the criteria isn't met.

During reinforcement learning, the model only has one goal: to maximise the score for every asnwer.

Notice how we don't tell the model exactly what it needs to do, but rather we let it figure it out based on the scores it recieves. 'Good' answers that meet the criteria get good results, 'bad' answers get porrer results. THe model will start identifying patterns that produce answers that get high scores.

This is called the alignment stage because we are ranking every answer based on how helpful each answer is.

We are not just scoring the format, but also the content, and anything else that might be relevant for the use case. For a Q&A model like ChatGPT some of the criteria might be an actual person that ranks answers based on how they 'feel' and whether they are easily readable, useful or not. Essentially the human in the loop is the evaluator. This is what is know as Reinforcement Learning with Human in the Loop. Over time the model learns patterns to create answers that 'humans' find agreeable.

But humans don't always need to be involved. For a coding LLM, the criteria might be things like: Does the code run? Does the code achive the task that was asked of it? Is the code broken down into functions? etc etc. The criteria depends on the use case. You may also decide to have an LLM judging some of the criteria, such as whether the answer actually answered the original question.



## In short, what's the difference beteewn fine tuning and reinforcement ltearning?

Fine tuning is about showing the model what 'good' answers might look like, word by word. The model learns the structure of how it should answer, but the model may be very unreliable in the helpfulness of the answers.

With reinforcement learning, we let the model produce a full answer each time and we evaluate it based on some criteria. We don't tell the model the exact answer we would have liked, but rather we tell the model what we liked and didn't like about the answer, and the model learns to maximise the score so that it can get good answers.
