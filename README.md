# rainbow-mind-machine

An extendable framework for running Twitter bot flocks in Python.

rainbow mind machine helps with managing multiple twitter bots (bot flocks).
It uses a Keymaker object to do the one-time authentication step with Twitter,
and uses a Shepherd-Sheep model to run the flock.

rainbow mind machine is a **framework** because it provides components (Keymaker, Shepherd, and Sheep)
with specific roles and ways of interactig.

rainbow mind machine is **extendable** to keep bots from becoming boring. 
There are a limited number of components to extend (2), 
these two components have a simple and clear function call order,
and rainbow mind machine tries to use sensible defaults.

That means we start out with bots that "just work" 
and we can incrementally improve, extend, override,
or redefine behaviors to make them increasingly complex,
while still abstracting away messy details.


## Installing rainbow mind machine

To install rainbow mind machine manually, use the 
normal `setup.py` procedure:

```
git clone https://github.com/charlesreid1/rainbow-mind-machine.git
cd rainbow-mind-machine
python setup.py build 
python setup.py install
```

To install rainbow mind machine with pip:

```
pip install rainbowmindmachine
```


## What You Will Need to Run a Bot Flock

You will need a few things before you can start using rainbow mind machine.

### A Bot Idea

You will need to decide on the behaviors
you want the bot to have, so you know how to 
structure the bot repo, what data to include,
and how to extend Sheep and Shepherd.

You will be defining how the Sheep 
(one sheep = one bot)
will populate their tweet queues.
This may be a simple action (get an item 
from a list owned by the Sheep), 
or it may be a complicated one
(make a URL request to get live data,
query a database, call an API, etc.).

See [`example_flocks/`](/example_flocks).

### Bot Flock Accounts

This tool handles everything _but_ the creation 
of the bot accounts. 

You _must_ have a Twitter account for each bot 
already created.

No customization of the account is needed - 
rainbow mind machine can take care of setting
profile, profile color, bio, and avatar information.

### A Twitter App

You also need to create a Twitter application.
You can use one application across all of your 
bot flocks - there is no limit on the number of 
accounts a single application can control.

It is recommended you create this app using a 
"bot master" account, and not using the bot 
accounts themselves.

This will register your rainbow mind machine bot flock 
application with Twitter, and give you credentials 
(a "consumer token" and a "consumer secret token" )
that will allow you to connect to Twitter's API
as the rainbow mind machine application that you are 
about to build.

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

Remember, we only have 3 objects we need to understand:

* The Keymaker (makes/manages keys and authenticates with Twitter)
* The Shepherd (one shepherd = one bot flock, runs the flock)
* The Sheep (one sheep = one bot, defines bot behavior)

### Keymaker: Authentication Step

The first step in rainbow mind machine is to run the Keymaker
to give the application permission to tweet on behalf of 
each of our bot users. This generates keys that the 
rainbow mind machine application requires be present 
to tweet as the bot flock.

The Keymaker takes a set of items, and creates
one key for each item. 

A set of items might be 
a Python list with integers, or a folder full of 
text files, or a set of URLs, or just plain old 
string labels.

The keys are what allow our application to tweet 
using a bot account. 

We call `make_a_key()` on each item to create each key.

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

Now you can run this in screen or as a background process,
and it will sequentially change each bot's 
Twitter page color, and will then spin up
one thread per sheep.


## More Examples

### Example: Ginsberg Bot Flock

Simple example, mutliple bots tweeting one line at a time,
one bot per file, associated with file

See [`example_flocks/ginsberg_botflock`](/example_flocks/ginsberg_botflock/)
and [b-ginsberg on git.charlesreid1.com](https://git.charlesreid1.com/bots/b-ginsberg).


### Example: Apollo Space Junk Bot Flock

Scheduling example, randomness and inner/outer loop,
one bot per file, associated with file,
generating dialogue from the file

See [`example_flocks/apollo_botflock`](/example_flocks/apollo_botflock/)
and [b-apollo on git.charlesreid1.com](https://git.charlesreid1.com/bots/b-apollo).


### Example: Mathematics Tripos Bot

Basically a photo-a-day bot, this bot posts a daily
mathematics tripos question (written in latex, converted to 
png format).

See [b-tripos on git.charlesreid1.com](git.charlesreid1.com/bots/b-tripos).




## Docker

To use rainbow mind machine from a docker container,
use the `Dockerfile` contained in this repository.

### Standalone Docker Container

You can use the `make_rmm_container.sh` script to build
the container (called `rmm_base`), or you can get the 
container image from dockerhub:

```
docker pull charlesreid1/rainbowmindmachine
```

### Docker Compose

For an example bot using rainbow mind machine in a docker container, see:

* [b-apollo](https://git.charlesreid1.com/bots/b-apollo)
* [b-ginsberg](https://git.charlesreid1.com/bots/b-ginsberg)
* [b-milton](https://git.charlesreid1.com/bots/b-milton)

The basic steps are as follows:

* Create a Twitter application
* Create a rainbow mind machine bot application
* Run the container pod interactively once with `docker-compose run <name-of-service>`
* Run the container pod in detached mode with `docker-compose up -d`


## Other Concerns

### Controlling the Docker Image Size

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

