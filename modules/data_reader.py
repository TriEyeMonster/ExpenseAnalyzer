import os

class ExcelReader:
    def __init__(self, *files):
        for file in files:
            if not os.path.exists(file):
                pass