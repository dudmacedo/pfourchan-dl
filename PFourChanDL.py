# Python 4chan Downloader
import argparse
import os
import re
import time

import wget

from straight.plugin import load
from plugins.ChanParserInterface import ChanParserInterface
from datetime import datetime


class PFourChanDL(object):
    def __init__(self):
        self.params = None

    def main(self):
        # Parsing arguments
        argparser = argparse.ArgumentParser(description="Download files from 4chan and other imageboards")
        argparser.add_argument('--min_space', type=int, default=1,
                               help="Minimum empty space in disk to download, in GB")
        argparser.add_argument('-i', '--imageboard', type=str, default="4chan", help="Imageboard to download from")
        argparser.add_argument('-t', '--thread', type=str)
        argparser.add_argument('-b', '--board', type=str)
        argparser.add_argument('-o', '--output', type=str, default="./")
        argparser.add_argument('-a', '--board_archive', dest='board_archive', action='store_true', default=False,
                               help="Define if must download the board archive too")
        argparser.add_argument('-p', '--save_page', dest='save_page', action='store_true', default=False,
                               help="Define if the html page of the thread will be saved too")

        self.params = argparser.parse_args()

        plugin_instances = load("plugins", subclasses=ChanParserInterface).produce()
        parser = None
        for plugin in plugin_instances:
            if plugin.its_me(self.params.imageboard):
                parser = plugin

        if parser is None:
            print(self.params.imageboard, "imageboard support not implemented yet!")
            quit()
        else:
            print(parser.__class__.__name__, "selected")

            if self.params.thread is not None:
                board_name, thread_title, links = parser.parse_thread(self.params.thread)
                self.download_thread_files(board_name, thread_title, links)

            elif self.params.board is not None:
                threads = parser.parse_board(self.params.board, self.params.board_archive)
                count = 0
                total = len(threads)
                for thread in threads:
                    count = count + 1
                    print("({}/{}) - Download {}".format(count, total, thread))
                    board_name, thread_title, links = parser.parse_thread(thread)
                    self.download_thread_files(board_name, thread_title, links)

        print("OK! Files downloaded.")

    def download_thread_files(self, board_name, thread_title, links):
        dest_directory = "{}{}/{}".format(self.params.output,
                                          self.get_valid_filename(board_name),
                                          self.get_valid_filename(thread_title))
        print("Destination:", dest_directory)
        if not os.path.exists(dest_directory):
            os.makedirs(dest_directory)

        count = 0
        total = len(links)
        for link in links:
            count = count + 1
            print("({}/{})".format(count, total))
            self.download_file(link, dest_directory)
            time.sleep(0.05)

    @staticmethod
    def download_file(url, dest_directory):
        dest_filename = "{}/{}".format(dest_directory, wget.filename_from_url(url))
        if os.path.exists(dest_filename):
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "- Already downloaded file ", dest_filename)
            return
        print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "- Downloading file ", dest_filename)
        try:
            wget.download(url, dest_filename)
            print()
        except:
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S"), "- Error downloading file ", dest_filename)

    """Make filename Windows-safe"""

    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '-', s)
