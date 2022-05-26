from pathlib import Path
from tempfile import TemporaryDirectory

from hypothesis import given
from hypothesis.strategies import text, integers

from url_downloader.url_downloader import _get_url_data, save_file, get_resource, _get_file_name


class SaveToDisk:
    def __init__(self, file_path, url):
        pass

    def get(self, url, headers, timeout):
        pass


@given(text())
def test__get_url_data(url: str):
    tries = 1
    timeout = 4
    wait = 0
    if url:
        assert _get_url_data(url, lambda x, headers, timeout: x, tries=tries, timeout=timeout, wait=wait) == url
    else:
        assert _get_url_data(url, lambda x, headers, timeout: x, tries=tries, timeout=timeout, wait=wait) is None


def test__get_file_name():
    assert _get_file_name('http://domain.com/filename.jpg') == 'filename.jpg'
    assert _get_file_name('http://domain.com/filename.jpg?w=1101') == 'filename.jpg'


@given(text())
def test_save_file(url: str):
    tries = 1
    timeout = 4
    wait = 0
    file_name = 'file_name'
    with TemporaryDirectory() as file_path:
        # Test existing file
        Path(file_path, file_name).touch()
        assert save_file(url=url, file_path=file_path, file_name=file_name, timeout=timeout, tries=tries, wait=wait,
                         save_class=SaveToDisk) is True


def test_get_resource():
    class TestResponse:
        text = 'file_name'

    tries = 1
    timeout = 4
    wait = 0
    file_name = 'file_name'
    with TemporaryDirectory() as file_path:
        # Test existing file
        file = Path(file_path, file_name)
        file.touch()
        url = file.as_uri()

        result = get_resource('', timeout=timeout, wait=wait, tries=tries,
                              get_function=lambda x, headers, timeout: TestResponse())
        assert type(result) == str


if __name__ == '__main__':
    test__get_url_data()
    test__get_file_name()
    test_save_file()
    test_get_resource()
