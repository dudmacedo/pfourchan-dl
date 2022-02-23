import os
import re
import wget

from datetime import datetime


class ChanParserInterface:
    """Download Threads from the Board"""
    def download_board(self, board_url: str, output_dir: str, board_archive: bool):
        pass

    """Download Thread from the URL"""
    def download_thread(self, thread_url: str, output_dir: str):
        pass

    """Download the file from url to dest_directory"""
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

    """Convert filename to a Windows-safe one"""
    @staticmethod
    def get_valid_filename(s):
        s = str(s).strip().replace(' ', '_')
        return re.sub(r'(?u)[^-\w.]', '-', s)