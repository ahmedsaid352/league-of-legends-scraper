# league-of-legends-scraper
python script downloads League of Legends characters' voices.

This is a Python script that can be used to scrape audio data for League of Legends characters. The script uses the BeautifulSoup library to parse HTML content and extract relevant data.

## Requirements

To use this script, you will need to have Python 3 installed on your system. You will also need to install the following Python libraries:

- BeautifulSoup
- requests

You can install these libraries using pip:

```
pip install -r requirements.txt
```


## Usage

To use this script, you will need to modify the following constants in the `consts.py` file:

- `URL`: The URL of the League of Legends characters page to scrape.


Once you have set these constants, you can run the script using the following command:

```
python main.py
```

The script will fetch the HTML content of the character page, extract the relevant data, and download the audio files to your local system.

