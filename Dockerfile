#FROM jfloff/alpine-python:recent-slim
#FROM jfloff/alpine-python:recent-onbuild
# 
# use the above when we are able to install rmm with pip.
#
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


##################################
# FAT

FROM python:3.6-stretch
MAINTAINER charles@charlesreid1.com

RUN git clone https://github.com/charlesreid1/rainbow-mind-machine.git /rmm

RUN cd /rmm && \
    /usr/bin/env pip install -r requirements.txt && \
    /usr/bin/env python /rmm/setup.py build && \
    /usr/bin/env python /rmm/setup.py install


#################################
# skinny
# no pip or python in the container
# 
# this whole approach is out.

### FROM alpine/git as gitbuilder
### MAINTAINER charles@charlesreid1.com
### RUN git clone https://github.com/charlesreid1/rainbow-mind-machine.git /rmm
### 
### FROM python:3.6-alpine
### WORKDIR /
### COPY --from=gitbuilder /rmm /rmm
### WORKDIR /rmm
### RUN pip3 install -r requirements.txt \
###     python3 setup.py build && \
###     python3 setup.py install

