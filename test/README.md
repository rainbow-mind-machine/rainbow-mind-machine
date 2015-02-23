# Rainbow Mind Machine Tests

Tests for rainbow-mind-machine should happen in two steps, corresponding to 
the two steps of using rainbow-mind-machine: 

1. Creating keys with the Keymaker

2. Running the Shepherd/Sheep bot flock

## Step 1: Keymaker Tests

Run tests in ```keymaker_tests/```. There are three tests for three Keymaker types.

Keymaker tests will, if you authorize them to use your account, create keys in the ```keys/``` directory. 
These keys are used for later tests.

## Step 2: Shepherd/Sheep Tests

This performs tests to make sure we can create a Shepherd with a bundle of keys. 

The Shepherd creates a flock of Sheep, one for each key. 

The Shepherd tests its ability to run Sheep actions sequentially.

It then tests its ability to run Sheep actions in parallel using multithreading.


