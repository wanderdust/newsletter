---
title: 'Unpublished Confessions: Uninspired by AI'
date: '2025-10-09T08:05:18+01:00'
draft: true 
summary: ''
tags: ['productivity', 'AI']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

I am so uninspired by how AI can improve my productivity as a data engineer.

I am not going to deny that these tools can increase your productivity in some tasks that would otherwise take a much more longer time to do. The thing is, that the tasks that it can automate are usually the very boring ones. 

Lately I've been working on doing some migration work. I needed to migrate dozens of tables from one warehouse to another, having to create new airflow DAGs, ETL pipelines etc. If I had to do this job manually for all tables it would have been hell, and it would have taken months. Instead I was able to use windsurf with a re-usable prompt to duplicate the same steps for all pipelines, freeing me from having to type thousands of column names, data types and descriptions manually. All I need is to copy paste into a re-usable prompt.

Sure thing, I'd rather have AI write airflow DAGs than doing them myself. THe problem is that now that windsurf is capable of writting all the code and pipelines, I've basically became a copy paste machine. All of this copy pasting could be automated by some workflow or agent, the problem is that the copy paste jobs are a one off, where it is not worth spending the time developing something if it is going to take me the same time or less to copy paste what I need 50 times. Then, the copy pasting is not a one off, there are a few small copy paste jobs.

Of course, there is more beyond the copy pasting. I need to make sure the pipelines are tested before merging in production, I need to ensure table names, descriptions and columns are correct and that the correct data is arriving at the destination without hickups.

I just feel that if as a Data Engineer this is what my job is going to look like in the future, I'd rather start looking for a job in a new field.

Anyway, after writing this I realise this may not be an AI problem, but really it seems like I have a very boring job. Although I still find AI to increase productivity really boring.

See you next time.
