LIB=$(NAME)-mind-machine
SHORT=$(NAME)mindmachine
BMM_GH=git@github.com:rainbow-mind-machine/$(LIB).git
BMM_CMR=ssh://git@git.charlesreid1.com:222/bots/$(LIB).git
MKM_CMR=ssh://git@git.charlesreid1.com:222/charlesreid1/mkdocs-material.git

SHELL := /bin/bash

default: 


##########
# utils

fix_remotes: 
	git remote set-url origin $(BMM_GH)
	git remote set-url cmr $(BMM_CMR)

submodule_init:
	git submodule update --init


##############
# init_docs

init_docs: fix_remotes init_site init_mkdocs_material

init_site:
	rm -rf site
	git clone -b gh-pages $(BMM_GH) site && \
		cd site && git remote add cmr $(BMM_CMR)

init_mkdocs_material:
	wget https://tinyurl.com/sample-mkdocs-yml -O mkdocs.yml
	git submodule add $(MKM_CMR) \
		&& git add mkdocs-material mkdocs.yml .gitmodules \
		&& git commit mkdocs-material mkdocs.yml .gitmodules -m 'Initializing mkdocs-material submodule' \
		&& git push origin \
	mkdir docs && cp README.md docs/index.md


#############
# init_gh

init_gh: fix_remotes
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


###############
# deploy_docs

deploy_docs: 
	mkdocs build
	cd site \
		&& git add -A . \
		&& git commit -a -m 'updating gh-pages site' \
		&& git push origin gh-pages \
		&& git push cmr gh-pages



########################
# testing 1 2 3

test:
	nosetests -v
