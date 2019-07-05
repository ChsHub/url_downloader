# url_downloader
Simplify retrieving data from any url

## Installation
`python3 -m pip install url-downloader`

## Usage Examples

```python

from url_downloader import save_file
save_file(url='https://example.url/image.jpg', file_path='C:\\path', file_name='name.jpg')


```python

from url_downloader import get_resource
data = get_resource(url='https://example.url/')
