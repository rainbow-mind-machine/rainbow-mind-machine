# rainbow-mind-machine

An extendable framework for running Twitter bot flocks in Python.

```python

import rainbowmindmachine as rmm

k = rmm.Keymaker()

# Create some keys
k.make_key({
    'name':'Twitter Bot 1',
    'json':'key1.json'
})
k.make_key({
    'name':'Twitter Bot 2',
    'json':'key2.json'
})

# [Here, you will get a link where 
#  you will enter your Twitter credentials.]

# make the Shepherd
sh = rmm.Shepherd()

# Change everybody's Twitter page color
sh.perform_action('change color','#CFC')

# Everybody tweet in parallel
sh.perform_pool_action('tweet')

```

See the ```rainbowmindmachine``` directory for more details.

