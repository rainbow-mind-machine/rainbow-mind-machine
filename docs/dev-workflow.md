# Dev Workflow


# Documentation Workflow

To get a copy of the documentation locally:

## The Lazy Way

Checkout a copy of the `gh-pages` branch.

## Building Documentation

To generate documentation locally,
you will need mkdocs:

```
pip install mkdocs
```

To make the documentation, execute the `mkdocs build`
command from the main repository to build the site 
into the directory `source/`:

```
mkdocs build
```

To start a web server, use a lightweight python http server:

```
cd source/
python -m http.server 8000
```

or use mkdocs:

```
mkdocs serve
```


# Bug Fix Workflow

Workflow for propagating bug fixes and additions.


## Branch workflow

Branch workflow:

* development takes place on various feature branches
* the `master` branch contains the latest (unstable) code
* use tags to release particular versions


## Tags workflow

Tags workflow:

* When you've tested that everything is good to go:
* Increment version number in `setup.py`
* Update changelog
* Create tag for release

Create tag command:

```
git tag -a vX.Y -m 'rainbow mind machine X.Y'
```


## Pypy workflow 

Pypi workflow:

* One-time: set up your .pypirc
* Make the package bundle
* Upload the package bundle to Pypi
* Test the package with virtualenv
* 

## Dockerhub workflow


