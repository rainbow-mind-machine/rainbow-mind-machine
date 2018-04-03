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



