# Code Layout

Rainbow Mind Machine code is layed out as follows:


## Bot object

Bot objects own keys for a particular bot account.

Bot objects own an interface to Twitter for that bot account.

Bot objects own the 

Each bot object has two timescales: the "outer wait" (residence time, longer in-between wait), 
and the "inner wait" (events timescale, in-betweeen individual lines or tweets).

Twitter object takes care of interfacing with Twitter, creating instances of Twitter API, 
uploading media, sending tweets, etc. For every bot, the tweet functionality works the same way.

## 



