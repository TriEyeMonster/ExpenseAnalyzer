import pandas as pd
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
    print(df.groupby(['Category', 'Shop']).sum())
    print(df.groupby('Category').sum().sort_values('Amount', ascending=False))
    print(df.groupby('Date').sum())


