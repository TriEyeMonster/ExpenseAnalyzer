import os
from file_parser import XlsxParser


class Analyzer:
    def __init__(self, scr_file):
        if not os.path.exists(scr_file):
            print "{0} does not exists".format(scr_file)
            exit
        self.scr_parser = XlsxParser(scr_file)

    def analyse(self):
        self.scr_parser.parse_data()