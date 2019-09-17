# python 3
from logging import info, exception, error
from shutil import move
from tempfile import gettempdir
from time import sleep

from os.path import join, getsize, exists
from requests import get


class SaveToDisk:
    def __init__(self, file_path, file_name):
        self._file = file_name
        self._path = file_path

    def get(self, url, headers, timeout):
        """
        Function replaces response.get so the url content is also saved as a file.
        Cancelling and resuming download is supported.
        :param url: Content url
        :param headers: Headers for response.get
        :param timeout: Timeout for response.get
        :return: True, if download was successful, or file already exists.
        """
        # '''http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html'''

        # Get full file path
        temp_path = join(gettempdir(), self._file)
        file_path = join(self._path, self._file)
        if exists(file_path):
            return True

        # Get html stream
        if exists(temp_path):
            resume_byte_pos = getsize(temp_path)
        else:
            resume_byte_pos = 0

        # Add range header for resuming the download
        headers['Range'] = 'bytes=%d-' % resume_byte_pos
        response = get(url, headers=headers, stream=True, timeout=timeout)

        if response.status_code != 206 and response.status_code != 200:
            info(response.status_code)
            raise ValueError('Wrong response')

        # Save to temporary file
        for chunk in response.iter_content(chunk_size=256):
            if chunk:  # filter out keep-alive new chunks
                with open(temp_path, "ab") as f:
                    f.write(chunk)

        # If download complete, make file permanent
        move(temp_path, self._path)
        info("DOWNLOADED: " + url + " TO " + file_path)
        return True


def _get_url_data(url: str, get_function, tries: int = 1000, timeout: int = 4, wait: int = 2):
    """
    Download the url's content.
    :param url: Content url
    :param get_function: response.get or custom function
    :param tries: Number of retries, if the download failed.
    :param timeout: Response.get timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :return: None, if download failed, or return value of the get_function
    """
    url = url.replace('&amp;', '&')  # TODO remove
    url = url.replace('amp;', '')  # TODO replacing this symbol? REMOVE THIS#

    # Try download until it succeeds
    for i in range(wait, tries):  # Wait time to prevent accidental DOS attack
        try:
            sleep(i)
            result = get_function(url, headers={'User-agent': 'Chrome'}, timeout=timeout)  # , verify=False
            return result
        except Exception as e:
            if 'Read timed out' in str(e):
                info('Read timeout (try %s)' % i)
            else:
                error('Error on try %s' % i)
                exception(e)

    return None


def save_file(url: str, file_path: str, file_name: str = '', timeout: int = 4, wait: int = 2) -> bool:
    """
    Download file and save to memory
    :param url: Url of the file
    :param file_path: File path
    :param file_name: File name
    :param timeout: Response timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :return: True, if download successful or file already exists, False otherwise
    """
    if not file_name:
        file_name = url.strip('/').split('/')[-1]  # Get last

    return _get_url_data(url, SaveToDisk(file_path, file_name).get, timeout=timeout, wait=wait)


def get_resource(url: str, timeout: int = 4, wait: int = 2) -> str:
    """
    Get web resource as a string.
    :param url: Url of the file
    :param timeout: Response timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :return: Resource as a string
    """
    data = _get_url_data(url, get, timeout=timeout, wait=wait)
    if data:
        return data.text
    return data
