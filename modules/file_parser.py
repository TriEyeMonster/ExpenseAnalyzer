import openpyxl

class XlsxParser:
    def __init__(self, scr_file):
        self.scr_file = scr_file
        self.ws = None
        self.records = []

    def load_ws(self):
        wb = openpyxl.load_workbook(self.scr_file)
        return wb.get_sheet_by_name(wb.get_sheet_names()[0])

    def parse_data(self):
        self.ws = self.load_ws()
        for row_index, row in enumerate(self.ws.iter_rows(min_row=10)):
            if row_index == 0:
                header = [str(x.value) for x in row]
                continue
            self.records.append(zip(header, map(lambda x: '' if x is None else str(x), [x.value for x in row] )))
        return self.records







