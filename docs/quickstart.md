# Quick Start

Let's walk through a quick example to illustrate
how this works.

Remember, we only have 3 objects we need to understand:

* The Keymaker (makes/manages keys and authenticates with Twitter)
* The Shepherd (one shepherd = one bot flock, runs the flock)
* The Sheep (one sheep = one bot, defines bot behavior)

# Keymaker: Authentication Step

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

# Running the Bot Flock

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

# Customizing Sheep

We didn't specify what kind of Sheep we want 
the Shepherd to create, so the Shepherd uses
the default `Sheep` class.

To change the behavior of your bot,
you can use built-in Sheep types
(`PhotoADaySheep`, `PoemSheep`, 
`QueneauSheep`, etc.) 
or you can extend the `Sheep` class
to define custom behaviors. 

For example,
to define a new `populate_queue()` 
behavior:

```
import rmm 

class CustomSheep(rmm.Sheep):
    def populate_queue(self,items):
        ...
```

Then modify the Shepherd to use this 
new Sheep class:

```python
# make the Shepherd
sh = rmm.Shepherd("keys/", sheep_class=CustomSheep)

# Change everybody's Twitter page color
sh.perform_action('change color','#CFC')

# Everybody tweet in parallel
sh.perform_pool_action('tweet')
```

# More Examples

## Example: Ginsberg Bot Flock

The Ginsberg bot flock is a simple example of 
a flock running multiple `PoemSheep`, with 
each Sheep loading a poem from a text file 
and tweeting the poem one line at a time.

See [`example_flocks/ginsberg_botflock`](/example_flocks/ginsberg_botflock/)
and [b-ginsberg on git.charlesreid1.com](https://git.charlesreid1.com/bots/b-ginsberg).

## Example: Apollo Space Junk Bot Flock

The Apollo Space Junk Bot Flock uses queneau generation
to create fake Apollo space mission radio chatter.
This bot flock runs multiple `QueneauSheep`.

See [`example_flocks/apollo_botflock`](/example_flocks/apollo_botflock/)
and [b-apollo on git.charlesreid1.com](https://git.charlesreid1.com/bots/b-apollo).

## Example: Mathematics Tripos Bot

The Math Tripos bot is basically a flock with a single photo-a-day bot.
It demonstrates how to create a bot flock with one single bot.

The Math Tripos bot has a directory full of 366 questions 
from the Cambridge University Mathematical Tripos,
in LaTeX format. Each LaTeX equation is converted to png.
The bot posts a new question each day.

See [b-tripos on git.charlesreid1.com](git.charlesreid1.com/bots/b-tripos).

