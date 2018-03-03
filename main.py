from modules.analyzer import Analyzer

if __name__ == "__main__":
    source = r"/Users/wguan17/PycharmProjects/ExpenseAnalyzer/Data/Mar_Expense.xlsx"
    analyzer = Analyzer(source)
    analyzer.analyse()
