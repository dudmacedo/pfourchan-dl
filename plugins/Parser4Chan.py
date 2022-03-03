import requests

from bs4 import BeautifulSoup
from selenium import webdriver
from plugins.ChanParserInterface import ChanParserInterface


class Parser4Chan(ChanParserInterface):
    def __init__(self):
        super().__init__(["4chan", "Fourchan", "4chan.org"])
        self.url_base1 = "https://boards.4chan.org/"
        self.url_base2 = "https://boards.4chan.org"

    """Parse Threads from the Board"""

    def parse_board(self, board_url: str, board_archive: bool):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        driver = webdriver.Chrome(options=options)
        driver.get(board_url + 'catalog')

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        threads = []
        divs = soup.findAll('div', {'class': 'thread'})
        for div in divs:
            a_href = div.find('a').get('href').split('#')[0]
            threads.append('https:' + a_href)

        if board_archive:
            options = webdriver.ChromeOptions()
            options.add_argument('--headless')
            driver = webdriver.Chrome(options=options)
            driver.get(board_url + 'archive')

            soup = BeautifulSoup(driver.page_source, 'html.parser')

            a_links = soup.findAll('a', {'class': 'quotelink'})
            for link in a_links:
                threads.append(self.url_base2 + link.get('href'))

        return threads

    """Parse Thread from the URL"""

    def parse_thread(self, thread_url: str):
        res = requests.get(thread_url)
        html_page = res.text

        soup = BeautifulSoup(html_page, 'html.parser')

        # Get data for directory names
        title_data = soup.title.text.split(' - ')
        thread_title = title_data[1]
        board_name = title_data[2]

        # Finding files
        links = []
        files = soup.findAll('div', {'class': 'file'})
        for f in files:
            a = f.find('a', {'class': 'fileThumb'})
            if a is not None:
                links.append("http:" + a.get('href'))

        return board_name, thread_title, links
