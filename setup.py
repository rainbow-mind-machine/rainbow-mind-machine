from setuptools import setup

version = "0.8.4"

setup(  name='rainbowmindmachine',
        version=version,
        description='The extensible framework for running Twitter bot flocks.',
        url='https://pages.charlesreid1.com/rainbow-mind-machine',
        author='charlesreid1',
        author_email='rainbowmindmachine@charlesreid1.com',
        test_suite='nose.collector',
        tests_require=['nose'],
        license='MIT',
        packages=['rainbowmindmachine'],
        install_requires=['boringmindmachine',
            'oauth2>=1.5',
            'simplejson>=3.13',
            'python-twitter>=3.4.1',
            'TextBlob>=0.15',
            'oauth2client>=3.0.0',
            'requests>=1.0.0'],
        zip_safe=False)

