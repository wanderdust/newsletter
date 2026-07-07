---
title: '049_how_i_became_a_web_developer'
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

The other day I went to my neighbors house to take my son to a playdate with his friend. My neighbor owns a physiotherapy business, and my wife had recently visited to see their accupunture specialist. I told him (in a nice way as possible) that I had a look at my wife's phone while she was browsing his website, and that I thought it looked a buggy and not as good as it could be, specially the mobile version. I'm not an expert web developer by any means, but even I know that these days you should design websites thinking about phone first, because that's what most people will use to book their appointments.

He then told me he was having issues with the web developer who built and maintains their website. He told me that he wanted to be given access to the website code, because he was thinking of potentially using another web developer who was more reliable or even migrating his website to a wordpress that he could easily manage. However, the web developer didn't want to give him access to the code artifacts, he was essentially holding it hostage so he could keep his monthly maintenace fee.

I told him that, although I'm not a professional web developer, I know my way around websites, and that I could take a look for him. With AI coding agents, it could not be too hard to clone the webisite so that he could own the code, and I could give it to him so he could do whatever he wanted afterwards.

The next day, I went and had a look at his site. It seemed like a simple static website, with a bunch of HTML pages and no complex logic anywhere beyond your typical hamburger menu in the navigation section. So I decided to give it a go.

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

The first thing I had to do was download the existing website locally for reference. I asked claude for help doing this, and it suggested this command.

```shell
  wget --mirror --convert-links --adjust-extension --page-requisites --no-parent https://example.com
```

I didn't want to get too involved in this, in case it became a rabbit hole, so I asked claude to do this for me. Within 10 minutes I had a local version of this website running on localhost that I could use as reference.

I had a look at the files, and it looked like bunch of html files, png, where each file contained its own css and javascript, meanining there was no re-usability at all. There were 37 h

```shell
home-physio.html
Homehero.jpeg
index.html
joint-mobilisation.html
lisa.html
locations.html
manipulation.html
manual-therapy.html
Marcus_Croy.jpeg
Marcus_Rae.jpeg
marcus-croy.html
marcus-rae.html
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
radial-shockwave-therapy.html
raes_anatomy_logo.png
rehabilitation-movement-coaching.html
robots.txt
services.html
serviceshero.jpg
sport-injury-rehab.html
sports-taping.html
strength-conditioning.html
vestibular-rehab.html
```
