import shutil
import csv
import pandas as pd
import os
from datetime import date


def get_date(file_name):
    with open(file_name, 'r') as f:
        f.readline()
        s = f.readline().strip()
        s = s.split(' ')[-1]
        s = s.split('/')
        s = [int(x) for x in s]
        return s


def rename_files():
    def ofn(a): return f"org_indexcomponents/indexcomponents ({a}).csv"
    def nfn(s): return f"components/indexcomponents_{s[2]}_{s[1]}_{s[0]}.csv"
    for i in range(71):
        old_name = ofn(i)
        s = get_date(old_name)
        new_name = nfn(s)
        print("Copied", old_name, "as", new_name)
        shutil.copy(old_name, new_name)


def get_symbols(file_name):
    df = pd.read_csv(file_name, index_col=1, header=2)
    return list(df.index)


def get_date_symbols():
    symbols_dir = {}
    for f in os.listdir('components'):
        file_name = os.path.join("components", f)
        s = date(*reversed(get_date(file_name)))
        # s = '/'.join(reversed(get_date(file_name)))
        symbols = get_symbols(file_name)
        symbols_dir[s] = symbols
    return symbols_dir


def get_out_stocks(before, after):
    return list(set(before) - set(after))


def get_in_stocks(before, after):
    return list(set(after) - set(before))


def diff_symbols():
    symbols_dir = get_date_symbols()
    soted_keys = sorted(symbols_dir)
    to_iterate = zip(soted_keys[:-1], soted_keys[1:])
    for before, after in to_iterate:
        print('from', before, 'to', after, end=', ')
        out_stocks = get_out_stocks(symbols_dir[before], symbols_dir[after])
        in_stocks = get_in_stocks(symbols_dir[before], symbols_dir[after])
        if len(out_stocks) == 0 and len(in_stocks) == 0:
            print("no change.", end='')
        if len(out_stocks):
            print('Out stocks: ', out_stocks, end=', ')
        if len(in_stocks):
            print('In stocks:', in_stocks, end='')
        print()


if __name__ == "__main__":
    diff_symbols()
