import pandas as pd
import numpy as np
from modules.analyzer import Analyzer


if __name__ == "__main__":

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
    df_total = pd.DataFrame(df.groupby('Category').agg({'Amount': np.sum, 'Category': np.size}))
    df = pd.merge(left=df, right=df_total,
                  how='left', left_on='Category', right_index=True)

    # df = df.set_index(['Date', 'Category'])
    # print(df.groupby(['Category']).sum())
    # print(df.groupby('Category').sum().sort_values('Amount', ascending=False))
    # print(df.groupby('Date').sum())
    df = df.pivot_table(index=['Category_x', 'Amount_y', 'Category_y', 'Shop'], aggfunc=np.sum)
    print(df.sort_values(['Amount_y', 'Amount_x'], ascending=False))


