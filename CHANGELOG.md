# Changelog

All notable changes to rainbow mind machine are documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [Planned for 1.0]

See [TODO.md](/TODO.md).

# [0.8] - 2018-06-10

### Added

- SocialSheep
    - currently just takes a search term
    - favorites/follows/retweets/etc

### Changed

- Sheep and Shepherd use `**kwargs` and stop fiddling around
    with this `extra_params` business
    - this will break stuff

# [0.7] - 2018-05-15

### Added

- Added tests for Keymaker
- Added tests for Shepherd
- Added documentation for Sheep, Shepherd, Keymaker
- Improved dev workflow documentation

### Changed

- Changed how media is attached to tweet
    - Sheep.tweet() now takes a media argument
    - Let python-twitter library handle media
    - PhotoADaySheep uses media argument of tweet method
- Changed apikeys.py arrangement to take filename arg
    - Importing as module was problematic for tests
    - Now pass in using a JSON file, a dictionary, or env vars

# [0.6] - 2018-04-15

### Added

- Added a changelog
- Added clarification to motivation behind rmm: 
    - we aren't providing templates for every bot you could possibly want to build
    - we are providing lego bricks for building the bot of your dreams
    - the defaults and templates are implemented as dead-simple low-maintenance bots
    - more advanced bots are totally possible, but YOU have to extend rainbow mind machine

### Changed

- changed URL for project to https://pages.charlesreid1.com/rainbow-mind-machine
- Docker images now use [jfloff/alpine-python](https://github.com/jfloff/alpine-python)
- Final docker image size cut from >900 MB to 330 MB

### Fixed

- fixed a bug in photoaday bot due to a variable name. `docker logs <container-name>`
- fixing another bug in photoaday bot due to another variable name
- fixing failed upload with 0.6.2
- Major bug fixes for PhotoADay Sheep's sloppy import

### Removed

- removed dependency on TwitterAPI

# [0.5] - 2018-04-12

### Added
- Added documentation folder

### Changed
- Fixed a bug with photo bot explicitly using `rmm`

# [0.4] - 2018-04-08

### Added 
- Began using semantic versioning
- Added setup.py and pip-friendly packaging
- Added Dockerfile
- Added project to Pypi: [rainbowmindmachine](https://pypi.python.org/pypi/rainbowmindmachine)
- Added project to Dockerhub
- Based other bot projects on rmm 
    (see [bots on git.charlesreid1.com](https://git.charlesreid1.com/bots))
- Sheep actios: follow someone, unfollow someone
- Sheep/Shepherd use dispatcher pattern to perform actions

### Changed
- Converted all code to Python 3
- Replaced old photo bot (different twitter API) with tripos engine

### Deprecated
- Python 2 no longer supported

### Removed

### Fixed


(Some links to specific tags ought to go here...)

