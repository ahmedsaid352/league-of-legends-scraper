from bs4 import BeautifulSoup
import requests
import re
import os

from consts import (
    URL,
    NAME_SELECTOR,
    AUDIO_CONTAINER_SELECTOR
)

def BeautifulSoup_of(url):
    """
    Given a URL, fetches the response content and returns a BeautifulSoup object.

    Args:
        url (str): The URL to fetch the content from.

    Returns:
        A BeautifulSoup object representing the HTML content.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup

def get_valid_characters_urls(url, selector):
    """
    Given a URL and a CSS selector, fetches the HTML content of the URL and
    returns a list of valid character URLs.

    Args:
        url (str): The URL to fetch the content from.
        selector (str): The CSS selector to use to find the character names.

    Returns:
        A list of valid character URLs.
    """
    valid_urls = []
    home_soup =  BeautifulSoup_of(url)
    characters_names = home_soup.select(selector)
    for url in characters_names:
        if url.get('href').endswith('Audio'):
            valid_urls.append(url.get('href'))
    return valid_urls

def get_character_audio_data(character_url):
    """
    Given a character URL, fetches the HTML content of the URL and returns a list
    of audio data and the character name.

    Args:
        character_url (str): The URL of the character to fetch audio data for.

    Returns:
        A tuple containing the audio data as a list of tuples (src, quote) and the
        character name as a string.
    """
    audio_data = [] # [(src, quote)]
    char_name = character_url.replace('https://leagueoflegends.fandom.com/wiki/','').split('/')[0]
    char_soup = BeautifulSoup_of(character_url)
    audio_containers = char_soup.select(AUDIO_CONTAINER_SELECTOR)
    
    for container in audio_containers:
        if container.select('audio'):
            src = container.select('audio')[-1].select_one('source')['src']
            quote = container.text.split('▶️')[-1]
            audio_data.append((src, quote))
    return audio_data , char_name

def convert_to_mp3_filename(string):
    """
    Given a string, converts it to a valid filename by removing any characters
    that are not allowed in filenames and replacing spaces with underscores.

    Args:
        string (str): The string to convert.

    Returns:
        A string that is a valid filename.
    """
    # Remove any characters that are not allowed in file names
    filename = re.sub(r'[^\w\s-]', '', string)
    filename = filename.strip().replace(' ', '_').replace('\n','').replace('\t','').replace('\\','')
    
    # Limit the length of the file name
    filename = filename[:255 - 4]  # 4 is the length of ".mp3"
    
    filename = filename + ".mp3"
    
    return filename

def download_char_audio(audio_data, char_name):
    """
    Given a list of audio data and a character name, downloads each audio file
    and saves it to a file with a valid filename in a folder named after the
    character.

    Args:
        audio_data (list): A list of tuples (src, quote) representing the audio data.
        char_name (str): The name of the character.
    """
    for audio in audio_data:
        src = audio[0]
        quote = audio[1]
        file_name = convert_to_mp3_filename(quote)
        response  = requests.get(src)
        # check if the character name folder exist
        print(os.path.join(char_name, file_name))
        if not os.path.exists(char_name):
            os.makedirs(char_name)
        try:
            with open(os.path.join(char_name, file_name), 'wb') as f:
                f.write(response.content)
        except:
            print(f'Failed to Download {char_name} / {file_name}\n')

def main():
    """
    The main function that runs the program.
    """
    characters_urls = get_valid_characters_urls(URL, NAME_SELECTOR)
    for char_url in characters_urls:
        audio_data , char_name = get_character_audio_data(char_url)
        download_char_audio(audio_data[:3], char_name)

if __name__ == '__main__':
    main()