# rainbow-mind-machine

## All the shields

![latest prime number version](https://img.shields.io/badge/latest--prime--number--version-5-blue.svg)

![tests-passing](https://img.shields.io/badge/tests-passing-green.svg)
[![works on my machine](https://img.shields.io/badge/works-on_my_machine-blue.svg)](https://img.shields.io/badge/works-on_my_machine-blue.svg)

[![pypi versions](https://img.shields.io/pypi/pyversions/boringmindmachine.svg)](https://pypi.python.org/pypi/boringmindmachine/) 
[![PyPI version rainbowmindmachine](https://badge.fury.io/py/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)
[![PyPI license](https://img.shields.io/pypi/l/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)
[![PyPI implementation](https://img.shields.io/pypi/implementation/rainbowmindmachine.svg)](https://pypi.python.org/pypi/rainbowmindmachine/)

[![gh pull requests](https://img.shields.io/github/issues-pr/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)
[![gh pull requests closed](https://img.shields.io/github/issues-pr-closed/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)
[![GitHub issues](https://img.shields.io/github/issues/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/issues/)
[![GitHub issues-closed](https://img.shields.io/github/issues-closed/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/issues?q=is%3Aissue+is%3Aclosed)
[![GitHub pull-requests](https://img.shields.io/github/issues-pr/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)
[![GitHub pull-requests closed](https://img.shields.io/github/issues-pr-closed/rainbow-mind-machine/rainbow-mind-machine.svg)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/pull/)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-Markdown](https://img.shields.io/badge/Made%20with-Markdown-1f425f.svg)](http://commonmark.org)
[![Website pages.charlesreid1.com](https://img.shields.io/website-up-down-green-red/https/pages.charlesreid1.com.svg)](https://pages.charlesreid1.com/rainbow-mind-machine)

[![cthulhu](https://img.shields.io/badge/Ph'nglui%20mglw'nafh%20Cthulhu%20R'lyeh%20wgah'nagl%20fhtagn-m'latgh%20gnaiih%20Nyarlathotep%20geb%20Tsathoggua%20bug-blue.svg)](https://en.wikipedia.org/wiki/Cthulhu)

[![GitHub stars](https://img.shields.io/github/stars/rainbow-mind-machine/rainbow-mind-machine.svg?style=social&label=Star&maxAge=2592000)](https://github.com/rainbow-mind-machine/rainbow-mind-machine/stargazers/)


## About 

![tinysheep](img/sheep.jpg)

**rainbow mind machine** is an extensible framework for running Twitter bot flocks in Python.

**rainbow mind machine** helps with managing multiple twitter bots (bot flocks).
It uses a Keymaker object to do the one-time authentication step with Twitter,
and uses a Shepherd-Sheep model to run the flock.

**rainbow mind machine** is a **framework** because it provides components
(Keymaker, Shepherd, and Sheep) with specific roles and ways of interacting.

**rainbow mind machine** is **extensible** to keep bots from becoming boring.
There are a limited number of components to extend (2),
these two components have a simple and clear function call order,
and rainbow mind machine tries to use sensible defaults.

The philosophy is to help users get started quickly,
and build on simple behaviors to create complex, rich
bot behaviors.


## Links

rainbow mind machine (rmm) links:

* rmm source code on Github: <https://github.com/rainbow-mind-machine/rainbow-mind-machine>
* rmm documentation: <https://pages.charlesreid1.com/rainbow-mind-machine/>
* rainbow mind machine organization on Github: <https://github.com/rainbow-mind-machine>

releases:

* rmm releases on Github: <https://github.com/rainbow-mind-machine/rainbow-mind-machine/releases>
* rmm on pypi: <https://pypi.org/project/rainbowmindmachine/>
* rmm on dockerhub: <https://hub.docker.com/r/rainbowmindmachine/rainbowmindmachine/>


## Pages

[About the Mind Machine Framework](mind-machine-docs/about.md) - general
information about the mind machine framework (how does it work? what does it
look like?)

[About Rainbow Mind Machine](about.md) - about the rainbow mind machine library
(what is it? what does it do?)

[Installing](installing.md) - installation instructions (how do I install bmm?)

[Quick Start](quickstart.md) - quick start instructions for getting started
with rainbow mind machine - run your first Twitter bot!

Documentation for components implemented in rainbow mind machine:

* Keymakers:
    * [TwitterKeymaker @ boring mind machine documentation](https://pages.charlesreid1.com/boring-mind-machine/bmm_keymaker_twitter/)
* [rmm.Shepherd](rmm_shepherd.md)
* [rmm.Sheep](rmm_sheep.md)
* [rmm.PoemSheep](rmm_poem_sheep.md)
* [rmm.QueneauSheep](rmm_queneau_sheep.md)
* [rmm.SocialSheep](rmm_social_sheep.md)



## Links

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

See [installing](installing.md) for installation instructions.

## Quick Start

See [quickstart](quickstart.md) for a quick guide to 
getting a bot up and running, and a few bot flock examples.

## Developer Notes

See [Developer Notes](mind-machine-docs/dev.md) for info about the 
workflow for uploading changes to pypi and dockerhub.

## Get In Touch

Contact the author: `rainbowmindmachine@charlesreid1.com`

