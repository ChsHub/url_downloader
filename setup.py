import setuptools
from distutils.core import setup
from url_downloader import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='url_resource',
    version=__version__,
    description='Download url',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ChsHub',
    author_email='christian1193@web.com',
    packages=['url_resource'],
    license='MIT License',
    classifiers=['Programming Language :: Python :: 3.7']
)
# C:\Python37\python.exe -m pip install . --upgrade
# C:\Python37\python.exe setup.py sdist bdist_wheel
# C:\Python37\python.exe -m twine upload dist/*