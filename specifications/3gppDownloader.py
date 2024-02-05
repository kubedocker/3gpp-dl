import requests
import json
import os
import shutil


from zipfile import ZipFile
from io import BytesIO
from urllib.parse import urlparse, unquote

from bs4 import BeautifulSoup

def generate_list(data):
    all_urls = []
    for rel, series_data in data.items():
        for urls in series_data.values():
            all_urls.extend(urls)
    return all_urls

def get_index(index_file):
    try:
        with open(index_file, 'r') as file:
            return json.load(file)
    except Exception as e:
        print(f"An error occurred: {e}.\nInitializing with an empty index list.")
        return []


def download_and_extract_docx(url, download_path='downloaded_files'):
    # 创建下载目录
    os.makedirs(download_path, exist_ok=True)

    # 下载文件
    response = requests.get(url)
    if response.status_code == 200:
        # 从响应中获取文件名
        filename = url.split('/')[-1]
        file_path = os.path.join(download_path, filename)

        # 将文件保存到本地
        with open(file_path, 'wb') as file:
            file.write(response.content)

        # 解压缩文件
        with ZipFile(file_path, 'r') as zip_ref:
            # 获取zip文件中的所有文件
            zip_file_contents = zip_ref.namelist()

            # 筛选出doc和docx文件
            doc_files = [file for file in zip_file_contents if file.endswith('.doc') or file.endswith('.docx')]

            # 提取doc和docx文件到目标目录
            for doc_file in doc_files:
                zip_ref.extract(doc_file, path=download_path)

        print(f"下载并解压成功，提取的doc/docx文件保存在 {download_path}")
    else:
        print(f"下载失败，状态码: {response.status_code}")

def download_and_extract_doc(url, download_path):
    if os.path.exists(download_path):
        shutil.rmtree(download_path)
        print(f'Deleted existing path: {download_path}')
    
    os.makedirs(download_path)


def generate_path_from_url(url):
    path_elements = urlparse(url).path.split('/')
    last = path_elements[-1]
    rel_path = '/'.join(path_elements[-3:-2] + [last[:last.rfind('-')]])
    
    return rel_path

if __name__ == '__main__':
    start_url = 'https://www.3gpp.org/ftp/Specs/latest/'
    
    ## Get DL
    rel_path = os.path.join(os.path.abspath(__file__), '../..', 'watchtower')
    abs_path = os.path.abspath(rel_path) + '/dl.json'
    print("Get latest json DL: ", abs_path)
    with open(abs_path, 'r') as file:
      data = json.load(file)
    url_list = generate_list(data)

    index_file = 'index.json'

    ## Get Old index
    old_index = get_index(index_file)

    new_index = [item for item in url_list if item not in old_index]

    print("Find updated index:")
    for url in new_index:
        path = generate_path_from_url(url)
        print(f"{url} --> {path}")
        download_and_extract_doc(url, path)

    

    '''
    with open(index_file, "w") as file:
      json.dump(url_list, file, indent=1)
    print(f"URL stored in {index_file}")
    '''
    
    
    
    
