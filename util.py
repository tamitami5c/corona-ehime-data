import urllib
import os
import requests

def get_file_name(url):
    path=urllib.parse.urlparse(url).path
    return os.path.split(path)[-1]

def download_file(url):
    file_name=get_file_name(url)

    response=requests.get(url)
    if response.status_code!=requests.codes.ok:
        raise Exception("status_code!=200")
    response.encoding=response.apparent_encoding

    with open(file_name,"wb") as f:
        f.write(response.content)
    return file_name