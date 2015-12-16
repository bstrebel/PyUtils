from setuptools import setup
import re

version = re.search(
    "^__version__\s*=\s*'(.*)'",
    open('pyutils/__init__.py').read(),
    re.M).group(1)

setup(
    name='PyUtils',
    version=version,
    packages=['pyutils'],
    url='https://github.com/bstrebel/PyUtils',
    license='GPL2',
    author='Bernd Strebel',
    author_email='b.strebel@digitec.de',
    description='Python Utilities Package',
    long_description=open('README.md').read()
    #install_requires=['requests']
)
