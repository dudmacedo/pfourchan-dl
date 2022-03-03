import os
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from plugins.ChanParserInterface import ChanParserInterface


class Parser1500Chan(ChanParserInterface):
    def __init__(self):
        super().__init__(["1500chan", "1500chan.org"])
        self.url_base1 = "https://1500chan.org/"
        self.url_base2 = "https://1500chan.org"

    """Parse Threads from the Board"""

    def parse_board(self, board_url: str, board_archive: bool):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(board_url + 'catalog.html')

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        threads = []
        divs = soup.findAll('div', {'class': 'thread'})
        for div in divs:
            a_href = div.find('a').get('href')
            threads.append(self.url_base2 + a_href)

        return threads

    """Parse Thread from the URL"""

    def parse_thread(self, thread_url: str):
        res = requests.get(thread_url)
        html_page = res.text

        soup = BeautifulSoup(html_page, 'html.parser')

        # Get data for directory names
        thread_title = soup.title.text.split(' - ')[1]
        board_name = soup.find('h1').text.split(' - ')[1]

        # Finding files
        links = []
        files = soup.findAll('p', {'class': 'fileinfo'})
        for f in files:
            a = f.find('a')
            if a is not None:
                links.append(self.url_base2 + a.get('href'))

        return board_name, thread_title, links
