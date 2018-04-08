from setuptools import setup

# see http://python-packaging.readthedocs.io/en/latest/minimal.html
# and https://packaging.python.org/guides/migrating-to-pypi-org/#uploading
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
      version='0.4',
      description='An extendable framework for running Twitter bot flocks.',
      url='http://github.com/charlesreid1/rainbow-mind-machine',
      author='charlesreid1',
      author_email='charles@charlesreid1.com',
      license='MIT',
      packages=['rainbowmindmachine'],
      zip_safe=False)

