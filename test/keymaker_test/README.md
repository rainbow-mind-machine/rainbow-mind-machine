# Keymaker Tests

## Setting Up Tests

Running tests requires ```apikeys.py``` to be present.
The ```apikeys.py``` file contains your Twitter app's
consumer token and consumer secret.
You can find an example ```apikeys.py``` file in the 
```rainbowmindmachine``` directory (up one).

## Running Tests

To run the tests, just run them with Python:

```
python test_keymaker.py
```

This will attempt to create keys for each item.

### test keymaker

This tests the ability to create one key for each item
passed to the Keymaker by the user.

### test filekeymaker

This tests the ability to read a directory of files of 
arbitrary type and create one key for each text file.

### test txtkeymaker

This tests the ability to read a directory of text files
and create one key for each text file.

### the folders

* ```files/``` - contains dummy files of various types
    for testing FileKeymaker
* ```txt/``` - contains text files for testing TxtKeymaker

### the util

Just prints a little message.
