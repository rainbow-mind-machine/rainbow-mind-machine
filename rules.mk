LIB=$(NAME)-mind-machine
SHORT=$(NAME)mindmachine
BMM_GH=git@github.com:rainbow-mind-machine/$(LIB).git
BMM_CMR=ssh://git@git.charlesreid1.com:222/bots/$(LIB).git
MKM_CMR=ssh://git@git.charlesreid1.com:222/charlesreid1/mkdocs-material.git

SHELL := /bin/bash

default: 


util_fix_remotes: 
	git remote set-url origin $(BMM_GH)
	git remote set-url cmr $(BMM_CMR)

util_submodule_init:
	git submodule update --init

# run once, after first clone, to create gh-pages branch
init_gh: util_fix_remotes
	rm -rf site && git clone $(BMM_GH) site
	set -x \
		&& cd site/ \
		&& git remote add cmr $(BMM_CMR) \
		&& git checkout --orphan gh-pages \
		&& rm -rf * .gitmodules .gitignore \
		&& echo '<h2>hello world</h2>' > index.html \
		&& git add index.html \
		&& git commit index.html -m 'add init commit on gh-pages branch' \
		&& git push origin gh-pages \
		&& git push cmr gh-pages \
		&& set +x

# run once, after first clone, to add mkdocs submodule
init_mkdocs_material:
	wget https://tinyurl.com/sample-mkdocs-yml -O mkdocs.yml
	git submodule add $(MKM_CMR) \
		&& git add mkdocs-material mkdocs.yml .gitmodules \
		&& git commit mkdocs-material mkdocs.yml .gitmodules -m 'Initializing mkdocs-material submodule' \
		&& git push origin \
	mkdir docs && cp README.md docs/index.md

# set up docs folder after cloning local copy
setup_docs: fix_remotes util_submodule_init setup_site 

# clone a copy of the gh-pages branch to gh-pages
setup_site:
	rm -rf site
	git clone -b gh-pages $(BMM_GH) site && \
		cd site && git remote add cmr $(BMM_CMR)

# build and deploy the documentation
deploy_docs: 
	mkdocs build
	cd site \
		&& git add -A . \
		&& git commit -a -m 'updating gh-pages site' \
		&& git push origin gh-pages \
		&& git push cmr gh-pages

# build and locally serve the documentation
serve_docs: 
	mkdocs build
	mkdocs serve

# run tests
test:
	nosetests -v

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

