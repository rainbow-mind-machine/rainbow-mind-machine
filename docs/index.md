# rainbow-mind-machine

![tinysheep](sheep.jpg)

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

[rainbow mind machine documentation on charlesreid1.com](https://pages.charlesreid1.com/b-rainbow-mind-machine)

[rainbow mind machine on pypi](https://pypi.python.org/pypi/rainbowmindmachine/0.4)

[rainbow mind machine on dockerhub](https://hub.docker.com/r/rainbowmindmachine/rainbowmindmachine/)

[rainbow mind machine organization on github](https://github.com/rainbow-mind-machine)

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

