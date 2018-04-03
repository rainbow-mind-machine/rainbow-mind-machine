# TODO

Keymaker:
- make this into a command line program
- keymaker: files-based keymaker, and items-based keymaker
- logging: ???
- split key generation/authentication step and tweet/action step
- expand and document the actions better
- when it looks for where to put the keys:
    - we run an open() on the filename the user passes
    - no check whether it is a directory or a file
    - no check whether it exists
    - no mkdir -p command
    - fix this!!!

sheep:
- use the dispatch design pattern 
- what does a sheep do by default?
    - tweet calls _tweet(twit)
    - twit comes from populate_queue()
    - populate_queue() by default creates five hello world messages
- address the question: what methods does the user need to override?
    - do they override tweet()?
    - do they override populate_queue()?
    - can they just set parameters?
    - can they write a custom routine that takes new parameters?
- what actions are defined?
- can bots upload multimedia?
- what actions are not implemented (add to the todo)

sheep actions:
- follow someone 
- unfollow someone 
- everyone tweet at someone 
- important: we are NOT trying to cover every possible base
- NOT just showing how to use existing objects
- showing how and where to add new functionality (extensible)
- abstracts away the details of credential management for multiple bots
- abstracts away the storage of keys and bot-specific information
- that way, you can focus on extending the sheep to do what you want

examples/tests:
- what is a "flickr bot"?
- how can we best describe the pattern of associating a file with a bot?

infrastructure:
- mkdocs for documentation
- dockerfile
- python package index
- travis/circleci/tox?
- how to get credentials into containers, in secret?
- [my pypi checklist](https://gist.github.com/audreyr/5990987)
    - history (changelog)
    - update version number
    - install with new version number
    - run tests 
    - release on pypi (sdist, wheel)
    - make temporary environment
    - ensure it installs
    - git push
    - git push tags
- [cookie cutter python package](https://github.com/audreyr/cookiecutter-pypackage)
    - testing setup
    - travis setup
    - tox testing
    - sphinx docs
    - bumpversion
    - autorelease to pypi
    - command line interface with click












