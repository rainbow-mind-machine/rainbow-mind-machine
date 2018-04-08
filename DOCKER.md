# Using rainbow mind machine With Docker

To use rainbow mind machine from a docker container,
you can build the container yourself using the 
`Dockerfile` in this repository;
you can use a container image from dockerhub;
or you can use docker compose and the `docker-compose.yml` 
file in this directory.

## Building Standalone Docker Container

You can use the `make_rmm_container.sh` script to build
the base rainbow mind machien container 
(called `rmm_base`): 


## Pulling Docker Container

You can also pull the container from dockerhub:

```
docker pull charlesreid1/rainbowmindmachine
```

[rainbow mind machine on dockerhub]()

## Docker Compose

For an example bot using rainbow mind machine in a docker container, see:

* [b-apollo](https://git.charlesreid1.com/bots/b-apollo)
* [b-ginsberg](https://git.charlesreid1.com/bots/b-ginsberg)
* [b-milton](https://git.charlesreid1.com/bots/b-milton)

The basic steps are as follows:

* Create a Twitter application
* Create a rainbow mind machine bot application
* Run the container pod interactively once with `docker-compose run <name-of-service>`
* Run the container pod in detached mode with `docker-compose up -d`


## Developer Concerns

### Controlling the Docker Image Size

The official Python Docker images are huge: 
the absolute smallest image is 200 MB, and 
a full python 3 container using debian takes
nearly 1 GB. 

To reduce the size of these images, you can use 
a couple of strategies.

* Use alpine for the "real deal" - it is designed to be minimal 
    but requires bundling any "extras" into the container

* Use an image designed to be small
    * [jfloff/alpine-python](https://github.com/jfloff/alpine-python)

* Maintain logical separation 
    * one container per flock
    * one pod per server

