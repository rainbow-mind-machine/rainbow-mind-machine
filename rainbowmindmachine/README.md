# Code Layout

Rainbow Mind Machine code is layed out as follows:

## Sheep: Bot objects

Bot objects own keys for a particular bot account.

Bot objects own an interface to Twitter for that bot account.

Bot objects own whatever things they need to tweet (poems, files, keys, accounts, etc.).

Each bot object has two timescales: the "outer wait" (residence time, longer in-between wait), 
and the "inner wait" (events timescale, in-betweeen individual lines or tweets).

Twitter object takes care of interfacing with Twitter, creating instances of Twitter API, 
uploading media, sending tweets, etc. For every bot, the tweet functionality works the same way.

## Sheep: Example

I'll use the example of a Milton bot to illustrate how this works.

Each Milton bot owns a poem, which it tweets, one line at a time, in perpetuity.

Each Milton account also owns one Twitter account, which it is using to tweet the poem,
and owns that account by owning an API key. This API key is contained in a JSON file.
By giving each bot its own JSON file, we associate each bot with its own Twitter account.

(This account setup is done by the Keymaker class.)

The outer loop represents instances of finishing the whole poem.
The outer wait is the amount of time the bot waits once it has finished
the poem, before beginning it again.

The inner loop controls the line-by-line events. 
The inner wait is the amount of time the bot waits between each line of the poem.

## Shepherd: Bot manager

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



# Other Notes

## Keymaker

Keymaker is the only class that uses apikeys.py, which contains
the app's consumer tokens. these are used to get authentication 
tokens.

The app-level information in apikeys is also bundled with the 
account-level information created by Keymaker, so Keymaker 
puts both into the Json file it creates. 

This way, apikeys.py is only required once, at time of key creation.
When Sheep load the Json file, they have all the information 
they need.

## Shepherd

So actually, the Shepherd doesn't even manage app-level information.
Sheep have everything they need.

Shepherds, then, seem like Free-Range Parents.

## Sheep








