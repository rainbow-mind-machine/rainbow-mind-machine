# TODO


## Documentation

On the one hand, it feels like a bit too much.

On the other hand, too much to explain.

Focus on common tasks (relates to clarifying who stores what):

* I want to set up my keys. What do I do?
    * Create a Keymaker
    * Run the Keymaker
    * Outcome is folder full of JSON files

* I want to do something with my bot flock
    * run Shepherd, which is the flock entry point
    * Shepherd will check bot keys
    * for each bot key, create a new bot Sheep
    * perform an action en masse

Clarifying the role of each thing (see issues).


### Logging

Add logging to the documentation.

Unfortunately, even after revamping the entire logging system,
I'm still a bit fuzzy on how it works, and I still don't think
it's doing what it needs to do.


## Examples

Going through a deep clean of each class, fully documenting,
leads to many loose ends.

To keep the documentation reasonable and readable,
move illustrative details into the examples,
and refer to them in the documentation.


### Usability Examples

How do I use this thing?

Like the tests, but less "test" and more "octo-banana".


### Extensibility Examples

How and when do I extend the Keymaker?

How and when do I extend the Shepherd?

How and when do I extend the Sheep?


## Testing

An absolute slog, but also important.


### Tests Need To Write

<s>Logger tests</s> (logging fixed as part of testing)

<s>Keymaker tests</s> done

Shepherd tests (in progress)

Sheep tests


### Container Tests

Tests of the docker container:

* Does the docker container build
* Can we run a command with it
* Can we run the non-auth tests in it (triggering tests from tests)
* Catch dumb stuff like copying into wrong dir in container


### Really Stupid Errors Not Being Caught By Tests

```
----------------------------------------
INFO:rainbowmindmachine:----------------------------------------
Flock name: Anonymous Flock of Cowards
INFO:rainbowmindmachine:Flock name: Anonymous Flock of Cowards
Flock log file: rainbowmindmachine.log
INFO:rainbowmindmachine:Flock log file: rainbowmindmachine.log
----------------------------------------
INFO:rainbowmindmachine:----------------------------------------
Bot Flock Shepherd: Validating keys
INFO:rainbowmindmachine:Bot Flock Shepherd: Validating keys
Traceback (most recent call last):
  File "TriposBot.py", line 46, in <module>
    run()
  File "TriposBot.py", line 17, in run
    sheep_class = rmm.PhotoADaySheep)
  File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.7.2-py3.6.egg/rainbowmindmachine/Shepherd.py", line 74, in __init__
    self._setup_keys(json_keys_dir)
  File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.7.2-py3.6.egg/rainbowmindmachine/Shepherd.py", line 116, in _setup_keys
    if _key_is_valid(json_key_file):
NameError: name '_key_is_valid' is not defined
running bot
```



```
[36mstormy_tripos_1    |[0m [2018-04-16 16:40:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:42:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:44:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:46:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:48:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:50:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:52:08 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:54:09 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:56:09 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m [2018-04-16 16:58:09 @math_tripos] Sleeping...
[36mstormy_tripos_1    |[0m running bot
[36mstormy_tripos_1    |[0m Traceback (most recent call last):
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.6.4-py3.6.egg/rainbowmindmachine/PhotoADaySheep.py", line 210, in photo_a_day
[36mstormy_tripos_1    |[0m     img_info = self.upload_image_to_twitter(tweet_params)
[36mstormy_tripos_1    |[0m AttributeError: 'PhotoADaySheep' object has no attribute 'upload_image_to_twitter'
[36mstormy_tripos_1    |[0m 
[36mstormy_tripos_1    |[0m During handling of the above exception, another exception occurred:
[36mstormy_tripos_1    |[0m 
[36mstormy_tripos_1    |[0m Traceback (most recent call last):
[36mstormy_tripos_1    |[0m   File "TriposBot.py", line 46, in <module>
[36mstormy_tripos_1    |[0m     run()
[36mstormy_tripos_1    |[0m   File "TriposBot.py", line 36, in run
[36mstormy_tripos_1    |[0m     'images_pattern' : '{i:03}.jpg'
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.6.4-py3.6.egg/rainbowmindmachine/Shepherd.py", line 111, in perform_pool_action
[36mstormy_tripos_1    |[0m     results = pool.map(do_it,self.all_sheep)
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/multiprocessing/pool.py", line 266, in map
[36mstormy_tripos_1    |[0m     return self._map_async(func, iterable, mapstar, chunksize).get()
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/multiprocessing/pool.py", line 644, in get
[36mstormy_tripos_1    |[0m     raise self._value
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/multiprocessing/pool.py", line 119, in worker
[36mstormy_tripos_1    |[0m     result = (True, func(*args, **kwds))
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/multiprocessing/pool.py", line 44, in mapstar
[36mstormy_tripos_1    |[0m     return list(map(*args))
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.6.4-py3.6.egg/rainbowmindmachine/Shepherd.py", line 108, in do_it
[36mstormy_tripos_1    |[0m     sheep.perform_action(action,params)
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.6.4-py3.6.egg/rainbowmindmachine/PhotoADaySheep.py", line 60, in perform_action
[36mstormy_tripos_1    |[0m     method( params )
[36mstormy_tripos_1    |[0m   File "/usr/lib/python3.6/site-packages/rainbowmindmachine-0.6.4-py3.6.egg/rainbowmindmachine/PhotoADaySheep.py", line 245, in photo_a_day
[36mstormy_tripos_1    |[0m     raise Exception(err)
[36mstormy_tripos_1    |[0m Exception: 'PhotoADaySheep' object has no attribute 'upload_image_to_twitter'
```


