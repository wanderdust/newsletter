---
title: 'Using Neovim with tmux'
date: '2025-05-20T12:09:22+01:00'
draft: true 
summary: ''
tags: ['tmux', 'terminal', 'vim']
categories: []
cover:
  image: ''
  alt: ''
  caption: ''
images: []
---


I've been using NeoVim for the past few months. I've always been a VSCode user, but then someone in my team suggested that VSCode is shit compared to IntelliJ Idea Ultimate. I then started using IntelliJ for a month or two with the VIM extension. At one point, I was starting to learn IntelliJ shortcuts to try and use the mouse less and less, and then I realised that I'd rather use an open source tool like NeoVIM rather than learning a bunch of shortcuts from a vendor tool.

After these few months, I still feel like I'm using NeoVim at a very basic level. I don't particularly feel much faster than using IntelliJ or VScode, but it _feels_ better, which is why I keep coming back to it. 

I've currently got some basic setup: I use treesitter to get pretty looking text, telescope to navgate files, and [conform](https://github.com/stevearc/conform.nvim) for all my formatting needs. This is enough to get me by.

The thing that has been annoying me the most lately is the terminal workflow. For starters, the terminal does not save any history across sessions, which is incredibly annoying. I often find myself wanting to look for commands in my history using `ctlr-r`, and for some reason the terminal in NeoVim does not save these (I use the `:terminal` command to start terminals). I'm pretty sure there are many workarounds online, but I'm not the kind of person who cares much about tinkering with the config, I just want something easy out of the box.

The second thing that's been annoying me lately is navigating buffers (or tabs as I think of them). I'm pretty sure I'm missing something here, but I always end up circulating my buffers using the `tab` key, which can get pretty slow if you have many tabs open. In a lot of cases I just want a single tap to go to my terminal from wherever window I'm currtently at.

And finally, I find the the `ctrl \` command to detach from the current terminal so I can go to a separate buffer very awkward to use.

For these reasons, and because I'm too lazy to properly research how to _fix_ these things with my current setup, I have decided to learn tmux so that I can run neovim inside it which I believe will solve all those problems. It also feels like _tmux_ is a useful tool to know, so I'm going to invest in it.


(20 minutes later ...)

Okay, so I wrote the text above just before looking into tmux. Getting setup and running takes almost no time. In the first 20 minutes that I've spent installing it and seeing how it works I believe I already have a much nicer workflow.

Here is a quick guide on how to get setup

## Install

```brew install tmux```

## Creating panels
- Starting a tmux terminal: `tmux`
- Creating a vertical panel: `ctrl-b %` - that is, press `control` + `b`, relase and then press `%`
- Creating a horizontal panel: `ctrl-b "`
- Move to left/right/up/down panel: `ctrl-b arrow-key`
- Closing pane: `ctrl d` or type `exit`

## Creating Sessions
Sessions are like different desktops. For example you use one session to have your vim and another to have your terminal and lazygit.

- Create a new session: `ctrl-b c`
- Move to next/previous session: `ctrl-b n` and `ctrl-b p`
- Move to specific session: `ctrl-b <number>`


## Other
- Renaming a sessions: `ctrl-b ,`
- Current panel full size: `ctrl-b z`
- Detaching current session: `ctrl-b d`
- Attaching a session: `tmux ls` to list sessions and `tmux attach -t <number>`

## Resizing
Resizing windows can be accomplished by pressing `ctl-b ctrl-<arrow>`. That is, you press `ctrl` and `b` first, then you release and then you press `ctrl` and `<arrow>` to resize.

I should note that mac already uses the `ctrl-<arrow>` keybinding for something else, so you'll need to disable it in your keyboard shortcut settings for this to work.


## Creating a config
You can create a tmux config for customisation at `~/.tmux.conf`

## Conclusion
 [Use this setup for a few days and say]


---
Resources: https://hamvocke.com/blog/a-quick-and-easy-guide-to-tmux/

---
## My Newsletter

I send out an email every so often about cool stuff I'm building or working on.

{{< subscribe >}}
