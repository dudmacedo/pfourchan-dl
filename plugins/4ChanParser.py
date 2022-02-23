from plugins.ChanParserInterface import ChanParserInterface


class FourChanParser(ChanParserInterface):
    def __init__(self):
        self.parser_ids = ["4chan", "Fourchan", "4chan.org"]

    """Download Threads from the Board"""
    def download_board(self, board_url: str, output_dir: str, board_archive: bool):
        pass

    """Download Thread from the URL"""
    def download_thread(self, thread_url: str, output_dir: str):
        pass