## do it now

examples:
- fix up examples

Logging:
- in the process of setting up tests, work out the logging too
- what happens when stuff fails?
- how do we catch exceptions more gracefully?
- how do we record exceptions in the log file?

MQ Logging:
- what would it take to add a backend plugin to log to MQ?

Keymaker:
- when it looks for where to put the keys:
    - we run an open() on the filename the user passes
    - no check whether it is a directory or a file
    - no check whether it exists
    - no mkdir -p command
    - fix this!!!

sheep:
- add new actions 

infrastructure: pypi
- branches and tags on pypi?
    - stable branch
    - dev branch
    - tags

infrastructure: dockerhub
- dockerhub webhooks - what does dockerhub trigger?
- github webhooks - dockerhub registry webhook set up 
- branches and tags on dockerhub?
    - stable branch
    - dev branch
    - tags


## documentation

screenshot video:
- abbreviated version of signing in and setting up keys
- the basic bot 
- running the bot
- seeing the output

philosophy of rmm: p1
- important: we are NOT trying to cover every possible base
- NOT just showing how to use existing objects
- showing how and where to add new functionality (extensible)
- abstracts away the details of credential management for multiple bots
- abstracts away the storage of keys and bot-specific information
- that way, you can focus on extending the sheep to do what you want

philosophy of rmm: p2
- going through photoaday bot
- not bending over backwards to provide stellar templates
- it's actually much faster for the user to write their own
- we give you the lego blocks
- you design your own lego ship
- not a movie set miniature

the main idea:
- three core objects
- keymaker, shepherd, sheep (and lumberjack)
- two steps: set up keys, run forever

Keymaker:
- keymaker: files-based keymaker, and items-based keymaker

Sheep:
- default behavior
- patterns for overriding
    - word examples
    - code examples
- what does a sheep do by default?
    - tweet calls `_tweet(twit)`
    - twit comes from `populate_queue()`
    - `populate_queue()` by default creates five hello world messages
    - let the user know, this is the method to override
- address the question: what methods does the user need to override?
    - do they override tweet()?
    - do they override `populate_queue()`?
    - can they just set parameters?
    - can they write a custom routine that takes new parameters?
- what actions are defined?
- can bots upload multimedia?


## done

<s>upgrade to python 3:
- go through and improve/modernize everything
- print statements
- etc.</s>

<s>docstrings:
- Keymaker docstrings
- Shepherd docstrings
- Sheep docstrings</s>

<s>documentation:
- mkdocs</s>



## do it later

pypi checkist:
* changelog
* bump version number
* install with new verion number
* run tests
* release on pypi (sdist, wheel)
* make temp env
* ensure installation works
* git push
* git push tags


pypi:
- travis/circleci/tox?
- how to get credentials into containers, in secret?
- [cookie cutter python package](https://github.com/audreyr/cookiecutter-pypackage)
    - testing setup
    - travis setup
    - tox testing
    - sphinx docs
    - bumpversion
    - autorelease to pypi
    - command line interface with click

prepare for pypi release:
- tests without credentials
- tests with credentials

