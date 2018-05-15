from setuptools import setup
from rainbowmindmachine import __version__
from pip.req import parse_requirements

with open('requirements.txt') as f:
    required = [x for x in f.read().splitlines() if not x.startswith("#")]

setup(  name='rainbowmindmachine',
        version=__version__,
        description='The extensible framework for running Twitter bot flocks.',
        url='https://pages.charlesreid1.com/b-rainbow-mind-machine',
        author='charlesreid1',
        author_email='charles@charlesreid1.com',
        test_suite='nose.collector',
        tests_require=['nose'],
        license='MIT',
        packages=['rainbowmindmachine'],
        install_requires=['simplejson>=3.13',
                'oauth2>=1.5',
                'python-twitter>=3.4.1',
                'TextBlob>=0.15',
                'oauth2client>=3.0.0'],
        zip_safe=False)

