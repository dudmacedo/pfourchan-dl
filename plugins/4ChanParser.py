import os
import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from plugins.ChanParserInterface import ChanParserInterface


class FourChanParser(ChanParserInterface):
    def __init__(self):
        super().__init__(["4chan", "Fourchan", "4chan.org"])
        self.url_base1 = "https://boards.4chan.org/"
        self.url_base2 = "https://boards.4chan.org"

    """Download Threads from the Board"""

    def download_board(self, board_url: str, output_dir: str, board_archive: bool):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(board_url + 'catalog')

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        divs = soup.findAll('div', {'class': 'thread'})
        for div in divs:
            a_href = div.find('a').get('href').split('#')[0]
            self.download_thread('https:' + a_href, output_dir)

        if board_archive:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(board_url + 'archive')

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            a_links = soup.findAll('a', {'class': 'quotelink'})
            for link in a_links:
                self.download_thread(self.url_base2 + link.get('href'), output_dir)

    """Download Thread from the URL"""

    def download_thread(self, thread_url: str, output_dir: str):
        res = requests.get(thread_url)
        html_page = res.text

        soup = BeautifulSoup(html_page, 'html.parser')

        # Get data for directory names
        title_data = soup.title.text.split(' - ')
        thread_title = title_data[1]
        board_name = title_data[2]

        # Creating directories
        dest_directory = "{}{}/{}".format(output_dir,
                                          self.get_valid_filename(board_name),
                                          self.get_valid_filename(thread_title))
        print("Destination:", dest_directory)
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        # Finding files
        files = soup.findAll('div', {'class': 'file'})
        for f in files:
            a = f.find('a', {'class': 'fileThumb'})
            if a is not None:
                self.download_file("http:" + a.get('href'), dest_directory)
