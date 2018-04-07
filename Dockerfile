FROM jfloff/alpine-python:recent-onbuild
MAINTAINER charles@charlesreid1.com

# This container defines a base rainbow mind machine image.
# This base rmm image is used to build other twitter bots.
# Eventually rmm will be on pypi and this will be 
#   on dockerhub.

RUN git clone https://github.com/charlesreid1/rainbow-mind-machine.git /rmm

RUN cd /rmm && \
    /usr/bin/env pip install -r requirements.txt && \
    /usr/bin/env python /rmm/setup.py build && \
    /usr/bin/env python /rmm/setup.py install

