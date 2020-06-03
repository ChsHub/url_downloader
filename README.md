# url_downloader
Simplify retrieving or downloading data from any url.
File downloads can be interrupted and continued later.

## Installation
`python3 -m pip install url-downloader`

## Usage Examples

Downloading files:
```python

from url_downloader import save_file
save_file(url='https://example.url/image.jpg', file_path='C:\\path', file_name='name.jpg')
```

Retrieving text data:
```python

from url_downloader import get_resource
data = get_resource(url='https://example.url/')
```