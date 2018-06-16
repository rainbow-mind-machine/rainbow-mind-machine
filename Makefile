NAME=rainbow
SHORTNAME=$(NAME)
include rules.mk

# run once right after you clone for the first time:
# make init_gh
# make init_mkdocs_material
#
# run once after you clone a local copy:
# make setup_site
#
# to serve docs locally while working on them:
# make serve_docs
# 
# when you are ready, run:
# make deploy_docs
