---
title: "Teaching an Agent to Play Space Invaders, Revisited"
date: '2026-11-08T20:03:45Z'
draft: false
description: "In 2019 I tried to teach a Deep Q-Network to play Space Invaders and ran out of credits with an agent barely better than random. In 2026 I finally finished it on a home-lab RTX 2060."
summary: "In 2019 I tried to teach a Deep Q-Network to play Space Invaders and ran out of credits with an agent barely better than random. In 2026 I finally finished it on a home-lab RTX 2060."
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: ['ai']
categories: []
ShowToc: true
TocOpen: false
math: true
cover:
  image: "hero_2019_vs_2026_2x_poster.jpg"
  alt: "My 2019 agent and my 2026 agent playing Space Invaders side by side"
  caption: ''
  hiddenInSingle: true
images: []
---

## Introduction

In 2019 I set out to build an agent that could play Space Invaders. It was when I was first learning Machine Learning, and I never had the chance of completing the project. My free EC2 credits ran out, and I abandoned the project with an agent that could barely perform better than a random agent.

In 2024 I decided to resurrect the project. I had a job and I could easily afford to buy some EC2 credits to train the agent. However, it was impossible to get the project back and running: none of the libraries were pinned and some libraries were out of date and were no longer supported. In short, it was less effort to start the project from scratch.

This time I decided to use PyTorch instead of Keras, which my older version used. I went back to the papers and built the model from scratch based on the original 2013 paper [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/pdf/1312.5602v1.pdf). By the time the model was good to be trained I got stalled again. The thought of setting up AWS for model training was more work than I wanted to take on in my free time. So the project was abandoned once more.

In October 2026 I had the bright idea of resurrecting my good ol' gaming PC and turning it into a training machine: install Ubuntu Server and leave models running for days. After all, it's got an OK GPU by modern standards (an RTX 2060) and should be able to tackle a good range of ML training problems.

<!-- TODO: photo of the home-lab PC goes here (placeholder in the original doc) -->

With this new setup I was finally able to make my dreams come true, and train a reinforcement learning agent capable of deliberately playing Space Invaders!

Throughout this blog post I'll walk through my implementation then and now, comparing the results and performance.

{{< video src="hero_2019_vs_2026_2x.mp4" poster="hero_2019_vs_2026_2x_poster.jpg" alt="My 2019 agent and my 2026 agent playing side by side until both games end, at double speed" caption="2019 and 2026, side by side, at double speed. The 2019 agent's game ends on 235 points while the 2026 agent scores 2,050." >}}

## Domain Background

Reinforcement learning works by maximising a value function, where the agent chooses the actions that maximise the expected reward. Advances in deep learning, especially in computer vision, made it possible for reinforcement learning algorithms to use neural networks as function approximators. These work far better than older techniques when the state space is continuous, such as raw screen pixels.

Before LLMs were invented and OpenAI built programs to beat professional Go players, Atari games used to be the benchmark for reinforcement learning. The Deep Q-Network (DQN) algorithm was the first alorithm introduced capable of beating some of these arcade games(Mnih et al., 2013). In 2015 the same team showed, in a paper in the journal Nature, that a DQN could reach human-level scores across dozens of Atari games, all learnt from pixels with the same network and settings (Mnih et al., 2015).

The motivation for this project is to recreate that algorithm for Space Invaders and see how close I can get to a human player.

### Problem Statement

The problem can be framed as a Markov Decision Process (Sutton and Barto, 2018), where the agent is the learner making the decisions and the environment is the Atari emulator. At each time step t, the agent selects an action from a discrete set of actions A = {1, ..., K}. One time step later, as a consequence of that action, the agent receives a new state S(t+1) from the emulator as an image, and a reward R(t+1) based on how the score changed. Repeating this produces a trajectory:

{{< figure src="mdp_loop.png" alt="The agent-environment loop: the agent sends an action, the environment returns a new state and a reward" caption="The Markov Decision Process: the agent acts, and the environment answers with a new state and a reward." align=center >}}

$$
S_0, A_0, R_1, S_1, A_1, R_2, S_2, A_2, R_3, \ldots
$$

The goal of the agent is to select the actions that maximise the expected return. Future rewards are discounted by a factor γ per time step, so the return from time t is:

$$
G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}
$$

