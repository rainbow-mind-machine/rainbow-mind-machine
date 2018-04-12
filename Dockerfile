#FROM jfloff/alpine-python:recent-slim
#FROM jfloff/alpine-python:recent-onbuild
# 
# use the above when we are able to install rmm with pip.
# (???)
# This container defines a base rainbow mind machine image.
# This base container image is used to build other twitter bots.

##################################
# this image is too fat

FROM python:3.6-stretch
MAINTAINER charles@charlesreid1.com

RUN git clone https://github.com/charlesreid1/rainbow-mind-machine.git /rmm

RUN cd /rmm && \
    /usr/bin/env pip install -r requirements.txt && \
    /usr/bin/env python /rmm/setup.py build && \
    /usr/bin/env python /rmm/setup.py install

