import requests
import json
from bs4 import BeautifulSoup

def get_all_links(url, filter):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        links = [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith(url)]
        if filter:
            return [link[len(url):] for link in links]
        else:
            return links
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")
        return []


def generate_json(start_url, series_list):
    directory = {}
    for release, links in series_list.items():
        for index, link in enumerate(links):
            dir_path = start_url + release + '/' + link + '/'
            dir_list = get_all_links(dir_path, False)
            
            if dir_list == []:
                break

            if release not in directory:
                directory[release] = {}

            directory[release].update({link: dir_list})
    
    return json.dumps(directory, indent=2)

def custom_sort(item):
    return int(item.split('-')[1])


def generate_file(file_path, json):
    with open(file_path, 'w') as file:
        file.write(json)


if __name__ == '__main__':
    start_url = 'https://www.3gpp.org/ftp/Specs/latest/'
    release_list = sorted(get_all_links(start_url, True), key=custom_sort)
    print(release_list)
    series_list = {release: get_all_links(start_url + release + '/', True)[:3] for release in release_list[:3]}
    json = generate_json(start_url, series_list)
    generate_file("dl.json", json)
