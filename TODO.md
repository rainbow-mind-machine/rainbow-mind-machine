# TODO

## add docker container test to tests

does the docker container build

can we run a command with it

can we run the tests in it

(triggering tests from tests??)

catch dumb stuff like - the very first time the photo bot hits a photo - splat, it dies.)

## wtf is with these stupid errors

This is running validate keys.

How the hell is this not being caught by tests?

I'm sick and tired of fixing these idiotic problems.

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


## documentation

focus on common tasks?

I want to set up my keys:
* Create keymaker
* Run keymaker
* Result: folder full of JSON files (bot keys)

I want to do something with my bot flock:
* Run Shepherd - it is the entrypoint
* Shepherd will check bot keys
* For each bot key, create new bot sheep
* Perform an action en masse


## fix the logger

Kill the lumberjack.

Use sys.stout and sys.stderr instead.


## tests

tests should always capture output,
even if doing nothing with it.

keymaker tests: done 

shepherd tests: in progress

sheep tests: in progress

logger tests: (N/A) (logging fixed as part of testing)


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

infrastructure: documentation
- mkdocs for documentation
- webhooks to build documentation

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

