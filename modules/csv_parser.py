import os
import pandas as pd

class Csv_Parser:
    def __init__(self, *csvs):
        self.csv_list = csvs

    def csv_combine(self):
        with open('output.csv', 'w') as dst:
            for csv in self.csv_list:
                acc_name = ""
                credit_col = None
                debit_col = None
                with open(csv, 'r') as scr:
                    for line in scr:
                        line = line.strip()
                        if 'Account Details'.lower() in line.lower():
                            acc_name = line[line.index(",")+1 : line.rindex('Account')]
                        elif 'Transaction Date'.lower() in line.lower():
                            col_list = line.split(",")
                            for col_num, col_name in enumerate(col_list):
                                if 'credit' in col_name.lower() or 'deposit' in col_name.lower():
                                    credit_col = col_num
                                elif 'debit' in col_name.lower() or 'withdraw' in col_name.lower():
                                    debit_col = col_num
                        elif credit_col and debit_col:
                            amount = None
                            if '"' in line:
                                nums = "".join(line[line.index('"')+1:line.rindex('"')])
                                nums = nums.replace(",", "")
                                line = line[:line.index('"')] + nums + line[line.rindex('"')+1:]
                            line_content = line.split(",")
                            if len(line_content) < max(credit_col, debit_col):
                                continue
                            if line_content[credit_col]:
                                amount = line_content[credit_col]
                            elif line_content[debit_col]:
                                amount = "-" + line_content[debit_col]
                            new_line = ",".join([acc_name, line_content[0], amount])
                            print new_line
                            dst.write(new_line+"\n")

    def csv_refactor(self):
        df = pd.read_csv('/Users/wguan17/Downloads/OCBC_Mar.csv', names=['systemtime', 'Var1', 'Description', 'Depit', 'Credit'], sep=',',
                         infer_datetime_format=True)  # or:, infer_datetime_format=True)
        fileDATES = df.T.to_dict().values()  # export the data frame to a python dictionary
        return fileDATES



if __name__ == "__main__":
    csv_list = [os.path.join(r"/Users/wguan17/Downloads", x) for x in os.listdir(r"/Users/wguan17/Downloads")
                if os.path.isfile(os.path.join(r"/Users/wguan17/Downloads", x)) and os.path.splitext(x)[1] == '.csv']
    cp = Csv_Parser(*csv_list)
    cp.csv_combine()
    print cp.csv_refactor()