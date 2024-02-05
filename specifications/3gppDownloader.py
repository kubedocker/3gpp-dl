import requests
import json
import os
import shutil

from zipfile import ZipFile
from io import BytesIO
from urllib.parse import urlparse, unquote

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


def init_path(download_path):
    if os.path.exists(download_path):
        shutil.rmtree(download_path)
        print(f'Deleted existing path: {download_path}')
    
    os.makedirs(download_path)

def download_and_extract_doc(url, download_path):
    init_path(download_path)
    response = requests.get(url)
    if response.status_code == 200:
        # Extract contents from the zip file in memory
        with ZipFile(BytesIO(response.content), 'r') as zip_ref:
            # Filter and keep only .doc and .docx files
            doc_files = [file for file in zip_ref.namelist() if file.lower().endswith(('.doc', '.docx'))]

            for doc_file in doc_files:
                file_name, file_extension = os.path.splitext(doc_file)
                ## Remove version info
                file_name = file_name[:file_name.rfind('-')] + file_extension

                doc_content = zip_ref.read(doc_file)
                doc_filepath = os.path.join(download_path, file_name)
                with open(doc_filepath, 'wb') as doc_file:
                    doc_file.write(doc_content)
                
                print(f"Extracted to: {doc_filepath}")

        print(f"{url} --> {download_path}")

    else:
        print(f"Download fail: {response.status_code}")


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
        download_and_extract_doc(url, path)
    
    with open(index_file, "w") as file:
      json.dump(url_list, file, indent=1)
    print(f"URL stored in {index_file}")
    
    
    
    
    
