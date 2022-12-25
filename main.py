import shutil
import csv
import pandas as pd
import os
from datetime import date
import sys

def get_date(file_name):
    with open(file_name, 'r') as f:
        f.readline()
        s = f.readline().strip()
        s = s.split(' ')[-1]
        s = s.split('/')
        s = [int(x) for x in s]
        return s



def copy_files_to_components():
    def nfn(s): return f"components/indexcomponents_{s[2]}_{s[1]}_{s[0]}.csv"
    org_folder = "active_folder"
    for f in os.listdir(org_folder):
        old_name = os.path.join(org_folder, f)
        s = get_date(old_name)
        new_name = nfn(s)
        if not os.path.isfile(new_name):
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


def diff_symbols(output_file = sys.stdout):
    symbols_dir = get_date_symbols()
    soted_keys = sorted(symbols_dir)
    to_iterate = zip(soted_keys[:-1], soted_keys[1:])
    ins_counter = 0
    outs_counter = 0
    for before, after in to_iterate:
        print('from', before, 'to', after, end=', ', file=output_file)
        out_stocks = get_out_stocks(symbols_dir[before], symbols_dir[after])
        in_stocks = get_in_stocks(symbols_dir[before], symbols_dir[after])
        if len(out_stocks) == 0 and len(in_stocks) == 0:
            print("no change.", end='',  file=output_file)
        if len(out_stocks):
            outs_counter+=len(out_stocks)
            print('Out stocks: ', out_stocks, end=', ',  file=output_file)
        if len(in_stocks):
            ins_counter+=len(in_stocks)
            print('In stocks:', in_stocks, end='',  file=output_file)
        print(  file=output_file)
    print(f"no. of ins changes  = {ins_counter}", file=output_file)
    print(f"no. of outs changes = {outs_counter}", file=output_file)
    print(f"no. total changes   = {ins_counter + outs_counter}", file=output_file)
        


if __name__ == "__main__":
    copy_files_to_components()
    output_file = 'output.txt'
    with open(output_file, 'w') as f:
        diff_symbols(f)
