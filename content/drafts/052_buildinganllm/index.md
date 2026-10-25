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

It's been a while since I've done any sort of model training, so it's been really exciting to finally get to build and train an LLM from scratch. This blog is a list of of intuitions I've learned from implementing and traning a Large (small really) language model on a dataset of short stories.


THe motivation for this project was to finally learn how LLMs work. I've tried to get the intuition for the attention mechanism for a very long time now, but nothing really clicked. Eventually I came across [this blog post on the LLM architecture](https://poloclub.github.io/transformer-explainer/) on hacker news where I could easily peek into each of the sections of the LLM. The fact that the whole madel could be illustrated in a single page made me think that it couldn't be that complicated after all, so I decided to give it a go.

## Intuitions from implementing the model

The following is a list of intuitions and things learned from working on this project.

### To understand the model, first draw it in the whiteboard

Before trying to implement anything, I wanted to properly understand each of the concepts. I started by drawing the architecture in my whiteboard. This was helpful, because by working through a specific example, I was forced to think about the size of the matrices as each point, so I really had to think about the operations at each point the inputs sizes and the ouptut sizes.

{{< figure src="./llm-whiteboard.jpg" alt="Description for screen readers" caption="Please ignore my note at the top right which is meant to remind me to get a spare wheel for my car. Also, please appreciate my 3rd prize at the village flower show, won by showcasing my wonderful apples" >}}

### It helps to see the difference between learned weights and the forward pass

One of the first things I noticed was the difference between what are learned weights in the model vs what operations are only part of the forward pass. This is quite obvious to me right now, but when you first learned about attention, you learn about how the Q,K,V matrices are combined with the token embeddings to calculate the attention scores, which are then added back to the original embedding. All of these operations are only part of the forward pass, when we are making a prediction. But the only thing that is learned is the Q,K,V matrix.

While diagramming, I could differentiate between learned matrices, and operations that are only executed during the forward pass. In my diagram, if you look closely, you can see that I illustrated this by adding a green dot in front of anything that was 'learned'. With this visual aid I could easily differentiate what's learned vs what's part of the forward pass.

Seeing how _few_ components are learned made the model a lot simpler to understand.


### Positional embeddings are learned

I was following the GPT2 architecture, which is was the first LLM that showed good generalisation capabilites.

One of the bigger surprises, was to find out the the positional embeddings - which are added to the token embedding to show its position in the sentence vs the other words - are learned. Unlike RoPE embeddings which aren't learned, the positional embeddings are defined as set of embeddings which are learned during training. There is one embedding per position of the token in the sentence.

For some reason, I expected postional encoding to be an array of 1,2,3,4..., for each token based on its position on the word. Instead, the positional encoding is another matrix learned during training. This makes sense, because the model can do a much better job of learning about positions than using simple integers.

### The job of the Q,K,V matrix is learn about the context around the word

The attention mechanism was one of the things that has evaded my understanding for a very long time. For the last 5 years I've read mulitple papers and blog posts about attention. But none of them really clicked. Like I said earlier, diagramming the whole thing helped me visualise what's learned vs what's done during the feed-forward operation. This is what really made it click in my head.

In terms of the intuition of attention, it really helped to discuss with Claude back and forth about why this and not that. To me, the attention score made already made sense - you multiply each 'token embedding' by all other embeddings embeddings in the sentence to get a score which tells you how much each word "attends" to the other words in the sentence. Then, you take this score and add it back to the original embedding so that it has context about the whole sentence.

![Diagram]

What I didn't get was the intuition of the Q,K,V matrix. I kept wondering why do you need it at all? Why not multiply the token embeddings directly to get a score?

After a back and forth with Claude I came to the conclussion that we could theoretically skip the Q,K,V, and the model would probably train, and perhaps even work well. By doing this however, we are putting too many responsibilties into the token embedding, which would be in charge of encoding this information on top of learning about the meaning of the words themselves. During training ,the token embedding would be in charge of both learning the **encoding** of the word, and learning about the **context** of the word.

