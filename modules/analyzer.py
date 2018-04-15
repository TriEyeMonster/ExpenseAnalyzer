import os
import json
from file_parser import XlsxParser
from internet_handler import GoogleHandler
import time

CATEGORY = r'/Users/wguan17/PycharmProjects/ExpenseAnalyzer/Data/category.txt'


class Analyzer:
    def __init__(self, scr_file):
        if not os.path.exists(scr_file):
            print "{0} does not exists".format(scr_file)
            exit
        self.scr_parser = XlsxParser(scr_file)
        self.parsed_records = []
        self.spent_by_shop_dict = {}
        self.spent_by_category_dict = {}
        self.category_dict = json.load(open(CATEGORY))
        self.google_hander = GoogleHandler()

    def get_category(self, shop_name):
        if self.category_dict.get(shop_name, False):
            return self.category_dict.get(shop_name)
        category = self.google_hander.search_page(shop_name)
        self.category_dict[shop_name] = category if category is not None else 'Others'
        print 'Category of %s get from Google is %s' % (shop_name, category)
        json.dump(self.category_dict, open(CATEGORY, 'w'), indent=4)
        print 'sleep 20 secs'
        time.sleep(20)
        return category


    def build_category_spent_dict(self, shop_name, single_spent):
        category = self.get_category(shop_name)
        self.spent_by_category_dict[category] = self.spent_by_category_dict.get(category, 0.) + single_spent


    def get_shopname(self, raw_name):
        if "*" in raw_name:
            return raw_name.split("*")[0]
        elif "@" in raw_name:
            return raw_name.split("@")[0]
        elif "-" in raw_name:
            return raw_name.split("-")[0]
        elif " " in raw_name:
            return raw_name.split(" ")[0]
        else:
            return raw_name

    def analyse_recrods(self):
        for record in self.parsed_records:
            shop_name = ""
            single_spend = 0
            shop_spent_init = {"spent": 0, "times": 0}
            for header, infor in record:
                if header == "Description":
                    shop_name = infor.split('\n')[0][:-15]
                    #shop_name = self.get_shopname(shop_name)
                elif header == "Transaction Amount(Local)":
                    single_spend = float(infor) if infor[-1] != "L" else float("".join(infor[:-1]))
            if single_spend < 0 or shop_name == "P":
                continue
            shop_spent_infor = self.spent_by_shop_dict.setdefault(shop_name, shop_spent_init)
            shop_spent_infor["spent"] += single_spend
            shop_spent_infor["times"] += 1
            self.build_category_spent_dict(shop_name, single_spend)

    def print_result_by_shop(self):
        for key, value in self.spent_by_shop_dict.iteritems():
            amount = 0
            times = 0
            for spent_key, spent_value in value.iteritems():
                if spent_key == 'spent':
                    amount = spent_value
                elif spent_key == 'times':
                    times = spent_value
            self.print_list.append((key, amount, times))
        self.print_list.sort(key = lambda x: x[1], reverse=True)
        print "%25s|%10s|%5s|\n%42s" %('Shop Name', 'Spent', 'Times', '-'*42)
        for key, amount, times in self.print_list:
            print "%25s|%10.2f|%5s|" % (key, amount, times)

    def print_result_by_category(self):
        self.print_list = []
        total = sum(self.spent_by_category_dict.values())
        sorted_spent = self.spent_by_category_dict.values()
        sorted_spent.sort(reverse = True)
        print "%15s|%10s|%11s|\n%s" % ('Category', 'Spent', 'Percentage', '-'*39)
        for spent in sorted_spent:
            for category, s_spent in self.spent_by_category_dict.iteritems():
                if s_spent == spent:
                    print "%15s|%10.2f|%10.2f%%|" %(category, spent, float(spent/total)*100)
        print "%s\n%15s|%10.2f|%10s%%|" % ('-'*39, 'Total', total, 100)
        print '\n\n'

    def print_result(self):
        self.print_result_by_category()
        self.print_result_by_shop()

    def analyse(self):
        self.parsed_records = self.scr_parser.parse_data()
        self.analyse_recrods()
        self.print_result()


