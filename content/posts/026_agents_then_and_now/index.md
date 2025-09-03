---
title: 'From LLM to Agent'
date: '2025-09-02T09:55:49+01:00'
draft: true 
summary: ''
tags: []
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---

After having ignored the agent hype for quite a while, I was starting to get that inevitable feeling of being left out.

I recently came across [this blog post](https://ghuntley.com/agent/) which walks through the basic flow of an agent, and it inspired me to build my own.  

This post is walks through the steps to convert an LLM into an agent.

At the end I share an example of a Software Engineering Agent that uses the workflows described in this post.

## The LLM

Lets start with a simple LLM workflow. This will be our starting point.

![](./llm-loop-1.png)


The user writes a prompt, and the LLM returns a response.

We are already very familiar with this, we all use chatgpt everyday. Next.

## Accessing Tools

What makes an LLM tuly useful is when it can do things on its own.

It is very annoying having to copy the contents of a file, and ask ChatGPT to generate some tests for that file. Then we have to copy the code response, and manually create a file in our project.

It is much better if the LLM can do that directly for us. We can give the LLM access to tool for this.

![](./llm-loop-2.png)


The way it works is that you define a set of actions in your program that the LLM can execute. Lets say for example we are building a coding agent. We can create 2 actions to read and to write files.

Whe can have the LLM return a structured JSON output to make the response easier to process.

In the first example we ignore the answer and run the tools instead.
```json
{
  "answer": "I have provided a list of tools blah blah ...", # ignore "answer" here and only run tools
  "tools": [
    {
      "tool": "read_file",
      "args": {
        "path": "search.py"
      }
    },
    {
      "tool": "write_file",
      ...
   }
  ]
}
```
In this next example, the LLM does not want to use any tools. If no tool is suggested, we treat the text as the final answer.

```json
{
  "answer": "Here are the unit tests for search.py...",
  "tools": []
}
```


The agent loop will look like this.
```python
# Simple tools
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()

def write_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)

TOOLS = {"read_file": read_file, "write_file": write_file}

user_prompt = "Write unit tests for search.py"
instructions = f"""
You are a coding agent. Use these tools when needed: {list(TOOLS.keys())}.
Otherwise, reply in plain text. Task: {user_prompt}
"""

response = LLM.chat(instructions)

if response["tools"]:  # run suggested tools
    history = []
    for action in response["tools"]:
        result = TOOLS[action["tool"]](**action["args"])
        history.append({"action": action, "result": result})
    
    response = LLM.chat(f"Give a final answer for task {user_prompt} after having executed these actions {history}")
else:
    print("Final answer:", response["answer"])
```

And with this you already have a useful LLM that can independently choose any of the tools available to run all sorts of actions on its own. Goodbye copy/paste.

## Adding a Validation Loop

The thing is, that agents get it wrong all the time.

The best thing we can do is add a validation step before we send the final response to the user. We want to check if the LLM actually accomplished the goal set by the user propmt.

If we skip this step, it is very likely that the agent will do some of the work, and forget to do the rest, giving the user an incomplete response.

To do the validation, we take the final answer candidate, and make a new LLM call passing the original user prompt and all the tool observations (files read, files created etc.)

![](./llm-loop-3.png)

Now, before sending a final response to the user, we check if the task has been completed. If not, we start the process all over again.

With the new loop, we need to make sure we log and save all the outputs from every step into a history so that it can be used by the agent in future iterations.

We'd update our code to do a validation loop:


```python
# ... same as before

response = LLM.chat(instructions)
history = []

while True:
    if response["tools"]:
        for action in response["tools"]:
            result = TOOLS[action["tool"]](**action["args"])
            history.append({"action": action, "result": result})
        response = LLM.chat(f"Give a final answer for task {user_prompt} after having executed these actions {history}")

    # Validation step
    is_done = LLM.chat(
        f"Prompt: {user_prompt}\nHistory: {history}\nHas the task been completed? Reply True/False."
    )

    if is_done == "True":
        break  # exit loop when task resolved

print("Final answer:", response["answer"])
```



And with this we have a fully functional LLM agent that can independently do tasks for us. For a coding agent we may want to give access to more tools other than read and write, such as file search, listing directories, terminal command exectution, and even internet search so it can search documentation. The world is your oister.

## Final Tweaks

We can add a few tweaks here and there to make the agent even more robust.

For example we may decide to add an additional LLM call at the beggining to turn the user prompt into a detailed propmt with a step by step plan. This plan will make the validation process better for the model by not only giving the next LLM a clue of what tools to use and in what order (ie list files first, read file next, write after), but also by making the validation more robust. During validation we check the model actions against a detailed list of TODOs to see if the task was accomplished or not.

In our code we simply add this line after the user prompt

```python
plan = llm.chat(f"Break the task into steps: {user_prompt}")
```

Another nice tweak is to add an LLM call before the final response, when the answer has already been validated. This way the model can take a full view of the action history and summarise the outcome into a one nice final answer. If you don't this part, the agent may still have done the task, but you may get an ugly and unpolished final text answer.

![](./llm-loop-4.png)

Now we can see this in action. I have built a coding agent so I could understand this process better. I recommend you do the same!

![example swe agent](./swe_agent_demo.gif)

In this demo, the agent is asked to create unit tests for a specific file. It first uses the read tool to open `search.py`, then sends the contents for validation.

The first validation fails, so the process restarts with a new LLM call. With the contents of `search.py` now in context, the agent uses the write tool to generate the unit tests. The outputs are validated again; this time they pass, and the agent sends the final response to the user.

## Final Words

We have seen how to go from LLM to agent by adding a few simple steps.

It is quite simple to build your own agent, and you can use them for all sorts of things.

Keep in mind that I came up with this implementation from playing around with it, but there will definitely be more efficient loops out there. I'd recommend you build your own and you see what works and what does not work.

You don't have to build agents from scratch like we have done in this post. You can use libraries like [pydantic ai](https://martinfowler.com/articles/build-own-coding-agent.html) that abstract a lot of this logic, so you can mainly focus on the tooling part.

I hope you found this educational, and hopefully it has been an enjoyable read.

See you next time!
