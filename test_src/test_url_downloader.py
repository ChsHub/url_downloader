from hypothesis import given, settings
from hypothesis.strategies import text, integers

from url_downloader.url_downloader import _get_url_data, save_file, get_resource


class SaveToDisk:

    def test_get(self, url, headers, timeout):
        pass


@settings()
@given(text(), integers(), integers(), integers(0, 2))
def test__get_url_data(url: str, tries: int = 1000, timeout: int = 4, wait: int = 2):
    get_function = lambda x: x
    _get_url_data(url, tries, timeout, wait)


@given(text(), integers(), integers(), integers(0, 2))
def test_save_file(url: str, file_path: str, file_name: str = '', timeout: int = 4, wait: int = 2):
    save_file(url, file_path, file_name, timeout, wait)


@given(text(), integers(), integers(), integers(0, 2))
def test_get_resource(url: str, timeout: int = 4, wait: int = 2):
    get_resource(url, timeout, wait)


if __name__ == '__main__':
    test__get_url_data()
    test_save_file()
    test_get_resource()
