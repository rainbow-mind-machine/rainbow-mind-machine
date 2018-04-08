#!/bin/bash
#
# Once you build this rmm container,
# you can build other images from it
# by putting the following in your Dockerfile:
# 
#    FROM rmm
#    ...
#
# If you haven't built this container,
# you'll get an error about docker 
# not being able to find a container
# named rmm.
#
# Eventually, rmm will be on pypi,
# and this Dockerfile will be in dockerhub.

docker build -t rmm_base .