In Space Invaders the agent controls a cannon at the bottom of the screen with 6 actions: do nothing, fire, move right, move left, and move right or left while firing. Points come from shooting invaders, and the game ends when the agent has lost all 3 lives.

### Solution Statement

The solution is a Deep Q-Network: a convolutional neural network that looks at the last 4 frames and estimates how much future score each of the 6 actions is worth.

The agent chooses actions based on a policy π, a mapping from a state s to an action a. The action-value function gives the expected return if the agent starts in state s, takes action a, and follows the policy afterwards. Bellman's optimality equation expresses the value of any state in terms of the states that could follow it:

$$
Q^*(s, a) = \mathbb{E}\left[ R_{t+1} + \gamma \max_{a'} Q^*(S_{t+1}, a') \mid S_t = s, A_t = a \right]
$$

In temporal-difference learning this becomes an update rule applied at every step:

$$
Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left( R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t) \right)
$$

In traditional Q learning, there is a Q table which holds all the possible next state values for each possible action. For a non-discrete environment like Space Invaders, a table can't hold a value for every possible screen, it's simply not feasible. Instead, we use a convolutional network with weights *w* that approximates *Q* instead. The estimated return at the next step becomes the target, computed with a separate copy of the weights, w⁻, that stays fixed for a while (fixed Q-targets):

$$
y = R_{t+1} + \gamma \max_a Q(S_{t+1}, a; w^-) \qquad \Delta w = \alpha \left( y - Q(S_t, A_t; w) \right) \nabla_w Q(S_t, A_t; w)
$$

In practice the network is trained to minimise the Huber loss between y and its prediction. The Huber loss is squared for small errors and linear for large ones, so one surprising transition can't produce a huge gradient. In 2019 I used a plain squared error, which is much less forgiving.

To balance exploration and exploitation, the agent follows an ε-greedy policy. With probability ε it picks a random action, and otherwise it picks the action with the highest Q-value. ε starts at 1 (pure exploration) and is multiplied by 0.9985 after every game until it reaches a floor of 0.01, which run 2 reached after about 3,000 games.


## Project Design

### Deep Q Learning with Experience Replay

Training a neural network on its own experience is unstable: consecutive frames are highly correlated, and the targets move as the network learns, so the weights can diverge. Two techniques from the DQN papers deal with this:

- **Experience replay.** Each (state, action, reward, next state, done) tuple is saved in a replay memory of 100,000 transitions. Training batches of 32 are sampled at random from it, which breaks up correlated sequences and lets the agent recall unusual situations more than once. Frames are stored as 8-bit integers, so the full memory fits in about 6 GB of RAM.
- **Fixed Q-targets.** The targets are computed with a copy of the network, w⁻, which is only updated to match the live weights w every 10,000 steps. This decouples the target from the weights being updated.

The algorithm interleaves two processes. One plays the game and stores each transition in the replay memory. The other, every 4 steps, samples a batch and takes one gradient-descent step on it. In run 2, learning only starts once the memory holds 50,000 transitions, so the first updates aren't fitted to a handful of games. Run 1 started after just 500.

{{< figure src="dqn_algorithm.png" alt="Deep Q-learning with experience replay, as pseudocode" caption="The DQN algorithm from Mnih et al. (2013), as I included it in my 2019 proposal. The current version follows it, with the changes listed below." align=center >}}

### Datasets and Inputs

In the context of Reinforcement Learning, there is no fixed dataset, the agent generates its own data by playing. Rather than building my own Atari Simulator, I use the `ALE/SpaceInvaders-v5` environment from Gymnasium, the maintained successor to OpenAI Gym, which runs the original Atari 2600 game through the Arcade Learning Environment.

The agent only receives raw pixels, the same as a human sees on the screen, and it learns to play from scratch based on its own experience and rewards. Each input goes through these steps:

{{< figure src="raw_frames_lives.png" alt="Three raw Space Invaders frames showing the agent's starting position with 3, 2 and 1 lives left" caption="Raw input frames, showing where the agent starts with 3, 2 and 1 lives left." align=center >}}


