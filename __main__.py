# Python 4chan Downloader
import argparse

from straight.plugin import load
from plugins.ChanParserInterface import ChanParserInterface


def main():
    # Parsing arguments
    argparser = argparse.ArgumentParser(description="Download files from 4chan and other imageboards")
    argparser.add_argument('--min-space', type=int, default=1, help="Minimum empty space in disk to download, in GB")
    argparser.add_argument('-i', '--imageboard', type=str, default="4chan", help="Imageboard to download from")
    argparser.add_argument('-t', '--thread', type=str)
    argparser.add_argument('-b', '--board', type=str)
    argparser.add_argument('-o', '--output', type=str, default="./")
    argparser.add_argument('-a', '--board_archive', dest='board_archive', action='store_true', default=False,
                           help="Define if must download the board archive too")
    argparser.add_argument('-p', '--save_page', dest='save_page', action='store_true', default=False,
                           help="Define if the html page of the thread will be saved too")

    args = argparser.parse_args()

    plugin_instances = load("plugins", subclasses=ChanParserInterface).produce()
    parser = None
    for plugin in plugin_instances:
        if plugin.its_me(args.imageboard):
            parser = plugin

    if parser is None:
        print(args.imageboard, "imageboard support not implemented yet!")
        quit()
    else:
        print(parser.__class__.__name__, "selected")
        if args.thread is not None:
            parser.download_thread(args.thread, args.output)
        elif args.board is not None:
            parser.download_board(args.board, args.output, board_archive=args.board_archive)

    print("OK! Files downloaded.")


if __name__ == '__main__':
    main()
