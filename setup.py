from setuptools import setup
from rainbowmindmachine import __version__

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

setup(  name='rainbowmindmachine',
        version=__version__,
        description='An extendable framework for running Twitter bot flocks.',
        url='https://pages.charlesreid1.com/b-rainbow-mind-machine',
        author='charlesreid1',
        author_email='charles@charlesreid1.com',
        test_suite='nose.collector',
        tests_require=['nose'],
        license='MIT',
        packages=['rainbowmindmachine'],
        install_requires=required,
        zip_safe=False)

