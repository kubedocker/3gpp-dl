import requests
import json
import os
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

    print("Find updated index:")
    new_index = [item for item in url_list if item not in old_index and print(item)]
    print("---finish---")
    

    '''
    with open(index_file, "w") as file:
      json.dump(url_list, file, indent=1)
    print(f"URL stored in {index_file}")
    '''
    
    
    
    
