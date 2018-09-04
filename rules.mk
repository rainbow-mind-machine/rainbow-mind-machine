LIB=$(NAME)-mind-machine
SHORT=$(NAME)mindmachine
BMM_GH=git@github.com:rainbow-mind-machine/$(LIB).git
BMM_CMR=ssh://git@git.charlesreid1.com:222/bots/$(LIB).git
MKM_CMR=ssh://git@git.charlesreid1.com:222/charlesreid1/mkdocs-material.git

SHELL := /bin/bash

default: 


# set remote URLs and names
util_fix_remotes: 
	git remote set-url gh $(BMM_GH)
	git remote set-url cmr $(BMM_CMR)

# pull from upstream for each submodule
util_submodule_init:
	git submodule foreach git checkout master && git submodule foreach git pull origin master

# clone the site/ directory to be the gh-pages branch
clone_site:
	rm -rf site
	git clone -b gh-pages $(BMM_CMR) site && \
		cd site && \
		git remote rename origin cmr && \
		git remote add gh $(BMM_GH)

# build and deploy docs to gh-pages branch
deploy: 
	mkdocs build
	cd site \
		&& git add -A . \
		&& git commit -a -m 'updating gh-pages site' \
		&& git push gh gh-pages \
		&& git push cmr gh-pages

# build the documentation
build: 
	mkdocs build

# build and locally serve the documentation
serve: 
	mkdocs build
	mkdocs serve

# run tests
test:
	python setup.py test

# upload to pypi
pypi: pypi_upload pypi_test

pypi_upload:
	@echo "The following commands require that you have"
	@echo "your pypi credentials stored in ~/.pypirc"
	python setup.py sdist
	python setup.py sdist upload

pypi_test:
	virtualenv testmm
	source testmm/bin/activate
	testmm/bin/pip install $(SHORT)
	rm -rf testmm

