# rainbow-mind-machine

An extendable framework for running Twitter bot flocks in Python.

Quick start:
* Install the program
* Decide what kind of items you want to use to itemize the bots:
    * Option 1: create one bot per item in a list (e.g., list of strings in Python)
    * Option 2: create one bot per file in a folder (e.g., text files containing poems)
* Define a tweet action for a given bot, optionally using its corresponding item
* (Once per account) Run the KeyMaker to create keys and authenticate your bot with a Twitter account
* Run the bot Shepherd to herd the bot Sheep and perform group actions

See the `examples/` directory for some example flocks.

## Install

```
git clone https://github.com/charlesreid1/rainbow-mind-machine.git
cd rainbow-mind-machine
python setup.py build 
python setup.py install
```

## Credentials

Start by creating a Twitter application. 

This will register your rainbow mind machine bot flock application
with Twitter, and give you credentials to connect to Twitter's API.

One Twitter application can tweet on behalf of an arbitrary number of accounts,
so you only need one Twitter application per bot flock (or, really,
one per "bot maker").

When you register your application Twitter will give you a consumer key 
and a consumer secret. Assign these values to the variables `consumer_key`
and `consumer_secret` in the file `apikeys.py`.

```
consumer_key    = '123456'
consumer_secret = '123456'
```

See the `apikeys.example.py` file.

## Quick Start 

Let's walk through a quick example to illustrate
how this works.

### Creating and Authenticating Bot Accounts

The first step we take is to run the Keymaker.

The Keymaker takes a set of items, and creates
one key for each item.

The keys are what allow our application to tweet 
using a bot account. 

The items are arbitrary - they may be a list of 
strings or Python objects, or they might be a 
directory of text files or json files.

We call `make_key` on each item to create each key.

The keymaker _requires_ that we specify
a `name` parameter to name the bot and a `json` parameter
to specify the location of the key.

Also note, this requires that your Twitter app's 
consumer secret and consumer token be set 
in `apikeys.py`.

In the example below, the "items" are strings containing the bot name.
This uses credentials in `apikeys.py` and outputs key files
at `keys/key1.json` and `keys/key2.json`.

```python
import rainbowmindmachine as rmm
import subprocess

subprocess.call(['mkdir','-p','keys/'])

k = rmm.Keymaker()

# Create some keys
k.make_key({
    'name':'Twitter Bot 1',     # This is the bot label
    'json':'keys/key1.json'     # This is the key file
})
k.make_key({
    'name':'Twitter Bot 2',
    'json':'keys/key2.json'
})
```

When this script is run, the Keymaker will 
go through a series of interactive steps 
to create keys from each item.

### Running the Bot Flock

Once that is done, make a Shepherd for the bot flock,
and point it to the keys the Keymaker created 
in the `keys/` directory:

```python
import rainbowmindmachine as rmm

# make the Shepherd
sh = rmm.Shepherd("keys/")

# Change everybody's Twitter page color
sh.perform_action('change color','#CFC')

# Everybody tweet in parallel
sh.perform_pool_action('tweet')
```

## Using Rainbow Mind Machine with Docker Compose

For an example bot using rainbow mind machine in a docker container, see:

* [b-apollo](https://git.charlesreid1.com/bots/b-apollo)
* [b-ginsberg](https://git.charlesreid1.com/bots/b-ginsberg)
* [b-milton](https://git.charlesreid1.com/bots/b-milton)

The basic steps are as follows:

* Create a Twitter application
* Create a rainbow mind machine bot application
* Run the container pod interactively once with `docker-compose run <name-of-service>`
* Run the container pod in detached mode with `docker-compose up -d`

### Keeping Image Small

The official Python Docker images are huge: 
the absolute smallest image is 200 MB, and 
a full python 3 container using debian takes
nearly 1 GB. 

To reduce the size of these images, you can use 
a couple of strategies.

* Use alpine for the "real deal" - it is designed to be minimal 
    but requires bundling any "extras" into the container

* Use an image designed to be small
    * [jfloff/alpine-python](https://github.com/jfloff/alpine-python)

* Maintain logical separation 
    * one container per flock
    * one pod per server

