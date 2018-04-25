# PyPi Notes to Self

### links:

http://python-packaging.readthedocs.io/en/latest/minimal.html

https://packaging.python.org/guides/migrating-to-pypi-org/#uploading

https://gist.github.com/gboeing/dcfaf5e13fad16fc500717a3a324ec17

### one time setup:

first you need to set up an account on pypi.

run this one time in your project
(note: apparently this is not needed anymore):

```
  $ python setup.py register
```

add the following to ~/.pypirc:

**~/.pypirc**:

```
[distutils]
index-servers =
    pypi

[pypi]
username:charlesreid1
password:YOURPASSWORDHERE
```

### new releases on pypi

Start by making a distribution package bundle:

```
$ python setup.py sdist
```

Upload it to pypi:

```
$ python setup.py sdist upload
```

Test it out with virutalenv:

```
  $ virtualenv vp && cd vp
  $ source bin/activate
  $ bin/pip install rainbowmindmachine
```

Note that if you have any problems 
and need to make any fixes, you'll 
have to bump the version number,
since you can't re-upload the 
same version of your software
twice.