The preprocessing pipeline of the images before it is fed into the model is as follows:
1. **Greyscale and resize.** The 210 × 160 colour frame becomes an 84 × 84 greyscale image.
2. **Frame skipping.** Each chosen action is repeated for 3 frames, so the agent decides 20 times a second rather than 60.
3. **Frame stacking.** The last M = 4 frames are stacked, so the agent can see movement, such as which way a bullet is travelling. The final state is 4 × 84 × 84.
4. **Scaling.** Pixel values are divided by 255 inside the network, so inputs sit between 0 and 1.
5. **Reward clipping.** For training, each reward is clipped to between −1 and +1, so every invader counts the same. The real, unclipped game score is recorded separately and is what I report.

In my original implementation back in 2019 I tried to write my own preprocessing pipeline with OpenCV. It was slow enough to crash my computer early in training.

{{< figure src="preprocessed_stack_2019.png" alt="Four consecutive preprocessed frames stacked as one input" caption="A stack of 4 preprocessed frames, as one input to the network. This is from my 2019 version, which cropped out the score and the ground and showed the frames in false colour. The current version keeps the full frame at 84 × 84." align=center >}}

I switched to the environment's own wrappers, which are much more efficient and easier to use.

{{< figure src="preprocessing_pipeline.png" alt="The current preprocessing pipeline: a raw colour frame, the 84 by 84 greyscale version, and the 4-frame stack the network sees" caption="The current pipeline, from the 2026 code: the raw 210 × 160 colour frame, the same frame in greyscale at 84 × 84, and the stack of the last 4 frames that the network actually receives. Look closely at the bullet between the cannon and the shields: it moves up between frames, which is how the agent can tell which way things are travelling." align=center >}}



### The network: starting small, then going bigger

My original 2019 implementation used the larger network as presented in the 2015 Nature paper, with a dueling head on top. But because it performed so poorly, when I rebuilt the project in 2024 I decided to take a step back, and use the smaller network originally presented in the 2013 paper. I also thought there was a chance I could try to train this on my MacBook. Spoiler alert, it still wasn't feasible.

As you'll see later in the results, the smaller network learned to play to some extent, replicating the results from the original paper, but it soon hit a ceiling.

{{< figure src="network_comparison.png" alt="The 2013 network next to the 2015 Nature network, layer by layer" caption="From src/q_function.py, before and after the November 2026 change." align=center >}}

Both networks take the same 4 × 84 × 84 input and output one Q-value per action. The Nature network adds a third convolutional layer and doubles the width of every other layer, which takes the parameter count from 677,686 to 1,687,206.



## Evaluation


### Metrics
The main metric is the agent's real game score, averaged over the last 100 games. In supervised learning you can split a dataset into training, validation and test sets. In reinforcement learning, evaluating the model isn't as straightforward, so I watch how the agent performs over time. Every game is logged with these numbers:

- **Game score.** The actual, unclipped Space Invaders score, the same number a human player would see on screen.
- **100-game moving average.** A single game is very noisy: the same agent can score 400 one game and 1,500 the next. The model with the highest 100-game average is saved separately as `best.pt`, so a later decline in training can't lose it.
- **Loss.** The Huber loss between the network's predictions and its targets. It doesn't fall steadily as it would in supervised learning. What matters is that it settles into a stable band rather than climbing without limit.
- **Epsilon and training time.** These show how much the agent is still exploring and how long each result took.

The scores I report are measured during training, where the agent still takes a random action some of the time.

For the final model, I evaluate the score over 100 games with no random moves.

### Benchmarks

The benchmark is a professional human games tester, who averaged 1,652 points in the 2015 Nature paper. In game terms, that's killing all the space aliens for about 3 rounds in a row.

The following table is a reference of the different benchmarks for the random agent, small and larger models as shown in the publications.

