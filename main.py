import shutil


def rename_files():
    ofn = lambda a : f"org_indexcomponents/indexcomponents ({a}).csv"
    nfn = lambda s : f"components/indexcomponents_{s[2]}_{s[1]}_{s[0]}.csv"
    for i in range(71):
        old_name = ofn(i)
        with open(old_name, 'r') as f:
            f.readline()
            s = f.readline().strip()
            s = s.split(' ')[-1]
            s = s.split('/')
        new_name = nfn(s)
        print("Copied", old_name, "as", new_name)
        shutil.copy(old_name, new_name)
            





if __name__ == "__main__":
    rename_files()
    