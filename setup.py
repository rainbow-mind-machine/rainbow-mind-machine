from setuptools import setup

# see http://python-packaging.readthedocs.io/en/latest/minimal.html
# and https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
# and https://gist.github.com/gboeing/dcfaf5e13fad16fc500717a3a324ec17
# 
#   $ python setup.py register
#   $ python setup.py sdist
# 
# add following to ~/.pypirc:
# 
# [distutils]
# index-servers =
#     pypi
# 
# [pypi]
# username:charlesreid1
# password:YOURPASSWORDHERE
#
#   $ python setup.py sdist upload
#
# test it out with virtualenv:
#
#   $ virtualenv vp && cd vp
#   $ source bin/activate
#   $ bin/pip install rainbowmindmachine


setup(name='rainbowmindmachine',
      version='0.5.1',
      description='An extendable framework for running Twitter bot flocks.',
      url='http://charlesreid1.github.io/rainbow-mind-machine',
      author='charlesreid1',
      author_email='charles@charlesreid1.com',
      license='MIT',
      packages=['rainbowmindmachine'],
      zip_safe=False)

