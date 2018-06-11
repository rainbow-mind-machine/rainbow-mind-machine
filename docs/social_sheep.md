# SocialSheep

![the social sheep](sheep.jpg)

**The social rainbow mind machine sheep. [credit](credits.md)**

Social Sheep turn the normally reclusive and
interoverted Sheep into extroverted bots that can
interact with the Twitterverse through tweets.

The `SocialSheep` class implements the ability to search
for tweets matching a search term, and perform
actions with those tweets.

## Why "Social"?

Sometimes you want a Twitter bot to do things like
follow people, favorite tweets, or retweet tweets.
That's what Social Sheep are for.

Social Sheep will search for the last N tweets
matching a search term (e.g., a hashtag or a
keyword) and will return them in a list.

Social Sheep can then:

* favorite all of the tweets in the list;
* retweet all of the tweets in the list;
* follow all of the users who wrote the tweets;
* any combination of the above, and more.

## How to use it

Internally, the Social Sheep uses a toilet for an
analogy: each search for N tweets matching a search
term forms a small pool of tweets (a Toilet).
The toilet is flush()ed each time a search is
performed. The Social Sheep can favorite the
toilet, follow the toilet, or retweet the toilet,
and when it is finished, it will take a nap,
then it will flush the toilet and repeat the 
whole process again.

Creating a Shepherd that creates Social Sheep,
and then tells the Social Sheep to perform this
"forever" action, use the usual Keymaker,
then pass the SocialSheep type (part of the
`rainbowmindmachine` package) to the Sheperd
for the `sheep_class` parameter.

Here is some example code: three methods,
one to perform the OAuth authentication process
via the Keymaker, one to create a Shepherd and
perform the `tweet` action using the bot account, 
and the last to perform the `favorite_toilet` action
and repeatedly flush the toilet and favorite 
everything in the toilet forever.


```
import rainbowmindmachine as rmm

def setup():
    k = rmm.Keymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_a_key(
            name = 'social_bot',
            json_name = 'social_bot.json',
            keys_out_dir = 'keys'
        )


def tweet():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = rmm.SocialSheep
                    )

    sh.perform_action('tweet',
            publish = False,
            inner_sleep = 10,
            outer_sleep = 60
    )


def favorite():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = TestSocialSheep
                    )

    sh.perform_action('favorite_toilet',
            sleep = 60,
            search_term = '#rainbowmindmachine'
    )


if __name__=="__main__":
    tweet()
```

## Extending the Social Sheep

A quick example of how we can define our own
bot behavior by extending rainbow mind machine's
classes: here, we define a `populate_queue()`
method for our Social Sheep, which enables us
to customize both the tweeting and the favorite
toilet behavior of our Sheep:

```
import rainbowmindmachine as rmm

class SuperTweetingSocialSheep(rmm.SocialSheep):
    def populate_queue(self):
        tweet_queue = []
        tweet_queue.append('hello world 1/3 #rainbowmindmachine')
        tweet_queue.append('i am not a bot 2/3 #rainbowmindmachine')
        tweet_queue.append('do not be alarmed 3/3 #rainbowmindmachine')
        return tweet_queue


def setup():
    k = rmm.Keymaker()
    k.set_apikeys_file('apikeys.json')
    k.make_a_key(
            name = 'social_bot',
            json_name = 'social_bot.json',
            keys_out_dir = 'keys'
        )


def tweet():
    sh = rmm.Shepherd( json_keys_dir = 'keys/',
                       flock_name = 'simple flock',
                       sheep_class = TestSocialSheep
                    )

    sh.perform_action('tweet',
            inner_sleep = 10,
            outer_sleep = 60
    )

if __name__=="__main__":
    tweet()
```


