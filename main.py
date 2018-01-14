from modules.analyzer import Analyzer

if __name__ == "__main__":
    source = r"/Users/wguan17/PycharmProjects/ExpenseAnalyzer/Data/CC_TXN_History_14012018115154.xlsx"
    analyzer = Analyzer(source)
    analyzer.analyse()