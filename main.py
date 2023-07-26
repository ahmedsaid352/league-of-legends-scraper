from bs4 import BeautifulSoup
import requests

from consts import (
    URL,
    NAME_SELECTOR,
    AUDIO_CONTAINER_SELECTOR
)

def BeautifulSoup_of(url):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

def get_valid_characters_urls(url, selector):
    valid_urls = []
    home_soup =  BeautifulSoup_of(url)
    characters_names = home_soup.select(selector)
    for url in characters_names:
        if url.get('href').endswith('Audio'):
            valid_urls.append(url.get('href'))
    return valid_urls





def main():
    home_soup = BeautifulSoup_of(URL)
    characters_names = home_soup.select(NAME_SELECTOR)

if __name__ == '__main__':
    main()