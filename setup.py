from setuptools import setup

version = "8"

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
        install_requires=['boringmindmachine==7',
            'TextBlob>=0.15'
        ],
        zip_safe=False)

