---
title: 'Deploying an Open Weights LLM as an API on a 6 GB GPU'
date: '2026-11-09T08:56:30Z'
draft: false
description: "What it takes to serve an open weights coding model over an API with Kubernetes, and use it as a coding agent from my laptop, on a home-lab RTX 2060."
summary: "What it takes to serve an open weights coding model over an API with Kubernetes, and use it as a coding agent from my laptop, on a home-lab RTX 2060."
# Valid tags: ai, aws, career, certifications, data-engineering, kubernetes, postgres, reflections, security, serverless, testing, tooling
tags: ['ai', 'kubernetes']
categories: []
ShowToc: true
TocOpen: false
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

<!-- TODO: cover image (maybe nvtop_ctx_81920.png or a photo of the box). The title is a suggestion. -->

Open weights models are becoming more and more capable, and many organisations are wondering whether they should deploy and manage their own. Earlier this year the [CEO of IBM](https://www.theregister.com/systems/2026/10/22/ibm-ceo-says-open-weight-models-are-now-irresistibly-good-and-cheap-on-prem/5304640) said that open weights models are getting good enough to use them instead of the closed ones. Running your own model also makes sense if you want your data to stay within your company and not go to third parties.

The purpose of this article is to find out what it takes to deploy an open weights model behind an API. I'll be using Kubernetes to manage the deployment and scaling. Once the model is deployed, I'll use the [Pi](https://pi.dev) coding agent to test the model's coding capabilities and speed.

## The hardware

This project runs on my own GPU home lab running Ubuntu Server. The machine has an RTX 2060 with 6 GB of VRAM, which is a fairly old card by today's standards, but good enough to run some of the smaller models. The rest of the box is a Ryzen 5 3600 (12 threads) and 15 GB of RAM.

For reference, the RTX 2060 is the same generation as the T4 in AWS's g4dn.xlarge, which costs about $0.53/hour on-demand, or roughly $380/month if left running. The T4 has 16 GB of VRAM though, so it can fit a bigger model than my card. <!-- TODO: double-check the current g4dn.xlarge price. -->

The VRAM on my graphics card is what limits the model size. I also only have one GPU, which means I can't scale to more than one instance. In a production environment you'd have several nodes available when you need to scale.

{{< figure src="TODO_homelab_box.jpg" alt="TODO" caption="TODO" align=center >}}
<!-- TODO: optional photo of the home-lab box (same machine as the Space Invaders post, could link to it here). -->

## The model

For the model I'll use [Qwen3.5 with 4 billion parameters](https://huggingface.co/unsloth/Qwen3.5-4B-GGUF), quantised to 4 bits (Q4_K_M). It's a small model that can write code and use tools, which is the kind of model you'd deploy internally for software engineers to use with a coding agent like Pi.

The reason for picking this model is that it's as much as I can fit in my card's VRAM. The model file is about 2.7 GB, which gets loaded into the 6 GB of memory. The rest of the VRAM is needed for the KV cache, which holds the context and is what makes responses fast. (I wrote about [how KV caching works]({{< relref "/posts/054_k_v_caching" >}}) in a previous post.)

The next size up is the 9 billion parameter model, which sits at about 5.7 GB before accounting for any memory for the KV cache. That would leave no room for context, making it useless on my card.

## The deployment

The model is deployed as a centralised API service in Kubernetes. Users (me) call it with a URL and an API key to use the model for coding tasks.

{{< figure src="TODO_architecture_diagram.png" alt="TODO" caption="TODO" align=center >}}
<!-- TODO: diagram 1, the big picture: laptop (Pi) -> home network -> k3s Service (LoadBalancer, 192.168.1.149:8080) -> llama-server pod -> RTX 2060. -->

I use [K3s](https://k3s.io), a lightweight version of Kubernetes, in my home lab. The deployment consists of a Deployment, a ConfigMap, a Secret, a Service and an HPA (Horizontal Pod Autoscaler), plus a PersistentVolumeClaim to keep the model files between restarts.

{{< figure src="TODO_k8s_resources_diagram.png" alt="TODO" caption="TODO" align=center >}}
<!-- TODO: diagram 2, the k8s resources: Deployment (with ConfigMap + Secret as env, PVC at /models), Service in front, HPA pointing at the Deployment. -->

The Deployment defines the image, storage and configuration used by the pods. At the container level you define which image the pods run, and which environment variables and config to load. For the image I'm using [llama.cpp](https://github.com/ggml-org/llama.cpp)'s `llama-server` (`ghcr.io/ggml-org/llama.cpp:server-cuda`), a ready-to-use HTTP server for open weights models. Each pod requests one GPU (`nvidia.com/gpu: 1`), and the model is downloaded on startup into a volume mounted at `/models`.

```yaml
# TODO: paste apps/llm/k8s/deployment.yaml
```
<!-- TODO: deployment config. Bits worth keeping visible: runtimeClassName nvidia, requests cpu 1 / memory 2Gi / nvidia.com/gpu 1, limits memory 4Gi / gpu 1, envFrom llm-config + llm-secrets, LLAMA_CACHE=/models, startup probe on /health (period 10s, failureThreshold 90), strategy Recreate. -->

During the first deploy the model needs to download the image and the model. The image, of 2.6 GB took about 10 minutes to dowload. Then, once the container starts, llama-server downloads the model, which took almost another 13 minutes. This is why the startup probe needs a generous budget.

The Deployment is coupled with a Service, which is the interface we use to talk to the pods. The Service gives us a single IP and port, and does basic load balancing across the pods running the LLM. In K3s, a Service of type `LoadBalancer` is exposed on the node's IP, so the API is available on my home network at `192.168.1.149:8080`.

```yaml
# TODO: paste apps/llm/k8s/service.yaml
```

The environment variables are loaded from a ConfigMap. This is where the model parameters live: which model to use, the context size, how many GPU layers to offload and so on. llama-server reads any `LLAMA_ARG_*` environment variable as a command line argument, so the whole model configuration lives in one file. This is the initial setup, using the Qwen3.5 4B model with a context size of 32,768 tokens:

```bash
# apps/llm/config/model.env
LLAMA_ARG_HF_REPO=unsloth/Qwen3.5-4B-GGUF:Q4_K_M
# The model "id" clients (Pi) ask for
LLAMA_ARG_ALIAS=qwen3.5-4b
# Total context, split across slots (32768 / 2 = 16384 per request)
LLAMA_ARG_CTX_SIZE=32768
# Concurrent request slots
LLAMA_ARG_N_PARALLEL=2
# Offload all layers to the GPU
LLAMA_ARG_N_GPU_LAYERS=99
# Use the model's chat template (needed for tool calls)
LLAMA_ARG_JINJA=true
# Expose Prometheus metrics at /metrics
LLAMA_ARG_ENDPOINT_METRICS=true
```

Another interesting setting is `LLAMA_ARG_N_PARALLEL`, which defines how many requests the model can handle in parallel. Any concurrent requests on top of that wait until earlier ones are finished. The context is also divided between the slots, so each one gets a slice of the total context size: with 2 slots, each request gets 16,384 tokens. Depending on your specs, you can tweak this to fit your needs. Since this is also what sets the number of concurrent users per pod, you'd tune it with stress tests to find the sweet spot of max concurrency an instance can hold, and set up autoscaling based on that.

The next part is the horizontal autoscaling. I've set it up to scale up to 2 instances if CPU usage goes over 70% (of the 1 CPU the pod requests). But this is pointless for two reasons.

First, CPU usage is not the right metric to track. A better metric would be GPU memory usage or the number of queued requests. However, out of the box, the HPA only scales on CPU and memory (RAM, not GPU memory). To track these more useful metrics we could use [KEDA](https://keda.sh) instead, but this is out of scope for this project because of the next reason.

Second, I only have one GPU. Even when autoscaling triggers (which it does), the new pod can't start because there are no more GPUs available, so it stays in `Pending`. On the first deploy, the CPU spike from loading the model was enough to trigger it: the HPA scaled to 2 replicas, and scaled back down to 1 six minutes later. I set up the HPA for illustrative purposes, and to check that it does work with these settings.

```yaml
# TODO: paste apps/llm/k8s/hpa.yaml
```

{{< figure src="k9s_pod_restarts_and_pending_replica.png" alt="k9s showing two llm pods: one running at 100% of its CPU request, and a second replica stuck in Pending" caption="The HPA in action: the running pod is at 100% of its 1 CPU request, so a second replica is created. With no second GPU, it stays in `Pending`." align=center >}}

Finally, there's the Secret, which holds the API key needed to call the API. I generate it from a gitignored `.env` file so the key never ends up in git. As everyone using Kubernetes knows, secrets are not really secret: the values are only base64 encoded. In a production environment it's better to load your secrets from a secrets vault instead.

```bash
# TODO: paste the kubectl create secret command from apps/llm/deploy.sh (with the key redacted)
```

Once the model is deployed, we can call the API using the home lab's IP and port:

```bash
export LLM=http://192.168.1.149:8080
curl $LLM/health
# {"status":"ok"}
```

## Testing the API

Before setting up the coding agent, we can test the model by calling the API directly:

```bash
curl -s $LLM/v1/chat/completions \
  -H "Authorization: Bearer $LLM_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5-4b","messages":[{"role":"user","content":"Write a Python function that reverses a string."}]}' \
  | python3 -m json.tool
```

{{< figure src="curl_first_chat_response.png" alt="The JSON response from the first chat completion request, with the model's answer, its reasoning, token usage and timings" caption="The first request to the model. It took 1 min 10 s, and 61 of those seconds were spent processing a 20 token prompt." align=center >}}

The API returns a JSON object that follows the OpenAI API standard. Apart from the answer in `message.content`, it returns:

- `reasoning_content`: Qwen3.5 is a thinking model, and this is its reasoning before answering.
- `usage`: the prompt and completion tokens. Here 20 tokens in and 708 tokens out.
- `timings`: a llama.cpp extra with the speed of each step. The model generates at about 80 tokens/second, which it does consistently on every request.

The very first request was slow: a whole minute just to process the prompt. Every request after that processed its prompt in well under a second, so this is a one-off cost after the model loads.

We can also call the API with streaming, by adding `"stream": true`. This is a much more useful approach, since we don't have to wait for the full answer to be ready. We can read it as it gets generated, as we're already used to from every LLM app out there.

```bash
curl -N $LLM/v1/chat/completions \
  -H "Authorization: Bearer $LLM_KEY" -H "Content-Type: application/json" \
  -d '{"model":"qwen3.5-4b","stream":true,"messages":[{"role":"user","content":"Count to 10"}]}'
```

{{< video src="streaming_response.mp4" poster="streaming_response_poster.jpg" alt="A streamed response from the API: one server-sent event per token, ending with a final chunk that holds the timings and a DONE message" caption="Streaming: the response arrives as server-sent events, one chunk per token. The last chunk carries the timings, followed by `data: [DONE]`." controls="true" >}}

As we can see, the response is split into many small chunks, one per token: `"6"`, `","`, `" "`, `"7"`. The final chunk has `finish_reason: "stop"` and the timings, and the stream ends with `data: [DONE]`.

One thing worth knowing is that the API is stateless. Calling it again won't remember the previous conversation unless we send it again in the next call. This is why context grows so large as conversations get longer and longer: every request carries the whole history.

```json
// TODO: replace with a real second call that includes the history, e.g.
{"model": "qwen3.5-4b", "messages": [
  {"role": "user", "content": "Count to 10"},
  {"role": "assistant", "content": "1, 2, 3, 4, 5, 6, 7, 8, 9, 10"},
  {"role": "user", "content": "Now count backwards"}
]}
```

Resending the whole history every time sounds expensive, but the server keeps a prompt cache. If the start of the prompt matches what it has already processed, it only processes the new tokens.

In our case we don't need to worry about managing the history, because the coding agent handles it for us.

The last piece of the API a coding agent relies on is tool calling. The model never runs anything itself. The agent sends a list of tools it can use (a name, a description and a JSON schema for the arguments) with every request, and the model replies with a structured request to call one of them:

```json
"finish_reason": "tool_calls",
"message": {
    "content": "",
    "tool_calls": [{
        "type": "function",
        "function": {"name": "read_file", "arguments": "{\"path\":\"main.py\"}"}
    }]
}
```

The agent runs the tool, sends the result back in the next request, and the loop continues until the model answers in plain text. Note that the tool definitions count towards the prompt: asking "What is in the file main.py?" with a single tool attached was already 273 prompt tokens.

## Using the model in a coding agent

To make the model useful, I'll use the [Pi](https://pi.dev) coding agent. Pi is an open source coding agent in the same vein as Codex or Claude Code, and because our API follows the OpenAI standard, it can connect to it to handle our coding tasks.

To make this similar to a real production setup, I install Pi on my laptop rather than on the machine running the model. This is the same as if you deployed the model on EC2 and ran the agent from your local machine.

{{< figure src="TODO_pi_diagram.png" alt="TODO" caption="TODO" align=center >}}
<!-- TODO: diagram 3, or reuse diagram 1: laptop running Pi -> HTTP + API key -> 192.168.1.149:8080 -> llama-server. Shows that the agent and its tools run on the laptop, only the model runs on the server. -->

Once Pi is installed, add the model to `~/.pi/agent/models.json`:

```json
// TODO: replace with your real ~/.pi/agent/models.json
{
  "providers": {
    "homelab": {
      "baseUrl": "http://192.168.1.149:8080/v1",
      "api": "openai-completions",
      "apiKey": "LLM_KEY",
      "models": [
        { "id": "qwen3.5-4b", "contextWindow": 32768, "maxTokens": 8192 }
      ]
    }
  }
}
```

And don't forget to add the API key to your environment. The `contextWindow` is used for pi to know when to compact the conversation. I set it to the same as the server.

Pi hides providers it can't authenticate with, so if the variable isn't set the model won't show up at all. To make sure it loads automatically, add it to your `~/.bashrc` or `~/.zshrc`:

```bash
export LLM_KEY=...
```

Then we can run Pi, and if everything went well, we'll see our model loaded. We can start using it for coding tasks. In this example I ask it to write some tests for my project.

{{< video src="TODO_pi_working.mp4" poster="TODO_pi_working_poster.jpg" alt="TODO" caption="TODO" controls="true" >}}
<!-- TODO: video of Pi working on a task. -->

When Pi is working, the GPU runs flat out. Each agent turn kept it at 97% utilisation and 158 of its 160 W for around 45 seconds.

{{< figure src="nvtop_pi_request_full_power.png" alt="nvtop while Pi is working: the RTX 2060 at 97% utilisation, drawing 158 of 160 W" caption="One Pi request in `nvtop`: 97% GPU utilisation and 158 W, the card's power limit." align=center >}}

## Testing the performance

When I first started using the model, I ran out of context after a few prompts. Coding agents need a generous context size, and a model isn't very useful if it only allows a handful of prompts before it errors out.

{{< figure src="pi_truncated_at_16k.png" alt="A Pi session where the model fixes a bug, then fails with a connection error and repeated 'Response was truncated before completion' messages, with the status bar at 72.2% of 16k" caption="Pi after a few prompts: a connection error, then every response is truncated. The status bar in the bottom left shows 72.2% of the 16k context used." align=center >}}

The cause was that the context size was being depleted very quickly, which meant the response could not be fully generated.

The underlying problem was context. When I checked my settings, I found two issues. First, the context size was initially set to 32,768 tokens. The bigger issue was that `LLAMA_ARG_N_PARALLEL` was set to 2, which means the context gets split in half between the two slots. So all I was getting was 16,384 tokens per request.

16k tokens sounds like a lot: it's around 12,000 words. But a coding agent burns through it fast. The system prompt and tool definitions go in every request, and so does every file the model reads and every command output. In one session the context doubled from about 6,000 to 12,000 tokens in a few minutes, and the server logs showed all the requests going to slot 0. Slot 1 was never used.

Qwen3.5 supports up to 262K tokens of context, but because the context is held in memory as the KV cache, I'm limited by the amount of VRAM I have. llama.cpp reserves all the memory it needs when the instance starts, so I can use [nvtop](https://github.com/Syllo/nvtop) to check how much memory the model needs. The memory used is the model size + the KV cache for the full context + some compute buffers. Once it's loaded, it doesn't grow: a longer conversation gets slower, not bigger.

This is nvtop with my initial setup (2 slots, 32,768 tokens of context):

{{< figure src="nvtop_idle_initial_config.png" alt="nvtop with the model loaded and idle: 0% GPU utilisation, 10 W, and llama-server holding 4800 MiB of GPU memory" caption="The initial setup, idle: llama-server holds 4.8 GB of the 6 GB even when nobody is using it, while drawing only 10 W." align=center >}}

Since I'm the only user, I set `LLAMA_ARG_N_PARALLEL` to 1, which gives one slot with the full context size, and matched Pi's context window to it. Pi went from 16k to 33k of context, and the session recovered.

{{< figure src="pi_after_parallel_1_33k.png" alt="The same Pi session after the change, with the status bar at 36.1% of 33k and the model rewriting the file" caption="The same session after setting `LLAMA_ARG_N_PARALLEL=1`: the context goes from 16k to 33k, and the model gets back to work." align=center >}}
<!-- TODO: verify. The 33k is Pi's own contextWindow setting. The 10 Nov ConfigMap screenshot shows the cluster still on 2 slots of 16k the next morning, so the recovery may have come from the maxTokens change rather than N_PARALLEL. Adjust the paragraph above if so. -->

However, 32k of context is still small for a coding agent, and my memory usage was already pretty close to the limit. What I did next was store the KV cache in 8 bits (`q8_0`) instead of the default 16 bits (`f16`), and turn on flash attention. This roughly halves the memory per token of context, so I could double the context size to 65,536, and then push it further to 81,920.

```bash
## Optimising context
LLAMA_ARG_CTX_SIZE=81920
LLAMA_ARG_N_PARALLEL=1
LLAMA_ARG_FLASH_ATTN=on
LLAMA_ARG_CACHE_TYPE_K=q8_0
LLAMA_ARG_CACHE_TYPE_V=q8_0
```

When I redeployed the pods, my changes didn't show up. I made the rookie mistake of restarting the pods without ensuring the new configmap was updated. It turned out the ConfigMap in the cluster still had the old settings, and the server logs still showed 2 slots of 16k each. I can't count the number of times this same issue has happened to me before.

{{< figure src="configmap_vs_model_env.png" alt="Terminal showing the ConfigMap in the cluster with CTX_SIZE 32768 and N_PARALLEL 2, the model.env file with CTX_SIZE 81920 and N_PARALLEL 1, and the server log showing n_slots = 2 and n_ctx_slot = 16384" caption="The ConfigMap in the cluster (top) doesn't match `model.env` in the repo (middle), and the server log (bottom) confirms the pod is still running 2 slots of 16,384 tokens." align=center >}}
<!-- TODO: add one sentence on what caused the stale ConfigMap and how you fixed it. -->

Once the new config was actually applied, nvtop showed it still fits in memory, with about 280 MB to spare:

{{< figure src="nvtop_ctx_81920.png" alt="nvtop with the context size at 81,920 tokens: llama-server holds 5454 MiB and the card is at 5.726 of 6 GB" caption="81,920 tokens of context with an 8-bit KV cache: 5.7 GB of the 6 GB used." align=center >}}

| Setup | Context per request | GPU memory |
|---|---|---|
| 32,768 total, 2 slots, 16-bit KV cache | 16,384 | 5.1 GB |
| 81,920 total, 1 slot, 8-bit KV cache | 81,920 | 5.7 GB |

For an extra 0.6 GB of memory, each request gets 5x the context.

When I run Pi on my laptop with the new config, you can see the larger context size in the bottom left of the screen, which makes the model much more useful.

{{< figure src="TODO_pi_80k_context.png" alt="TODO" caption="TODO" align=center >}}
<!-- TODO: Pi screenshot running a task with the 80k context visible in the status bar (highlight it). -->

80k of context is still relatively small for coding tasks. The model needs to look at many files and outputs from different commands, and the context piles up very quickly. As I try the model on more complex tasks, such as a small MVP web application, it manages the first couple of tasks successfully, but starts to run out of context after the 5th or 6th prompt.
<!-- TODO: re-run the MVP web app test on the 80k config and check this still holds. -->

If I take a look at Kubernetes, I can also see the pods restarting mid-session.
<!-- TODO: add the restart reason (kubectl describe pod -> Last State, or kubectl logs --previous) and a screenshot. It isn't RAM: the k9s screenshot shows the pod at 19% of its memory limit. -->

## Thoughts on the model

The model applies what I tell it too literally.

<!-- TODO: add elaborate. -->

## Scaling this for production

With one GPU I couldn't really scale anything, but the setup makes it clear what you'd need to think about for a real deployment.

**Concurrency is slots × replicas.** Each pod can serve `N_PARALLEL` requests at once, and anything above that queues. But the context is split between slots, so more users per pod means less context for each of them on the same GPU. For coding agents, which need a lot of context, that pushes you towards fewer slots per GPU and more GPUs.

**Scale on queued requests, not CPU.** llama-server already exposes Prometheus metrics at `/metrics`, including how many requests are processing and how many are waiting. That's the signal to autoscale on, with something like KEDA. CPU tells you almost nothing: the only time it spiked on my setup was while loading the model.

**Scaling up is slow.** A new pod on a fresh node needs to pull a 2.6 GB image and download the model before it can serve a single request. On my first deploy that took over 20 minutes. In production you'd want images pre-pulled and models on shared storage, so a new replica only has to load the model into memory.

**Idle replicas still cost a whole GPU.** The memory is reserved at startup, so an idle replica holds its GPU whether anyone is using it or not. On AWS, every replica running 24/7 on a g4dn.xlarge is roughly $380/month. Check usage metrics based on the actual usage (requests per second, concurrent users) not just based on memory allocation.

**Monitoring and access.** You'd want to track queued requests, time to first token, tokens per second and GPU memory, and put a gateway in front of the API for per-user keys and rate limits.

## Lessons learned from this project

Overall, I was limited by my hardware. With 6 GB of VRAM I'm not really able to deploy a very useful LLM for coding. When I started this project, I wanted to learn what it takes to deploy an open weights model behind an API. What I found out is that this is the easy part.

Like with most systems in production, the tricky part is getting the node size, model size, context size, number of instances and autoscaling right, so the system runs smoothly and efficiently for its users. That can only be achieved by testing these models with real usage and having good monitoring of resource usage and SLAs (e.g. are there queued requests?), which give us enough insight to improve the deployment over time.

Even though I wasn't able to try the larger, more capable models, I can already see how capable open models are at tackling many coding tasks if used well. They are not as good as the frontier models from OpenAI or Anthropic, but that may not be needed for many everyday tasks.

{{< outro >}}
