FROM python:3.6
MAINTAINER charles@charlesreid1.com

# ideally, we could do pip install rainbow-mind-machine
# even better: pip install -e git://github.com/{ username }/{ reponame }.git@{ tag name }#egg={ desired egg name }

ADD entrypoint.sh /entrypoint.sh

RUN apt-get update 
RUN apt-get -y install git curl
RUN git clone https://git.charlesreid1.com/bots/b-rainbow-mind-machine.git

CMD ["/entrypoint.sh"]

