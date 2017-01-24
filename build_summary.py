#!/usr/bin/env python
import sys
from pathlib import Path
import pandas as pd


def fix_columns(df):
    sample_name = df.columns[0]
    replacement = {sample_name: "SAMPLE",
                   "COVRATIO": "FA",
                   sample_name+".AD": "AD",
                   sample_name+".DP": "DP",
                   sample_name+".FA": "FA"}
    return df.rename(columns=replacement)


def load_all_tables(directory, metadata=None):
    """ Loads all tables in a directory """
    table_list = []
    p = Path(directory)
    for table_file in p.glob('*table.done'):
        print(table_file)
        tmp = pd.read_table(table_file.as_posix(), delim_whitespace=True)

        if tmp.empty:
            continue
        tmp = fix_columns(tmp)

        if metadata is not None:
            print(table_file.as_posix())
            print(tmp.SAMPLE.values[0])
            key = tmp.SAMPLE.values[0]
            value = metadata[metadata.ScilifeID == key].SubmittedID.values[0]
            tmp["SAMPLE_2"] = value

        table_list.append(tmp)
    return table_list


def main():
    if len(sys.argv) < 3:
        print("usage: {} [path to base dir] [metadata excel sheet]"
              .format(sys.argv[0]))
    else:
        meta = pd.read_excel(sys.argv[2])

        dataset = []
        p = Path(sys.argv[1])
        dirs = [x for x in p.iterdir() if x.is_dir()]
        print(dirs)
        for d in dirs:
            dataset.append((
                d.stem,
                pd.concat(load_all_tables(d.as_posix(), metadata=meta))))

        with pd.ExcelWriter("summary.xlsx") as writer:
            for patient in dataset:
                patient[1].to_excel(writer, sheet_name=patient[0])

        print("DONE")


if __name__ == "__main__":
    main()
