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
    author_email='christian1193@web.com',
    url="https://github.com/ChsHub/url_downloader",
    packages=['url_downloader'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3.7']
)
# C:\Python37\python.exe -m pip install . --upgrade
# C:\Python37\python.exe setup.py sdist bdist_wheel
# C:\Python37\python.exe -m twine upload dist/*
