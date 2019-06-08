import pandas as pd


# from modules.analyzer import Analyzer


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

        def splitListToRows(row, row_accumulator, target_column, separator):
            split_row = row[target_column].split(separator)
            for s in split_row:
                new_row = row.to_dict()
                new_row[target_column] = s
                row_accumulator.append(new_row)

        new_rows = []
        df.apply(splitListToRows, axis=1, args=(new_rows, target_column, separator))
        new_df = pd.DataFrame(new_rows)
        return new_df

    src_file = r"Data/May.xls"
    df = pd.read_excel(src_file, skiprows=range(1, 9), header=1)
    df = df[~df.Description.isin(['GIRO PAYMENT                            ', 'Previous Balance'])]
    df[['shop', 'ref_no']] = df.Description.str.split('Ref No:', 1, expand=True)
    df.drop(columns=['Local Currency Type','Transaction Amount(Foreign)','Foreign Currency Type','Description', 'Posting Date'], inplace=True)
    df.shop = df.shop.str[:25]
    df.shop = df.shop.str.strip()
    df

