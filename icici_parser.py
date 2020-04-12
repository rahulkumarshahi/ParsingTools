""""
Desc: ICICI FNO trades are in data set of the form of :
------------------------------------------------
Trade Date	Exchange	Credit/Debit	Amount
------------------------------------------------
31-Mar-20	NFO	DR	-1224.06
30-Mar-20	NFO	CR	24438.82
27-Mar-20	NFO	CR	16182.31
    :         :  :      :
-------------------------------------------------
To get data from ICICI and find the monthly PnL output

"""

import csv
import os
import pandas as pd
from collections import OrderedDict

PATH='/Users/rahul/Desktop/D/quickWork/'
FILE_NAME = 'fno_2019.csv'
filePath = PATH + FILE_NAME
months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
MON_YRS = [ (m+'-19').lower() for m in months] + [(m + '-20').lower() for m in months]

def make_df(filePath=None):
    return pd.read_csv(filePath)

def get_mon_yr_pairs(df=None, col_name='Trade Date', pick_from=6 ):
    return set(df[col_name].apply(lambda x : x[ -pick_from : ]))

def pick_rows(mon_yr, col='Trade Date', df=None):
    return df[col].apply(lambda x : mon_yr.lower() in x.lower()).to_frame()

def get_amts_table(df, col_date='Trade Date', col_amt = 'Amount'):
    d = OrderedDict()
    for m in get_mon_yr_pairs(df=df):
        df_tru_rows = pick_rows(m, df=df)
        df_tru_table = df.loc[(df_tru_rows[col_date] == True) & (df[col_amt]) ]
        df_amt = df_tru_table[col_amt]
        d[m] = sum(df_amt)
    return sorted(d.items(), key = lambda x: MON_YRS.index(x[0].lower()) )


def main():
    from pprint import pprint
    df = make_df(filePath)
    pprint(get_amts_table(df))

main()
