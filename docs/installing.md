# Installing rainbow mind machine

To install rainbow mind machine manually, use the 
normal `setup.py` procedure:

```
git clone https://github.com/charlesreid1/rainbow-mind-machine.git
cd rainbow-mind-machine
python setup.py build 
python setup.py install
```

To install rainbow mind machine with pip:

```
pip install rainbowmindmachine
```

## Required Packages

If you need a list of required packages, see `requirements.txt`.
These packages will be installed using either of the above 
installation methods.

# What You Need to Run a Bot Flock

You will need a few additional things before you can get a bot flock
up and running with rainbow mind machine.

## A Bot Idea

You will need to decide on the behaviors
you want the bot to have, so you know how to 
structure the bot repository, what data to include,
and how to extend Sheep and Shepherd.

You will be defining how the Sheep 
(one sheep = one bot)
will populate their tweet queues.
This may be a simple action (get an item 
from a list owned by the Sheep), 
or it may be a complicated one
(make a URL request to get live data,
query a database, call an API, etc.).

See [`example_flocks/`](/example_flocks).

## Bot Master Account

It's good practice to create the Twitter application 
you'll be using to run your bot flock under a bot master account.

Like your Twitter application, the bot master account 
can be used to run as many bot flocks as you would like,
so you don't need to make it flock-specific.

This account is also (obviously) not itself a bot,
so you can use your personal twitter account 
as the bot master account.

## Bot Accounts

rainbow mind machine handles everything _but_ the creation of bot accounts. 
You must have a Twitter account for each bot already created.

No customization of the bot accounts is needed 
prior to using rainbow mind machine - 
rainbow mind machine can take care of setting
profile, profile color, bio, and avatar information.

## A Twitter App

You also need to create a Twitter application.
You can use one application across all of your 
bot flocks - there is no limit on the number of 
accounts a single application can control.

It is recommended you create this app using a 
"bot master" account, and not using the bot 
accounts themselves.

This will register your rainbow mind machine bot flock 
application with Twitter, and give you credentials 
(a "consumer token" and a "consumer secret token" )
that will allow you to connect to Twitter's API
as the rainbow mind machine application that you are 
about to build.

When you register your application Twitter will give you a consumer key 
and a consumer secret. Assign these values to the variables `consumer_key`
and `consumer_secret` in the file `apikeys.py`.

```
consumer_key    = '123456'
consumer_secret = '123456'
```

See the `apikeys.example.py` file.

