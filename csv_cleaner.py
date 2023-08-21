"""
Author: Thomas Wenzke
Date:   Aug 2023
Name:   csv_drop_columns.py


Quickly resolve a large host file list to IP addresses and print them into a table.

Usage: ./resolv.py hostnames.txt -i infile.csv -o outfile.csv

"""

import datetime
from argparse import ArgumentParser
import pandas as pd

# global variables
KEEP_COLUMNS_FILE = "keep_columns.txt"
TS = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

def parse_csv(input_csv, output_csv) -> str:
    """
    Parse input csv file and keep only the columns listed in keep_columns.txt

    Args:  
        input_csv (str): input csv file
        output_csv (str): output csv file

    Returns:
        output_file (str): output csv filename
    """

    # read in the list of columns to keep
    with open(KEEP_COLUMNS_FILE, 'r', encoding='utf-8') as keep_cloumns_file:
        keep_columns = keep_cloumns_file.read().splitlines()

    print(f"\nKeeping the following list of columns: {keep_columns}")
        
    # read in and parse the csv file
    data = pd.read_csv(input_csv)
    data.drop(data.columns.difference(keep_columns), axis=1, inplace=True)    
    data.to_csv(output_csv, index=False)

    return output_csv


def __main__():
    """
    Main function
    """

    argparse = ArgumentParser()

    argparse.add_argument("-i", "--input", required=True, type=str, help="input csv file")
    argparse.add_argument("-o", "--output", required=False, type=str, help="output csv file")
    args = argparse.parse_args()

    input_csv = args.input
    output_csv = args.output

    if not output_csv:
        print("No output file specified, using default output file name.")
        output_csv = "output-" + TS + "-" + input_csv


    # create output csv file name
    output_file = parse_csv(input_csv, output_csv)

    # print filename to be nice
    print(f"\nOutput file: {output_file}\n")


if __name__ == "__main__":
    __main__()
