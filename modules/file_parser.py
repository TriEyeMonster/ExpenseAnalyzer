import openpyxl


class XlsxParser:
    def __init__(self, scr_file):
        self.scr_file = scr_file
        self.ws = None

    def load_ws(self):
        wb = openpyxl.load_workbook(self.scr_file)
        return wb.get_sheet_by_name(wb.get_sheet_names()[0])

    def parse_data(self):
        self.ws = self.load_ws()
        for row in self.ws.iter_rows():
            for cell in row:
                print cell.value



