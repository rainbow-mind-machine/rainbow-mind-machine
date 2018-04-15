# Changelog

All notable changes to rainbow mind machine are documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0).

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

# [Planned for 1.0]

See [TODO.md](/TODO.md).

# [0.6.3] - 2018-04-15

### Fixed
- fixing another bug in photoaday bot due to another variable name

# [0.6.1] - 2018-04-15

### Fixed
- fixed a bug in photoaday bot due to a variable name. `docker logs <container-name>`

# [0.6] - 2018-04-14

### Added
- Added a changelog
- Added clarification to motivation behind rmm: 
    - we aren't providing templates for every bot you could possibly want to build
    - we are providing lego bricks for building the bot of your dreams
    - the defaults and templates are implemented as dead-simple low-maintenance bots
    - more advanced bots are totally possible, but YOU have to extend rainbow mind machine

### Changed
- Docker images now use [jfloff/alpine-python](https://github.com/jfloff/alpine-python)
- Final docker image size cut from >900 MB to 330 MB

### Fixed
- Major bug fixes for PhotoADay Sheep's sloppy import

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
