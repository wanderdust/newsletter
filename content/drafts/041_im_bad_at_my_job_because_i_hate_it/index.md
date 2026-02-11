---
title: '041_im_bad_at_my_job_because_i_hate_it'
date: '2026-02-11T08:28:05Z'
draft: false
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

Today's something has happened that has affected my confidence as an engineer. In a Pull Request review to build a data pipeline in spark, I was told to review some "unwanted changes from the AI in my PR". And this has hit me in the soul. Why? Because I believe a good engineer should always own their code, no matter if they use AI or not. They should make high quality PRs they own, with code they can defend. And today that wasn't me. I let the AI do its thing and make a PR without really verifying the results too much. It has shuttered my confidence into making me feel like a junior being told to pay more attention.

The funny thing, is that I am well aware that the quality of my work is bad because I don't like my job. When I first got into programming, I got into it because it was so fun. I was so addicted not only to build things, but I was also obsessed with learning "best practices". With every new project I built, I could see the different and improvement of my code, every time looking more orginised, more readable, more beautiful.

Fast forward to today, and I'm working as a Data Engineer building data pipelines. I never really wanted to be a Data Engineer in the first place, but life doesn't really care much about that.  When I first joined my current company, I entered as a platform engineer. I'm not going to lie and say I loved my job back then, there were good times and bad times. But I had the opportunity to be surrounded by a (mostly) fantastic team, with many role models. I was learning a lot, which means I was enjoying myself.

It is funny, when you work with extremely talented people who are open to collaborate and want to help you grow, it does something amazing for your self confidence. It makes you feel confident about your job, and your skills. It gives you the confidence that you can reach the next level. On the other hand, when you end up in a team of people of work that you are not excited about, and a team of nice people but with no role models, then that confidence goes away. Suddenly room for growth seems harder, mainly because of lack of motivation and learning.

I don't like building pipelines. I've been trying to motivate myself into enjoying the role. Trying to tell myself that it is not about the pipelines, but about the business value these pipelines bring. But that's not enough. I am so demotivated to do my job that I've been relying on AI to try and build all the Airflow Dags and Spark code that I don't have the motivation to build myself.

To be fair with myself, I have pushed the coding agents really far into building spark code and airflow dags with little input from my side, except providing the specs for the data pipelines. I have got to a point where I can provide the specs, and the agents spin up a local version of Airflow (something that wasn't available before I set it up), run the Dag, check the logs, fix the issues and try again until the dag runs end to end. At the end it uses the databricks MCP server to validate the tables based on the specs.

This setup can automate things and get you there 90% of the way, but the last 10% still requires a human in the loop. That human in the loop needs to validate all the data transformations are correct, and that the output table does indeed contains the right data. This last part is what gives you ownership over your AI creation. And this last part is the part I have no motivation to do. I just make a PR and suffer the consequences of getting a "bad" review.

On the bright side, ever since I was made to join this team, I have created documentation on how to use our in-house Airflow platform, something that was never there before, and I've also shared numerous guides on how to be able to test pipelines locally using a local instance of Airflow and Databricks Connect. If nothing else this should be enough to tell myself I'm pushing the team forward into better engineering practices.

Unfortunately that is not enough. All it takes is someone to point out I made a sloppy PR because I used AI and didn't really check my work (which I didn't) to make me feel like shit. And I should feel like shit, because the standards are dropped. But I can't help but not give a shit because I don't like my job. But then, I can't help it but to feel shit when the inevitable bad PR rivew comes my way.
