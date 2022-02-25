import os
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from plugins.ChanParserInterface import ChanParserInterface


class BrChanParser(ChanParserInterface):
    def __init__(self):
        super().__init__(["1500chan", "1500chan.org"])
        self.url_base1 = "https://1500chan.org/"
        self.url_base2 = "https://1500chan.org"

    """Download Threads from the Board"""

    def download_board(self, board_url: str, output_dir: str, board_archive: bool):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(board_url + 'catalog.html')

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        divs = soup.findAll('div', {'class': 'thread'})
        for div in divs:
            a_href = div.find('a').get('href')
            self.download_thread(self.url_base2 + a_href, output_dir)

    """Download Thread from the URL"""

    def download_thread(self, thread_url: str, output_dir: str):
        res = requests.get(thread_url)
        html_page = res.text

        soup = BeautifulSoup(html_page, 'html.parser')

        # Get data for directory names
        thread_title = soup.title.text.split(' - ')[1]
        board_name = soup.find('h1').text.split(' - ')[1]

        # Creating directories
        dest_directory = "{}{}/{}".format(output_dir,
                                          self.get_valid_filename(board_name),
                                          self.get_valid_filename(thread_title))
        print("Destination:", dest_directory)
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        # Finding files
        files = soup.findAll('p', {'class': 'fileinfo'})
        for f in files:
            a = f.find('a')
            if a is not None:
                self.download_file(self.url_base2 + a.get('href'), dest_directory)
