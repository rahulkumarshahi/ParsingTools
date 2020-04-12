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
--> Note may need to remove the last autocalculated output, and the top 3 rows.
---> Will look at that later.
"""

import csv
import os
import pandas as pd
from collections import OrderedDict

PATH='/Users/rahul/Desktop/D/quickWork/'
FILE_NAME = '8500598372_FnOPnL.csv'
filePath = PATH + FILE_NAME
months = ['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
MON_YRS = [ (m+'-19').lower() for m in months] + [(m + '-20').lower() for m in months]

def make_df(filePath=None, skiprows=None):
    """
    :param filePath: str
    :param skiprows: int or list [1,3,5] : research further
    :return: dataframe
    """
    return pd.read_csv(filePath, skiprows=skiprows)

def get_mon_yr_pairs(df=None, col_name='Trade Date', pick_from=6 ):
    """
    :desc: from the trade dates, compose a set of Month-year pairs to
            clculate monthly PnL.
    :param df: from the input file
    :param col_name: the only pertinent colum
    :param pick_from:
    :return:
    """
    return set(df[col_name].apply(lambda x : x[ -pick_from : ]))

def pick_rows(mon_yr, col='Trade Date', df=None):
    """
    :desc: From dataframe, get the pertinent rows based on month-year combo
    :param mon_yr: part of set of month-year pairs e.g.: 'Jul-19'
    :param col: str
    :param df: dataframe
    :return: dataframe
    """
    return df[col].apply(lambda x : mon_yr.lower() in x.lower()).to_frame()

def get_amts_table(df, col_date='Trade Date', col_amt = 'Amount'):
    """
    :desc: From the read file, it gets the cumulative sum for month-year
    :param df: dataframe
    :param col_date: str
    :param col_amt: str
    :return: ordered_dict (sorted by month an OrderedDictionary of monthly PnL)
    """
    d = OrderedDict()
    for m in get_mon_yr_pairs(df=df):
        df_tru_rows = pick_rows(m, df=df)
        df_tru_table = df.loc[(df_tru_rows[col_date] == True) & (df[col_amt]) ]
        df_amt = df_tru_table[col_amt]
        d[m] = sum(df_amt)
    return sorted(d.items(), key = lambda x: MON_YRS.index(x[0].lower()) )


def main():
    from pprint import pprint
    df = make_df(filePath, skiprows=None)
    pprint(get_amts_table(df))

main()
