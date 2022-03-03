from typing import final


class ChanParserInterface:
    def __init__(self, parser_ids):
        self.parser_ids = parser_ids

    """Returns if this is the pretended parser of the passed id"""
    @final
    def its_me(self, parser_id: str):
        if parser_id in self.parser_ids:
            return True
        else:
            return False

    """Parse Threads from the Board"""
    def parse_board(self, board_url: str, board_archive: bool):
        pass

    """Parse Thread from the URL"""
    def parse_thread(self, thread_url: str):
        pass
