# rainbow-mind-machine

An extendable framework for running Twitter bot flocks in Python.

```python

import rainbowmindmachine as rmm

k = rmm.Keymaker()
k.make_keys({
    'name':'Twitter Bot',
    'json':'key.json'
})

sh = rmm.Shepherd()

# Change everybody's Twitter page color
sh.perform_action('change color','#CFC')

# Everybody tweet in parallel
sh.perform_pool_action('tweet')

```

See the ```rainbowmindmachine``` directory for more details.
