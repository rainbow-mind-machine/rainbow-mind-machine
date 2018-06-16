# rainbow-mind-machine

![tinysheep](img/sheep.jpg)

## All the shields

[![works on my machine](https://img.shields.io/badge/works-on_my_machine-blue.svg)](https://img.shields.io/badge/works-on_my_machine-blue.svg)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)

[![Website pages.charlesreid1.com](https://img.shields.io/website-up-down-green-red/https/pages.charlesreid1.com.svg)](https://pages.charlesreid1.com/rainbow-mind-machine)
[![PyPI version rainbowmindmachine](https://badge.fury.io/py/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)
[![PyPI license](https://img.shields.io/pypi/l/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)

[![gh issues](https://img.shields.io/github/issues/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/issues/)
[![gh issues-closed](https://img.shields.io/github/issues-closed/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/issues?q=is%3Aissue+is%3Aclosed)
[![gh pull-requests](https://img.shields.io/github/issues-pr/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)
[![gh pull-requests closed](https://img.shields.io/github/issues-pr-closed/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)

[![cthulhu](https://img.shields.io/badge/Ph'nglui%20mglw'nafh%20Cthulhu%20R'lyeh%20wgah'nagl%20fhtagn-m'latgh%20gnaiih%20Nyarlathotep%20geb%20Tsathoggua%20bug-blue.svg)](https://en.wikipedia.org/wiki/Cthulhu)

[![GitHub stars](https://img.shields.io/github/stars/rainbow-mind-machine/rainbow-mind-machine.svg?style=social&label=Star&maxAge=2592000)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/stargazers/)

## About

**rainbow mind machine** is an extensible framework for running Twitter bot flocks in Python.

rainbow mind machine helps with managing multiple twitter bots (bot flocks).
It uses a Keymaker object to do the one-time authentication step with Twitter,
and uses a Shepherd-Sheep model to run the flock.

rainbow mind machine is a **framework** because it provides components 
([Keymaker](keymaker.md), [Shepherd](shepherd.md), and [Sheep](sheep.md))
with specific roles and ways of interacting.

rainbow mind machine is **extensible** to keep bots from becoming boring. 
There are a limited number of components to extend (2), 
these two components have a simple and clear function call order,
and rainbow mind machine tries to use sensible defaults.

That means we start out with bots that "just work" 
and we can incrementally improve, extend, override,
or redefine behaviors to make them increasingly complex,
while still abstracting away messy details.

See the [Shepherd](shepherd.md) page or the [Social Sheep](social_sheep.md) 
page for examples.

## Useful links

You are here:

* [rainbow mind machine documentation on charlesreid1.com](https://pages.charlesreid1.com/rainbow-mind-machine)

Source code:

* [rainbow mind machine source code on git.charlesreid1.com](https://git.charlesreid1.com/bots/rainbow-mind-machine)

* [rainbow mind machine source code on github.com/rainbow-mind-machine/rainbow-mind-machine](https://github.com/rainbow-mind-machine/rainbow-mind-machine)

Packaged products:

* [rainbow mind machine package on pypi](https://pypi.org/project/rainbowmindmachine/) (`pip install rainbowmindmachine`)

* [rainbow mind machine on dockerhub](https://hub.docker.com/r/rainbowmindmachine/rainbowmindmachine/) (`docker pull rainbowmindmachine/rainbowmindmachine`)

Related projects:

* [rainbow mind machine organization on github](https://github.com/rainbow-mind-machine)

## Installing rainbow mind machine

See [installing](/installing.md) for installation instructions.

## Quick Start

See [quickstart](/quickstart.md) for a quick guide to 
getting a bot up and running, and a few bot flock examples.

## Docker

See [docker](/docker.md) for more information about
using rainbow mind machine in a docker container.

## Dev Workflow

See [dev-workflow](/dev-workflow.md) for info about the workflow for 
uploading changes to pypi and dockerhub.

## Get In Touch

Contact the author: `rainbowmindmachine@charlesreid1.com`

