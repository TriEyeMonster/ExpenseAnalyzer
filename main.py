import pandas as pd
from modules.analyzer import Analyzer


if __name__ == "__main__":
    # source = r"/Users/wguan17/PycharmProjects/ExpenseAnalyzer/Data/Apr_Expense.xlsx"
    # analyzer = Analyzer(source)
    # analyzer.analyse()

    def splitDataFrameList(df, target_column, separator):
        ''' df = dataframe to split,
        target_column = the column containing the values to split
        separator = the symbol used to perform the split
        returns: a dataframe with each entry for the target column separated, with each element moved into a new row.
        The values in the other columns are duplicated across the newly divided rows.
        '''

    src_file = r"Data/May.xls"
    df = pd.read_excel(src_file, skiprows=range(1, 9), header=1)
    df = df[~df.Description.isin(['GIRO PAYMENT                            ', 'Previous Balance'])]
    df[['shop', 'ref_no']] = df.Description.str.split('Ref No:', 1, expand=True)
    df.drop(columns=['Local Currency Type','Transaction Amount(Foreign)','Foreign Currency Type','Description', 'Posting Date', 'ref_no'], inplace=True)
    df.shop = df.shop.str[:25]
    df.shop = df.shop.str.split(r'[*@-]', expand=True)
    df.shop = df.shop.str.split(r'\(', expand=True)
    df.shop = df.shop.str.strip()
    df.columns = ['Date', 'Amount', 'Shop']
    analyzer = Analyzer()
    df['Category'] = pd.Series(df['Shop'].apply(analyzer.get_category), index=df.index)
    df['Date'] = pd.to_datetime(df['Date'])
    df
    agg_amt = df.groupby('Date').sum().plot()
    agg_amt


