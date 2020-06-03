import setuptools
from distutils.core import setup
from url_downloader import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='url_downloader',
    version=__version__,
    description=long_description.split('\n')[1],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ChsHub',
    url="https://github.com/ChsHub/url_downloader",
    packages=['url_downloader'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3.7'],
    requires=['requests']
)
# python -m pip install . --upgrade
# python setup.py sdist bdist_wheel
# python -m twine upload dist/*
