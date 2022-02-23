# Python 4chan Downloader
import argparse

from straight.plugin import load
from plugins.ChanParserInterface import ChanParserInterface


def main():
    # Parsing arguments
    parser = argparse.ArgumentParser(description="Download files from 4chan and other imageboards")
    parser.add_argument('--min-space', type=int, default=1, help="Minimum empty space in disk to download, in GB")
    parser.add_argument('-i', '--imageboard', type=str, default="4chan", help="Imageboard to download from")
    parser.add_argument('-t', '--thread', type=str)
    parser.add_argument('-b', '--board', type=str)
    parser.add_argument('-o', '--output', type=str, default="./")
    parser.add_argument('-a', '--board_archive', dest='board_archive', action='store_true', default=False,
                        help="Define if must download the board archive too")
    parser.add_argument('-p', '--save_page', dest='save_page', action='store_true', default=False,
                        help="Define if the html page of the thread will be saved too")

    args = parser.parse_args()

    plugins = load("plugins", subclasses=ChanParserInterface)
    for parser in plugins:
        try:
            print(parser.its_me("4chan"))
        except:
            pass


if __name__ == '__main__':
    main()
