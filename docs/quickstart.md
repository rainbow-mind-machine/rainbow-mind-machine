# Quick Start

Let's walk through a quick example to illustrate
how this works.

Remember, we only have 3 objects we need to understand:

* [The Keymaker](keymaker.md) (makes/manages keys and authenticates with Twitter)
* [The Shepherd](shepherd.md) (runs the flock; one shepherd = one bot flock)
* [The Sheep](sheep.md) (runs a bot, and defines bot's behavior; one sheep = one bot)

# Keymaker: Authentication Step

Also see the [keymaker](keymaker.md) page.

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

The Keymaker _requires_ that we specify
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
k.set_api_keys_env()

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

# A Shepherd to Run the Bot Flock

Also see the [shepherd](shepherd.md) page.

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

Also see the [sheep](sheep.md) page.

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

```python
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

Source code: [git.charlesreid1.com/bots/b-ginsberg](https://git.charlesreid1.com/bots/b-ginsberg).

Bot page: [pages.charlesreid1.com/b-ginsberg](https://pages.charlesreid1.com/b-ginsberg)

## Example: Paradise Lost Bot Flock

The Paradise Lost bot flock is another simple example 
of a flock running multiple `PoemSheep`, with 
each Sheep loading a poem from a text file 
and tweeting the poem one line at a time.

Source code: [git.charlesreid1.com/bots/b-milton](https://git.charlesreid1.com/bots/b-milton).

Bot page: [pages.charlesreid1.com/b-milton](https://pages.charlesreid1.com/b-milton)

## Example: Apollo Space Junk Bot Flock

The Apollo Space Junk Bot Flock uses queneau generation
to create fake Apollo space mission radio chatter.
This bot flock runs multiple `QueneauSheep`.

Source code: [git.charlesreid1.com/bots/b-apollo](https://git.charlesreid1.com/bots/b-apollo).

Bot page: [pages.charlesreid1.com/b-apollo](https://pages.charlesreid1.com/b-apollo)

## Example: Mathematics Tripos Bot

The Math Tripos bot is basically a flock with a single photo-a-day bot.
It demonstrates how to create a bot flock with one single bot.

The Math Tripos bot has a directory full of 366 questions 
from the Cambridge University Mathematical Tripos,
in LaTeX format. Each LaTeX equation is converted to png.
The bot posts a new question each day.

Source code: [git.charlesreid1.com/bots/b-tripos](https://git.charlesreid1.com/bots/b-tripos).

Bot page: [pages.charlesreid1.com/b-tripos](https://pages.charlesreid1.com/b-tripos)

