# rainbow-mind-machine

**rainbow mind machine** is an extensible framework for running Twitter bot flocks in Python.

rainbow mind machine helps with managing multiple twitter bots (bot flocks).
It uses a Keymaker object to do the one-time authentication step with Twitter,
and uses a Shepherd-Sheep model to run the flock.

rainbow mind machine is a **framework** because it provides components 
(Keymaker, Shepherd, and Sheep) with specific roles and ways of interacting.

rainbow mind machine is **extensible** to keep bots from becoming boring. 
There are a limited number of components to extend (2), 
these two components have a simple and clear function call order,
and rainbow mind machine tries to use sensible defaults.

That means we start out with bots that "just work" 
and we can incrementally improve, extend, override,
or redefine behaviors to make them increasingly complex,
while still abstracting away messy details.

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

See [installing](/docs/installing.md) for installation instructions.

## Quick Start

See [quickstart](/docs/quickstart.md) for a quick guide to 
getting a bot up and running, and a few bot flock examples.

## Docker

See [docker](/docs/docker.md) for more information about
using rainbow mind machine in a docker container.

## Dev Workflow

See [dev-workflow.md](/docs/dev-workflow.md) for info about the workflow for 
uploading changes to pypi and dockerhub.

## Get In Touch

Contact the author: `rainbowmindmachine@charlesreid1.com`

