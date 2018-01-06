import os
from file_parser import XlsxParser


class Analyzer:
    def __init__(self, scr_file):
        if not os.path.exists(scr_file):
            print "{0} does not exists".format(scr_file)
            exit
        self.scr_parser = XlsxParser(scr_file)
        self.parsed_records = []
        self.shop_dict = {}

    def analyse_recrods(self):
        for record in self.parsed_records:
            shop_name = ""
            single_spend = 0
            shop_spent_init = {"spent": 0, "times": 0}
            for header, infor in record:
                if header == "Description":
                    shop_name = infor.split('\n')[0]
                elif header == "Transaction Amount(Local)":
                    single_spend = float(infor) if infor[-1] != "L" else float("".join(infor[:-1]))
            shop_spent_infor = self.shop_dict.setdefault(shop_name, shop_spent_init)
            shop_spent_infor["spent"] += single_spend
            shop_spent_infor["times"] += 1

    def print_result(self):
        self.print_list = []
        for key, value in self.shop_dict.iteritems():
            amount = 0
            times = 0
            for spent_key, spent_value in value.iteritems():
                if spent_key == 'spent':
                    amount = spent_value
                elif spent_key == 'times':
                    times = spent_value
            self.print_list.append((key, amount, times))
        self.print_list.sort(key = lambda x: x[1], reverse=True)
        for key, amount, times in self.print_list:
            print "Shop Name:{0}\tSpent Total Amount: {1:6.2f}\tTimes: {2}".format(key, amount, times)

    def analyse(self):
        self.parsed_records = self.scr_parser.parse_data()
        self.analyse_recrods()
        self.print_result()


