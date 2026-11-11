---
title: '057_deploy_open_weights_llm_api'
date: '2026-11-09T08:56:30Z'
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

Structure of the blog post

1) Intro: why it makes sense to deploy open weights - (open models are very capable, your data stays within the company)

2) The hardware: RTX, ubuntu server etc, othes specs

3) The LLM: Qwen 4B with tools, llama.cpp API server

4) THe deployment: Kubernetes with K3s, the specs, what the url looks like with the service

5) Calling the deployed model: What it looks like, OPENAPI specs, stateless models, what streaming looks like


6) Calling the model via PI harness from my laptop to use as coding agent.

7) Hardware conmuption/performance, memory, GPU, idle resources etc


8) Commentary on scalability for real prod envs (lots of GPU required, KEDA for proper autoscaling needs), monitoring, costs

----

Open Weights models are becoming more and more capable, with many organizations wondering whether they should deploy and manage their own. Earlier this yeor the CTO of IBM (find article) said that open weights models are getting good enough to make sense to use them instead. This approach also makes sense if you want your data to stay within your company, and not go to third parties.

The purpose of this article is to find out what it takes to deploy an Open Weights model over an API. I'll be using Kubernetes to manage the deployment and scalability. Once the model is deployed I'll use the PI harness (link) to test the model for coding capabilities and speed.

## The Hardware

This project will be deployed in my own GPU homelab running ubuntu server. The machine runs an RTX 2060 with 6GB of vRAM, which is a fairly old card for today's standards, but good enough to run some of the smaller models. For referecnce, this GPU is similar to AWS's g4dn.xlarge which costs ~0.54$/hour.

The specs of my graphics card is what will limit the model size. In my case I only have one GPU, which means I can't scale to more than one instance. In a production environment you'd have several nodes available when needed for scaling.

## The model

For the model I'll use Qwen3.5 with 4 Billion parameters. This is a model trained on coding, trained on using tools. This is the kind of model that would be deployed internally for software engineers to use. This model can then be integrated with a coding harness like pi.dev

The reason for using this model is because is as much as I can fit in the virtual memory of the card. The model size is about 2.79GB (which is loaded into the 6GB memory). The rest of the vRAM is needed to fit the KV cache, which is needed for fast responses.

The next larger model is 9 Billion parameters which sits at 5.68 GB without accounting for the memory needed for the KV cache. This model would leave no room for KV cache, making it very useless for my specs.


## The deployment

The model will be deployed as an API. The model will be deployed as a centralised service in kubernetes, and users (me) will be able to use an URL with an API key to use the model for coding tasks.

[diagram]

The model will be deployed as a kubernetes deployment. I use K3s, a minimal version of Kubernetes that runs in my homelab. The kubernetes deployment will consist of a deployment, configmap, secret, service and hpa (horizontal pod autoscaling).

[Diagram]

The deployment defines the image, storage and configuration used in the individual pods. At the container level you define which image your pos will be running, and the environment variables and config to load. For this use case I'm using llamma.cpp (link), which is a ready to use API server for open weights models. 

[deployment config]

The deployment is coupled with a service, which is the interface with which we interact with the pods. The service gives us a single url/ip which uses basic load balancing to call our pods holding the llm. The service maps the URL and port number to the pods.

[service config]

The environment variables will be loaded in a configmap, which define model parameters such as which model to use, context size, quantization. Any model configuration is defined here. In this case we can se we are using Qwen 3.5 4B model with context size of [add ctx size used inutally (3k)].

[configmap]

Another interesting setting is the `LLAMA_ARG_N_PARALLEL=1`, which defines how many calls in parallel the model can handle. Any more concurrent calls on top of the setting will wait until earlier exectuions are finished. Also, the context is divided between the four slots, so each one gets a slice of the total context size. In my case, due to my limitations with vRAM I've set this to 1 (since I'm going to be the only user). Depending on your specs, you can tweak this to fit your needs. This is also a parameter that determines the number of concurrent users, so this can be tweaked based on stress tests to find out the sweet spot of the max concurrency the instance can hold. Based on this you can then setup autoscaling accordingly.

The next part is the horizontal autoscaling. In my case I've set it up to scale up to 2 instances if CPU usage goes over 70%. This is pointless for 2 reasons. First, CPU usage is not the right metric to track here, a better metric would be VRAM memory usage or number of queued requests. However vanilla Kubernetes only allows HPA trakcing for CPU and memory (pc memory not GPU memorp). To track these other more useful metrics we could use KEDA instead, but this is out of scope for this project because of the next reason.

Secondly, I only have one GPU in my setup. Even when autoscaling triggers (which it does), the new pods will fail to load because there are no more available nodes. The reason I've setup HPA in this project is for illustrative purposes, and to check HPA does work for the defined settings.

[hpa config]

Finally, there's the secret which holds the API key needed to call the API. As everyone using kubernetes knows, secrets are not necessarily secret, the values are simply base64 ecnoced. In a production environment it might be better to load your secrets from a secret vault instead.

