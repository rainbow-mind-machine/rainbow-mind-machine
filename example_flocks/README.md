# How to Create a Bot Flock

This document walks through the creation of a hypothetical
bot flock.

## Step 0: Create Twitter App 

Before you can do anything with a Twitter bot 
you'll have to get an app key from Twitter.

Visit [http://dev.twitter.com](http://dev.twitter.com)

Once you have set up your app through
Twitter developer, you will be able to
see a consumer token and a consumer 
secret key. These are the values 
that go in the file ```apikeys.py```.

The ```apikeys.py``` file is required
to create keys for new bots. Its only
purpose is to hold the consumer token
and consumer secret.

It looks like this:

```python
consumer_key    = 'AAAAAAAAAAAAAAAA'
consumer_secret = 'BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB'
```

## Step 1: Create Email Alias 

importance of being able to quickly set up new email aliases

aliases, not accounts, because want everything going to same place

## Step 2: Create Twitter Account

Now you'll go to [twitter.com](http://twitter.com) and sign up for a new account.
When it asks you for your email, pass the email address alias that you created above.

### If Twitter Asks For Your Phone Number

If you are asked for a phone number during the account creation process, skip that step.

Press the skip button. If there's no skip button,
just navigate to a different page, or change the URL of the page. By the time 
it asks you for your phone number, it has already finished setting up your account - 
so if you cancel the process before giving a phone number, your account has still 
been created.

The same is true of Twitter asking you to pick 10 people to follow. Your account
has already been set up, so if you don't want to pick people to follow,
you can juts navigate away from that page.

## Step 3: Confirm Email

Twitter will require you to confirm your email for your acount. This should be 
straightforward, since we used an email alias, and so we don't have to check
a separate email address for each bot.

## Step 4: Install Rainbow Mind Machine

Yup. Go do it. [rainbow-mind-machine](https://github.com/charlesreid1/rainbow-mind-machine)

## Step 5: Authenticate with Keymaker

Now you'll authenticate your app and give it permission to tweet using the Keymaker class:

```python
import rainbowmindmachine as rmm

k = rmm.Keymaker()
k.make_keys('poems/')
```

This will create a bot for each text file in the ```poems/``` directory.

## Step 6: Update Account Settings

## Step 7: Customize Sheep Behavior

## Step 8: Tweet!