By creating the attenion matrices Q,K,V we are essentially splitting the responsabilities. The token embeddings are in charge, and only in charge of learning the representation of a word, without any context. It learns about words, and how they are similar to other words. But for example, for the word _wave_ it won't know if it refers to the sea, or a person saying hello.

On the other hand, the attention matrices are purely in charge of learning about the context of the words. THese matrices learn to which words the current word should _attend_ to in the sentence. It is all about the context, and not the word itself.

In theory, rather than using Q,K,V matrices we could use a single one. But by breaking it down into different ones we follow the same pattern to break it down as to not give too many responsibilities to a single matrix. The Query matrix is is chargge of encoding the (todo). The Key matrix encodes the (todo). And the value matrix encodes the (todo).

### Multi Headed attention is a simple slice of the resulting Q,K,V matrices

I was also pleasently surplised to see that multi-headed attention is as simple as slicing the output embeddings into n smaller arrays, and then computing the attention score in parrallel for each of them. Nothing fancy going on, simply slice, compute, and then glue all the smaller embeddings into the one to make it the same size as the original. Nothing really fancy going on there.

![Diagram]

### Projection matrices are cool!

As mentioned above, the results from the attention head are smaller vectors that are concatenated before the MLP layer to bring the vector back to its original size. But simply concatenating the results mean that each of the smaller vectors does not know about the other vectors. THis is a missed opportunity.

To fix this, we add an extra step, called a projection matrix. Essentially, we pass the resulting vector via a one layer MLP which outputs a vector of the same size. This single layer MLP (or matrix if you prefer thinking of matrices) is to 'combine' the knowledge of all he output heads into a vector that is aware of all of its parts. This projection matrix, or MLP layer, is learned during training. It's job is to learn how to best combine the different concatenated outputs from the heads so that the vector is self aware.

![Diagram]

### The MLP layers of the attention block is a simple 2 layer network

With LLMs, it seems that most of the work is done in the attention layer, because the fully connected layers of the model are suprisingly simple. For each attention block, we only have 2 fully connected layers. That's it. The only goal of the layer is to expand the embedding to a bigger size (2x or 4x) and then bringing it back to its original size. The idea behind it being that by expanding it, we can encode more detail into the embedding before bringing it back to its original size.

![Diagram]

### The output layer (head) of the LLM is a simple single layer model

Same idea with the final layer of the model. It is simply a fully connected network that expands the final embedding into an output which has the same size as the number of tokens available in our model. Each output represents the probability that each token will be predicted next. The token with the larges probability is the next word in the prediction.

Finally, I finally realised - despite having heard and read this many times - that it comes down to the size of the dataset plus the size of the model's parameters. If you stack enough attention blocks on top of each other, and trained on a dataset the size of the internet, the model will eventually learn to generalise. The LLm model itself is quite simple.

## Extras

### Once you compose all the components of a model, it ends up as a single function

THis is probably something that I learned when I was first learning ML, but that I forgot along the way. It was really cool to remind myself that neural networks, as complex as they look, once you compose all of the parts, they end up just being a single function that learns to recognise complex patterns. When an input goes in, the learned patterns in the network are able to 'predict' the right answer.

![Latex example of model with 2 neurons. Show the 'expanded' version and then the single function with all the parts ie resolved version]


### Without Non-Lineal layers, a neural network cannot learn complex patterns

The other super cool reminder about Deep Neural Networks is how if you don't add non-linearity the model resolves to a simple linear function. Non-linearity (Relu, Gelu etc) is what makes the lines squiggly. This is best explained with an example

Example one, a simple linear model with no RELU
- Two neurons. Single input. Show how the ax + b once you compose it resolves to a linear funciton (show latex of how we resolve the equation by composing the layers and the final result. Also show the diagram of what the final line looks like)

Example two, a simple linear model with RELU
- Same as before. Show how the final drawn function has 'complex' patterns that are non linear.



## Looking ahead

I'm currently training the LLM on the stories dataset. Once this completes with a good enough loss, I plan to fine tune the model so that it goes from simple next word prediction, into a useful question answering model. Lastly, I want to do alignment so that the model responds according to my preferences by using Reinforcement Learning.


### Extras



------




### Lessons Learned




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
