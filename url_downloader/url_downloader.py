"""
Simple download from url
"""
import math
from typing import Optional
from logging import info, exception, error
from shutil import move
from tempfile import gettempdir
from time import sleep
from hashlib import sha224
from requests import get
from requests.auth import AuthBase
from pathlib import Path
from re import findall
from tqdm import tqdm


class SaveToDisk:
    """
    Override requests.get to save file to target path
    """
    def __init__(self, file_path: Path, url: str):
        # Prevent name collisions by using hash
        self._temp_path = Path(
            gettempdir(),
            sha224(bytes(url, encoding='UTF-8')).hexdigest() +
            file_path.suffix)
        info(f'Temporary file for download: {self._temp_path}')
        self._file_path = file_path

    def _move_temporary(self, url: str) -> bool:
        """
        Move file to final location after the completed download
        :param url: Content url
        :return: True, if download was successful, or file already exists.
        """
        if self._file_path.exists():
            info('File already exists')
            return True
        # If download complete, make file permanent
        move(self._temp_path, self._file_path)
        info("DOWNLOADED: %s TO %s" % (url, self._file_path))
        return True

    def get(self,
            url: str,
            headers: dict,
            timeout: int,
            auth: Optional[AuthBase] = None) -> bool:
        """
        Function replaces requests.get so the url content is also saved as a file.
        Cancelling and resuming download is supported.
        :param url: Content url
        :param headers: Headers for response.get
        :param timeout: Timeout for response.get
        :param auth: Instance of authentication class from requests
        :return: True, if download was successful, or file already exists.
        """
        # '''http://masnun.com/2016/09/18/python-using-the-requests-module-to-download-large-files-efficiently.html'''
        # Get html stream
        resume_byte_pos = self._temp_path.stat(
        ).st_size if self._temp_path.exists() else 0

        # Add range header for resuming the download
        headers['Range'] = 'bytes=%d-' % resume_byte_pos
        response = get(url,
                       headers=headers,
                       stream=True,
                       timeout=timeout,
                       auth=auth)
        if response.status_code not in (200, 206):
            info('Wrong http response %s %s' %
                 (response.status_code, response.text))
            return False

        content_length = response.headers.get("Content-Length")
        chunk_size = 1048576  # 1Mo
        nb_chunks = math.ceil(float(content_length) / chunk_size)
        # Save to temporary file
        with open(self._temp_path, "ab") as f:
            for chunk in tqdm(response.iter_content(chunk_size=chunk_size),
                              total=nb_chunks):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)

        return self._move_temporary(url)


def _get_url_data(url: str,
                  get_function: callable,
                  tries: int,
                  timeout: int,
                  wait: int,
                  auth: Optional[AuthBase] = None):
    """
    Download the URL's content
    :param url: Content url
    :param get_function: requests.get or custom function
    :param tries: Number of retries, if the download failed
    :param timeout: Response.get timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :param auth: Instance of authentication class from requests
    :return: None, if download failed, or return value of the get_function
    """
    # Try download until it succeeds
    for i in range(tries):
        try:
            sleep(i)  # Wait time to prevent accidental DOS
            result = get_function(url,
                                  headers={'User-agent': 'Chrome'},
                                  timeout=timeout,
                                  auth=auth)
            if result:
                return result
        except Exception as e:
            if 'Read timed out' in str(e):
                info('Read timeout (try %s)' % i)
            else:
                error('Error on try %s' % i)
                exception(e)
    return None


def _get_file_name(url: str) -> str:
    """
    Produce file name from url string
    :param url: Download url
    :return: File name string
    """
    url = url.strip('/')
    result = findall(r'/(\w+\.\w+)[?|$]', url)
    if result:
        return result[-1]
    return url.split('/')[-1]


def save_file(url: str,
              file_path: str,
              file_name: str = '',
              timeout: int = 4,
              wait: int = 2,
              tries: int = 10,
              save_class: callable = SaveToDisk,
              auth: Optional[AuthBase] = None) -> bool:
    """
    Download file and save to disk.
    :param url: Url of the file
    :param file_path: File path
    :param file_name: File name
    :param timeout: Response timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :param tries: Number of download tries
    :param save_class: Class to manage saving file
    :param auth: Instance of authentication class from requests
    :return: True, if download successful or file already exists, False otherwise
    """
    if not file_name:
        file_name = _get_file_name(url=url)

    path = Path(file_path, file_name)
    if path.exists():
        info('File exists %s' % file_name)
        return True

    return _get_url_data(url,
                         save_class(file_path=path, url=url).get,
                         tries=tries,
                         timeout=timeout,
                         wait=wait,
                         auth=auth)


def get_resource(url: str,
                 timeout: int = 4,
                 wait: int = 2,
                 tries: int = 10,
                 auth: Optional[AuthBase] = None,
                 get_function: callable = get) -> str:
    """
    Get web resource as a string.
    :param url: Url of the file
    :param timeout: Response timeout in seconds
    :param wait: Wait time before download starts (in seconds)
    :param tries: Number of download tries
    :param auth: Instance of authentication class from requests
    :param get_function: requests.get or custom function
    :return: Resource as a string
    """
    data = _get_url_data(url,
                         get_function,
                         tries=tries,
                         timeout=timeout,
                         wait=wait,
                         auth=auth)
    if data:
        return data.text
    return data
