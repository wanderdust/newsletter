---
title: '037_setting_up_a_homelab'
date: '2025-11-26T19:48:55Z'
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

1) The hardware
- Compute nodes (thinkpads)
- NAS (Optional)

2) Setting up the nodes

2.1) Installing Ubuntu Server
2.2) Setting up a static IP on the nodes
- See which is your ethernet name by looking at ip addr. It is the one that starts with enp0...
- Use that as the ethernet name in the netplan/50-cloud init file. Use neplan apply https://linuxconfig.org/setting-a-static-ip-address-in-ubuntu-24-04-via-the-command-line
- Ah! But I'm using wifi. So I need to do it in the wifi part instead
- Find out your ip addr range via your Router (192.168 etc). Use ping command to verify your route (access to internet), this is your router ip where you see the UI. Use netplan apply to validate. Always make sure you backup the config before you start in case you fuck it up
(paste my config here)

2.3) Testing connectivity between nodes
-

3) Installing K3s