[secret config]

Once the model is deployed we can access the API by calling using the homelab's IP and the port such as
```bash
curl 192.168.1.45:8080/....
```

## Testing the API

Before we setup the coding harness, we can test the model by calling the API directly.

[curl here w response]

As we can see, the API returns a JSON obect following the OpenAI API standards. It returns information such as .... (add some of the more relevant things from the response).

We can also call the API using streaming instead, a much more useful approach so that we don't have to wait for the full answer to be ready, we can read it as it gets generated, as we're alroady used to from every single LLM app out there.

[curl here with streaming and response.]

As we can see the response is fragmented into multiple resposes, one per token (verify this).

One thing worth knowing is that the API is stateless, which means calling the API again won't remember our previous conversation unless we add it the next call. This is the reason why context size grows so large as conversations go longer and longer. In our case, we don't need to worry about this, because the coding harness will handle this for us.

[example like jay almarrs]


## Using the model in a coding harness

To make the model useful, I'll use pi.dev harness. This harness is the open source version of codex or claude code, and it can connect to our API (becasu it uses a standard response) to handle our coding tasks.

To make this similar to a real life production example, I install pi in my personal laptop rather than on the machine running the model. THis is similar as if you were deploying the model on EC2s and running the harness from your local setup.

[Diagram]

Once pi is installed, add the following config to ~/.pi/models.json (check that's the actual path).

```json
{}
```

And don't forget to add the API key to your environment. To make sure it loads automatically you can add it to your ~/.bashrc or ~/.zshrc.

```bash

export API_KEY ....

```

Then we can run pi harness, and if everything went well, you'll see your model being loaded. We can start using it for coding tasks. In this example I ask it to some tests for my project.

[video with pi working]


## Testing the performance

When I first started using the model, I realised that I ran out of context after a few prompts. Coding agents require a generous context size, and it is not very useful it only allows a handful of prompts before it errors out. I check my settings and I find out two issues. First, my context size is set to 3k (get correct figure), which is clearly not large enough. The bigger issue is that I originally had LLM_Parallell (get correct name) set to 2, which means the context size available for that node gets halfed. So all I'm getting is 1.5k context size which is not great. For reference 1.5k tokens is around ~1,100 words which is about 2 pages in an essay. The context size includes the response too. A 1.5K slot can't take a 1-page essay and write a 1-page response.

[Add screenshot if I have it]

Qwen 3.5 can hold up to 262K tokens, but because context size is loaded into memory as KV caching, I'm limited to the amount of context I can take. LLama.cpp reserves the memory it needs ot startup as the instance starts, so I can use nvtop to check the amount of memory used by nvtop. The amouth of memory is the model size + the context size. 

The following image is the nvtop with my initial setup (2 concurrent, 3k)

[nvtop]

Since I'm the only user, I set LLM_parallel to 1, this will give access to the full context size for all my sessinos. However, 3k context size is still very small. Based on my nvtop, my memory usage is already pretty close to 100%. What I do is use fp8 (check that is the actual thing I used) instead the q16 (check if that's the correct one from initial setup.). THis helps reduce memory and I can increase my context size to 6k (get exact number).

When I redeploy the pods, I can see that nvtop shows that it still fits the memory, with my new config

[nvtop]

When I run pi on my laptop, I can test the new context size, which is about 4x the original context size. As you can see, the ctx size is now larger at the bottom right side of the screen (highlight), which makes the model much more useful.

[pi dev screenshot running a task]


6k context size is still relatiely small for coding tasks. The model needs to look at many files and outputs from the different commands. The context piles up very quickly. To make a coding agent useful you need a very large context size. As I try the model on more complex tasks, such a small MVP web application, it is capable of running the first couple of tasks succesfully, but it starts to run out of context size after the 3rd or 4th prompt. If I take a look at kubernetes, I can se ethe instances are rebooting mid sesnions, likely because they are running out of memory since the memory is already very tight from startup

[pods restart image]

## Toughts on the model

THe model applies what I tell it too literally. 
## Lessons learned from this project

Overall I was limited by my hardware. With my 6GB vRAM on my GPU card I'm not really able to deploy a useful LLM. When I first approached this project, I wanted to learn what it takes to deploy an open weights model via an API. What I found out is that this is the easiy part. Like with most systems in productions, the tricky part is to get right the node size, model size, and number of instances and autoscaling to be able to run a system smoothly and without issues for users when using these models. These can only be achieved by testing these models in production and having good monitoring of resource usage, sla (ie are there quehed responses) that give us enough insights to improve the deployments over time.

Even though I wasn't able to try the largest more capable model, I can arleayd see how capable open models are at being able to tackle many coding tasks if used well. They are not as close as the frontier models from OpenAI or Cladue, but that may not be required for many everyday tasks.



TODO 
- Using nvtop to check the best ctx_size. Ctx size is 