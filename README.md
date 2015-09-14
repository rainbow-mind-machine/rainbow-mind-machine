# rainbow-mind-machine

An extendable framework for running Twitter bot flocks in Python.

## Install

```
git clone https://github.com/charlesreid1/rainbow-mind-machine.git
cd rainbow-mind-machine
python setup.py build 
python setup.py install
```

## Credentials

You will need to put your Twitter credentials
into apikeys.py, which will contain
your consumer key and consumer secret key.

```
consumer_key    = '123456'
consumer_secret = '123456'
```

See the `apikeys.example.py` file.

## Link Bot to Twitter Account 

Each key is linked to an "item". 
This might be a text file, a poem, 
a corpus of text, or whatever.

In the example below, the "items"
are names of twitter bots. This will 
use credentials in apikeys.py,
and output key files to `key1.json` 
and `key2.json`.

```python

import rainbowmindmachine as rmm
import subprocess

subprocess.call(['mkdir','-p','keys/'])

k = rmm.Keymaker()

# Create some keys
k.make_key({
    'name':'Twitter Bot 1',
    'json':'keys/key1.json'
})
k.make_key({
    'name':'Twitter Bot 2',
    'json':'keys/key2.json'
})

# [Here, you will get a link where 
#  you will enter your Twitter credentials.]
```

Now you can make a Shepherd for your bot flock,
and point it to the keys you just created:

```python
import rainbowmindmachine as rmm

# make the Shepherd
sh = rmm.Shepherd("keys/")

# Change everybody's Twitter page color
sh.perform_action('change color','#CFC')

# Everybody tweet in parallel
sh.perform_pool_action('tweet')

```

See the ```rainbowmindmachine``` directory for more details.

