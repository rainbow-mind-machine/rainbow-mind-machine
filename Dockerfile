FROM jfloff/alpine-python:recent-onbuild
FROM alpine/git
MAINTAINER charles@charlesreid1.com

# This container defines a base rainbow mind machine image.
# This base container image is used to build other twitter bots.
# Eventually rmm will be on pypi and this will be 
#   on dockerhub.
# 
# However, for now, build it with the -t flag:
# 
#   docker build -t rmm_base .
# 
# and use 
# 
#   FROM rmm_base
# 
# in your bot Dockerfiles to start with rmm.
# This should also speed up your build!

RUN git clone https://github.com/charlesreid1/rainbow-mind-machine.git /rmm

RUN cd /rmm && \
    /usr/bin/env pip install -r requirements.txt && \
    /usr/bin/env python /rmm/setup.py build && \
    /usr/bin/env python /rmm/setup.py install

