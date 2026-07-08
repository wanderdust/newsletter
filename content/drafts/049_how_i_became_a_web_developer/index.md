---
title: 'How I overengineered a whole thing because of AI'
date: '2026-07-07T08:06:07+01:00'
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

This is the story of how I overengineered a whole website migration because I had access to AI coding tools. This was originally going to be a success story of how I managed to rescue my friend's webisite from his web developer who was keeping it hostage. I was going to write about how I used AI to rewrite a whole website in a day, despite me not being a web developer. But at the end, when I was ready to boast about what I great job I'd done, I realised I was a fool.

----
The story begins with me and my famili going to our neighbors house to take my son to a playdate with his friend. My neighbor owns a physiotherapy business, and my wife had recently visited to see their accupunture specialist. I told him (in a nice way as possible) that I had a look at my wife's phone while she was browsing his website, and that I thought it looked a buggy and not as good as it could be, specially the mobile version. I'm not an expert web developer by any means, but even I know that these days you should design websites thinking about phone first, because that's what most people will use to book their appointments.

He then told me he was having issues with the web developer who built and maintains their website. He told me that he wanted to be given access to the website code, because he was thinking of potentially using another web developer who was more reliable or even migrating his website to a wordpress that he could easily manage. However, the web developer didn't want to give him access to the code artifacts, he was essentially holding it hostage so he could keep his monthly maintenace fee.

I told him that, although I'm not a professional web developer, I know my way around websites, and that I could take a look for him. With AI coding agents, it could not be too hard to clone the webisite so that he could own the code, and I could give it to him so he could do whatever he wanted afterwards.


He also told me that the guy who had created his website had told him that he had his own "AI platform to build it". I didn't mention anything to him at the time, but it felt to me like this guy was trying to sell him some snake oil. In my head I thought he was probably just using claude to build websites and he was marketing it as something bigger than it really is.

The next day, I went and had a look at his site. It seemed like a simple static website, with a bunch of HTML pages and no complex logic anywhere beyond your typical hamburger menu in the navigation section. So I decided to give it a go. I could see from 100 miles away that the dev had indeed used AI to create the website. I could tell by the shape of the cards, emojis, font colors in titles etc. So I had already formed this idea in my head that the website was going to be a mess.

 Making these assumptions without proof was going to be one of my biggest downfalls, but I'll get to that later.

## The Requirements

The requirements for this project were simple

1. Create a clone of the website. The copy should look as similar to the original. If we were to swap them a returning customer should feel like they have landed on the same site.
2. Create a clean repo structure that can easily be picked up by any developer that has landed on it. I made the decision of not using any frameworks, because I wanted this to be able to run without requiring any library updates in a years time. Plain HTML, CSS and Javascript.
3. All the links, media and everything else should work as expected

## The Setup

Back in the day, this sort of cloning job would have been a lot of donkey work. It is essentially re-building the whole website from scratch using the existing website design as reference.

However, with AI it is a different story. I've been using AI driven development quite a bit over the last year, and with the right setup it can easily be done.

I decided to use claude combined with the [agent skills](https://github.com/addyosmani/agent-skills) framework. With this framework you can break large tasks such as this one into a set of requirements and a detail plan, that the agent can follow to complete the task.

## Getting started

The first thing I had to do was download the existing website locally for reference. I asked claude for help doing this, and it suggested this command. I had already formed a plan in my head, I would clone the website locally and use it for reference to build the clone. I would write it from scratch, because I had already formed the idea in my head that the downloaded files were not going to be re-usable at all.

The command that claude suggested was this. I asked it run it for me un run the thing in localhost.

```shell
  wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://example.com
```

Once it downloaded, I had a quick look at the files. To be honest, I spent less that 5 seconds looking at the list. I could see a bunch of HTML stuff and png files with random names, all flat in the directory. I had already decided that rebuilding the whole thing was the best way forward, and with AI it would not be too much upheaval.


```shell
home-physio.html
Homehero.jpeg
index.html
joint-mobilisation.html
lisa.html
locations.html
manipulation.html
manual-therapy.html
massage-therapy.html
MBM00268.jpeg
opc1.jpeg
opc2.jpeg
opc3.jpeg
Pic_placeholder.png
post-op-rehab.html
pricing.html
privacy-policy.html
psychologist-writing-his-notebook copy.jpg
psychology-reviews.html
psychology.html
...
```

I checked my local server, and I could see that the website was running locally, and it looked exactly like the original, so I was ready to migrate.

## Building the Webiste

I got started. I opened claude code in the terminal and fired up the agent skills framework.

![claude code](./claude_code.png)

I started using the `/interview-me` skill to set the original requirements. I have to say, whoever came up with this idea is a genious. This skill will ask you questions about what you want to build until it has enough confidence that it's got enough detail of all the specs. If you combine this skill with your microphone to narrate your answers, it makes for a pretty sweet workflow.

Within 5 minutes I had all of the requirements defined. So I moved on to generate the spec file with the `/spec` skill. This file gathered all of the HTML files that we needed to create, 32 in total, one for each page in the website, and all the external links that needed to be preserved.