| Benchmark | Average score | Where it comes from |
| --- | --- | --- |
| Random agent | 148 | Nature paper, 2015 |
| DQN, small network | 581 | [Mnih et al., 2013](https://arxiv.org/pdf/1312.5602v1.pdf) |
| Professional human tester | 1,652 | Nature paper, 2015 |
| DQN, Nature network | 1,976 | Nature paper, 2015 |

{{< video src="random_agent.mp4" poster="random_agent_poster.jpg" alt="A random agent playing one game of Space Invaders and scoring 210 points" caption="A random agent scoring 210 points." >}}

## Training specs

Hardware and training specs across all three runs: the 2019 failed attempt, the first run on the small model in 2026 and the second run with the larger model in 2026.

### Hardware

|  | 2019 | 2026 (both runs) |
| --- | --- | --- |
| Machine | AWS EC2 p2.xlarge | Home PC |
| OS | Ubuntu Server | Ubuntu Server 26.04 LTS |
| GPU | NVIDIA Tesla K80 (one GPU, 12 GB) | NVIDIA GeForce RTX 2060 (6 GB) |
| CPU | 4 virtual CPUs | AMD Ryzen 5 3600 (6 cores, 12 threads) |
| RAM | 61 GB | 16 GB |
| Software | Python 3, TensorFlow with Keras, OpenAI Gym (SpaceInvaders-v0); versions not recorded | Python 3.10, PyTorch 2.14 with CUDA 13, Gymnasium 1.4, Arcade Learning Environment 0.12 |

### Training

|  | 2019 Run | Run 1: small network | Run 2: Nature network |
| --- | --- | --- | --- |
| Training time |  | 17 h 56 min | 31 h 37 min |
| Time to best model |  | 5 h 4 min | 27 h 10 min |
| Training steps | 29,000,000 | 28,218,535 | 44,845,815 |
| Games played | 40,000 | 29,288 | 28,667 |
| Speed |  | 436 steps a second | 394 steps a second |
| Gameplay seen | about 86 million frames, roughly 17 days of real life play | about 85 million frames, roughly 16 days of real life play | about 135 million frames, roughly 26 days of real life play |

Note: the keen eyed will have noticed that the 2019 model has played more games than the other 2 models, despite the training steps being much less than the better model. The reason is that models that perform better make the games last longer, so with similar training time a better model will play overall fewer games.

Training ran on my RTX 2060 with a single script I could leave running in the background. Before that, I briefly tried training on Google Colab, which kept disconnecting every two hours.

{{< figure src="nvtop_run2.png" alt="nvtop on the training machine during run 2: the RTX 2060 at about 37% utilisation, with the training script using 252 MiB of GPU memory, 462% CPU and 7.4 GB of RAM" caption="Run 2 training, watched with `nvtop` inside tmux. The GPU sits at about 37% utilisation, draws 40 of its 160 W, and runs at 39°C. The training script uses only 252 MiB of the GPU's 6 GB, but about 4.6 CPU cores and 7.4 GB of RAM, most of it the replay memory. The work is mostly on the CPU side, running the game." align=center >}}


## Results

Each attempt was better than the last. The 2019 wasn't any better than random play. The newer version with the smaller model was capable of deliberate gameplay to almost beat the first screen of aliens. The larger model was able to beat several screen of aliens with deliberate, strategic play.

| Attempt | Network | Training steps | Best average score |
| --- | --- | --- | --- |
| 2019, Keras | Nature-sized, with dueling head | about 29 million (estimated) | about 190 |
| 2026, run 1 | 2013 small network | 28.2 million | 503.5 |
| 2026, run 2 | Nature-sized network | 44.8 million | 1,175.6 |

Results summary:
- **2019 Run:** the trend line shows the model learnt a little, then went back down. Evaluated over 500 games, it averaged 190, barely above a random agent. I never had the chance to iterate over the code to find the reason of the failure.
- **Run 1 (small network):** learnt quickly, then stalled. Its best 100-game average was 503.5, after 8.0 million steps (5 hours). It then drifted down to 292 by the end, even though the loss stayed stable. Best single game: 1,695.
- **Run 2 (Nature network):** passed run 1's best after only 1.6 million steps, about an hour in, and kept improving slowly for the next 27 hours. Its best 100-game average was 1,175.6, after 38.5 million steps. After that it levelled off rather than collapsing, and its last 100 games averaged 1,045.7. Best single game: 2,830.

{{< figure src="chart_scores.png" alt="Average score over training for the 2019 agent, run 1 and run 2" caption="" align=center >}}

### Watching them play
All agents side by side vs the random benchmark:

{{< video src="progression_4up.mp4" poster="progression_4up_poster.jpg" alt="Four agents playing at the same time: random, 2019, run 1 and the final agent" caption="How the final agents from each of the runs compares to the random agent" controls="true" >}}

The two 2026 agents on their own, each playing a full game:

{{< video src="run1_small_network.mp4" poster="run1_small_network_poster.jpg" alt="The run 1 agent with the small network playing one game" caption="Run 1's best model playing one game: it scores 590 points. The model shows some signs of deliberate gameplay, but it is not very good at dodging bullets or moving strategically to fire on targets." controls="true" >}}

{{< video src="final_agent_best_game.mp4" poster="final_agent_best_game_poster.jpg" alt="The final agent's best game out of 10, playing with no random moves" caption="Run 2's best model, the final agent: scores 2,050 points over two and a half minutes of gameplay. The agent can clearly dogde bullets and fires mostly when there are targets on site." controls="true" >}}

### How good is the final agent?

The agent from the last run can clearly play the game. From the gameplay you can see it clearly dodging bullets as well as mostly firing only when there are targets on site.

Playing with no random moves, the best model from the last run averaged 1,111 points over 100 games, with a best game of 2,375 and a worst of 410. That's nearly double the 2013 DQN benchmark (581), but still below the professional tester (1,652) and the Nature DQN (1,976) benchmarks. Its best games beat both of those averages.

### What it learnt

{{< figure src="chart_action_mix.png" alt="Share of each action in run 2's first and last 1,000 games" caption="Action counts from run 2's train_log.txt, first and last 1,000 of 28,667 games." align=center >}}

Early in training, while the agent is mostly exploring at random, each of the 6 actions gets close to an even share. By the end it has learnt to move far more than it fires: plain left and right moves rise from about 15% each to about 21%, and the fire actions drop from about 53% of moves to 43%. It spends more of its time dodging and lining up shots, rather than firing constantly.

## Potential Improvements

These are the potential improvements that would certainly increase the model's capabilities to surpass the beforementioned benchmarks. It is likely that I won't revisit the project again, and although I could easily ask an LLM to implement these for me, there's no much fun in that.

1. **N-step returns.** Use the sum of the next 3 rewards as the target instead of just one. When the agent fires, the bullet takes dozens of steps to reach an invader, so the credit for a good shot should flow back faster. This is the cheapest change and, according to the Rainbow paper (Hessel et al., 2018), one of the two that matter most.
2. **Double DQN.** Let the live network choose the next action and the target network score it. This reduces the overestimation of Q-values, a common cause of scores declining late in training.
3. **Prioritised experience replay.** Replay the transitions the network got most wrong more often (Schaul et al., 2015). This is the one I couldn't get working in 2019.
4. **Dueling network.** Split the last layer into a state value and an advantage for each action, as I did in 2019 (Wang et al., 2015).

{{< figure src="dueling_network_2019.png" alt="A plain network next to a dueling network, which splits into two streams before the output" caption="From my 2019 attempt: the plain network next to the dueling network I used then. The dueling version splits after the convolutional layers into one stream for the state's value and one for each action's advantage, then combines them into the 6 Q-values." align=center >}}

## Closing thoughts

The goal I set in 2019 was to make an agent capable of playing Space Invaders. What I've got now is an agent that clearly understands the game, and is capable of beating the first level almost every time. In some games it scores higher than the human tester baseline at 1,652 points.

It's very unlikely that I'll revisit this project again, but it has been deeply satisfying to see this project realised. Reinforcement learning has a special place in my heart, and it makes me happy to finally have it successfully implemented.

This project has also opened my eyes to the incredible opportunities of AI assisted programming for ML work. While I built all of the model architecture myself, I used AI as an advisor for potential issues in the code or for advice on which parameters to pick. It has also been immensely useful to hand over all of the checkpointing, charts, logging and all other important yet tiresome and slow work to the agent, so I could simply focus on running the script and observing the results.

Next, I'll probably spend more time with language models. Now that I have my GPU home lab I can start training my own language models, which I'm very excited about.

Until next time!

----


## Appendix: detailed training charts

The full charts behind the summary in Results, including the training loss, which the summary chart leaves out.

### 2019 attempt

{{< figure src="training_2019.png" alt="2019 training: average reward per 50 and per 100 episodes over 40,000 episodes" caption="2019: average reward per 50 and per 100 episodes over 40,000 episodes of training." align=center >}}

{{< figure src="evaluation_2019.png" alt="2019 evaluation: average reward of the trained agent over 500 games" caption="2019: evaluating the trained agent over 500 games. The average settled at about 190." align=center >}}

At the time, I suggested that perhaps there were signs of deliberate play. In this sequence, the agent moves under cover to dodge an incoming bullet, however, this was likely a fluke, considering the agent barely got better than the random agent.

{{< figure src="taking_cover_2019.png" alt="Eight consecutive frames of the 2019 agent moving under cover to avoid a bullet" caption="2019: eight consecutive frames, left to right, of the agent &quot;taking cover to dodge a bullet&quot;." align=center >}}



### Log History of changes made

| Date | Change | Why |
| --- | --- | --- |
| Nov 2026 | Switched to the Nature-sized network | The small network hit a ceiling (see Results) |
| Nov 2026 | Adam optimiser (learning rate 0.0001) instead of RMSprop | RMSprop with PyTorch's default settings made jumpy updates, the likely cause of the decline in run 1 |
| Nov 2026 | Losing a life counts as the end of a sequence in the replay memory | The agent learns that dying cuts off future points, without restarting the game |
| Nov 2026 | Exploration floor lowered from 10% to 1%; learning waits for 50,000 transitions | Fewer random moves late in training; a less biased start |
| Oct 2026 | Discount factor raised from 0.9 to 0.99; faster ε decay | 0.9 only looks about 10 steps ahead, too short for a bullet to reach an invader |
| Oct 2026 | Replay memory raised from 10,000 to 100,000, stored as 8-bit | More varied memories without running out of RAM |
| Oct 2026 | Squared error replaced with Huber loss; learn every 4 steps | More stable updates, as in the papers. My 2019 version only learnt once per game |
| Oct 2026 | Pixel values scaled to between 0 and 1 | The network was being fed raw 0 to 255 values |
| Mar 2024 | Rewrote the project in PyTorch with the 2013 small network | A clean restart, starting small to train faster |
| Mar 2019 | Built the first model version |  |

### Run 1: small network

{{< figure src="progress_run1.png" alt="Run 1: training loss and game score for the small network over 28 million steps" caption="Run 1's training chart: 29,288 games and 28.2 million steps over 17 h 56 min. The loss stays stable, while the score peaks at about 8 million steps and then declines." align=center >}}

### Run 2: Nature network

{{< figure src="progress_run2.png" alt="Run 2: training loss and game score for the Nature-sized network over the full 44.8 million steps" caption="Run 2's training chart: 28,667 games and 44.8 million steps over 31 h 37 min. The loss settles early and stays stable, and the score keeps rising slowly until about 38 million steps." align=center >}}

## References

- Hessel, M., Modayil, J., van Hasselt, H., Schaul, T., Ostrovski, G., Dabney, W., Horgan, D., Piot, B., Azar, M. and Silver, D. (2018). [Rainbow: Combining Improvements in Deep Reinforcement Learning](https://arxiv.org/abs/1710.02298). *AAAI*.
- Mnih, V., Kavukcuoglu, K., Silver, D., Graves, A., Antonoglou, I., Wierstra, D. and Riedmiller, M. (2013). [Playing Atari with Deep Reinforcement Learning](https://arxiv.org/pdf/1312.5602v1.pdf). *arXiv*.
- Mnih, V., Kavukcuoglu, K., Silver, D., Rusu, A. A., Veness, J., Bellemare, M. G., Graves, A., Riedmiller, M., Fidjeland, A. K., Ostrovski, G., Petersen, S., Beattie, C., Sadik, A., Antonoglou, I., King, H., Kumaran, D., Wierstra, D., Legg, S. and Hassabis, D. (2015). [Human-level control through deep reinforcement learning](https://www.nature.com/articles/nature14236). *Nature*, 518.
- Schaul, T., Quan, J., Antonoglou, I. and Silver, D. (2015). [Prioritized Experience Replay](https://arxiv.org/abs/1511.05952). *arXiv*.
- Sutton, R. and Barto, A. (2018). *Reinforcement Learning: An Introduction*. 2nd ed. Cambridge, Massachusetts: The MIT Press.
- Wang, Z., Schaul, T., Hessel, M., van Hasselt, H., Lanctot, M. and de Freitas, N. (2015). [Dueling Network Architectures for Deep Reinforcement Learning](https://arxiv.org/abs/1511.06581). *arXiv*.

Project code: [original 2019 project](https://github.com/wanderdust/ML_nanodegree_udacity/tree/master/projects/capstone_project) · [current version](https://github.com/wanderdust/reinforcement-learning/tree/main/reinforcement_learning/deep_q_learning).
