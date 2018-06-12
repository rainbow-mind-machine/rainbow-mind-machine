# Code Layout

Rainbow Mind Machine code is layed out as follows:

## Lumberjack Logger

The Lumberjack object creates a log and provides 
a way to interface with the log.

The default Lumberjack object uses python's
`logging` module.

The Lumberjack class can be extended to send log info
to other destinations, such as message queues or 
monitoring databases.

## Sheep (Twitter Bot Objects)

Bot objects own keys for a particular bot account.

Bot objects own an interface to Twitter for that bot account.

Bot objects own whatever things they need to tweet (poems, files, keys, accounts, etc.).

Each bot object has two timescales: the "outer wait" (residence time, longer in-between wait), 
and the "inner wait" (events timescale, in-betweeen individual lines or tweets).

Twitter object takes care of interfacing with Twitter, creating instances of Twitter API, 
uploading media, sending tweets, etc. For every bot, the tweet functionality works the same way.

### Sheep Example

I'll use the example of a Milton bot to illustrate how this works.

Each Milton bot owns a poem, which it tweets, one line at a time, in perpetuity.

Each Milton account also owns one Twitter account, which it is using to tweet the poem,
and owns that account by owning an API key. This API key is contained in a JSON file.
By giving each bot its own JSON file, we associate each bot with its own Twitter account.

(This account setup is done by the TwitterKeymaker class.)

The outer loop represents instances of finishing the whole poem.
The outer wait is the amount of time the bot waits once it has finished
the poem, before beginning it again.

The inner loop controls the line-by-line events. 
The inner wait is the amount of time the bot waits between each line of the poem.

## Shepherd (Twitter Bot Manager)

The Shepherd manages all of the Sheep bots.
It iterates through keys/poems/items 
and instantiates one Sheep for each item.
Once the Sheep are instantiated, they are 
pretty much roaming free on their own.
The Sheep manage their own tweeting behavior,
the Shepherd is mainly there to create the flock.

When performing actions on the entire flock,
the Shepherd is basically "wrapping" those actions
for each sheep.

Rather than define a wrapper for each individual action,
specific actions are defined in Sheep, and are wrapped by
a generic action method with an action keyword.

Shepherds can run an action in serial, iterating over
each sheep and performing the action. This is good for 
one-time actions like setting profile information.

Shepherds can also run actions in paralell, creating one 
thread per sheep. This is good for forever actions
like generating and sending tweets.


# Other Notes

## TwitterKeymaker

TwitterKeymaker is the only class that uses apikeys.py, which contains
the app's consumer tokens. These are used to get authentication 
tokens.

The app-level information in apikeys is also bundled with the 
account-level information created by TiwtterKeymaker, so TwitterKeymaker 
puts both into the Json file it creates. 

This way, apikeys.py is only required once, at time of key creation.
When Sheep load the json file, they have all the information 
they need.

## Shepherd

The Shepherd class is like a free-range parent.
The Sheep manage all of their own information,
and never need the Shepherd for anything.
The Shepherd just sets them to pasture.

## Sheep

The Sheep class is intended to provide sensible 
defaults, but also to be extremely flexible.
By overriding the various methods of the Sheep class,
we can obtain precisely the behavior we want - 
whether it's tweeting once a day, once an hour, 
or totally at random. 

The Sheep class can also handle complicated procedures
for populating the tweet queue. The Sheep class separates
the population of a tweet queue from the tweet action itself,
and this separation allows tweet population to be complicated.

