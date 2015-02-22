# Rainbow Mind Machine Tests

## Step 1: Keymaker Tests

Run tests in ```keymaker_tests/```. There are three tests for the three Keymaker types.

Keymaker tests will, if you authorize them to use your account, create keys in the ```keys/```
directory. 

## Step 2: Shepherd Tests

This performs tests to make sure we can create 
a Shepherd with a bundle of keys. 

This test will create a Shepherd, which then creates 
a flock of Sheep. 

It also tests performing an action sequentially,
then performing an action in parallel using 
multithreading.

## Step 3: Sheep Tests



