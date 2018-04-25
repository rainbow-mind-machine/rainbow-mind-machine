from setuptools import setup

setup(name='rainbowmindmachine',
      version='0.6.6',
      description='An extendable framework for running Twitter bot flocks.',
      url='https://pages.charlesreid1.com/b-rainbow-mind-machine',
      author='charlesreid1',
      author_email='charles@charlesreid1.com',
      install_requires = ['simplejson==3.13',
                          'oauth2>=1.5',
                          'python-twitter==3.4.1',
                          'TextBlob==0.15'],
      license='MIT',
      packages=['rainbowmindmachine'],
      zip_safe=False)

