from modules.analyzer import Analyzer

if __name__ == "__main__":
    source = r"C:\1.PyProject\ExpenseAnalyzer\Data\CC_TXN_History_01012018215522.xlsx"
    analyzer = Analyzer(source)
    analyzer.analyse()
