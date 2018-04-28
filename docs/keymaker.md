# The Keymaker

![the keymaker](keymaker.jpg)

**You can definitely trust this keymaker. [credit](credits.md)**

The Keymaker is the object that is used to 
authenticate with twitter and generate the 
oauth keys the application needs to do things
on behalf of a user.

There is a one-time authorization step needed
for each bot. The Keymaker generates an OAuth 
token request URL, the user visits the URL and 
signs in to Twitter, and the user then passes
a PIN number back to the Keymaker.

The Keymaker will generate keys for each bot,
and will store each bot's keys in a JSON file.
The Keymaker will not be needed again until a 
new set of keys need to be generated.

