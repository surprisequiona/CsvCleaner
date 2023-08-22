"""
Copyright (c) 2017-2021, Zach Jetson All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Author: Thomas Wenzke
Date:   Aug 2023
Name:   csv_drop_columns.py


Keep a list of columns in a csv file and drop all other columns.

Usage: ./csv_cleaner.py [-h] -i INPUT [-o OUTPUT]

"""

import datetime
import ipaddress
import sys
from argparse import ArgumentParser
import pandas as pd


# global variables
KEEP_COLUMNS_FILE = "keep_columns.txt"
TS = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")


def remove_columns(input_csv) -> str:
    """
    Parse input csv file and keep only the columns listed in keep_columns.txt

    Args:  
        input_csv (str): input csv file
        output_csv (str): output csv file

    Returns:
        output_file (str): output csv filename
    """

    # read in the list of columns to keep
    try:
        with open(KEEP_COLUMNS_FILE, 'r', encoding='utf-8') as keep_cloumns_file:
            keep_columns = keep_cloumns_file.read().splitlines()

    except FileNotFoundError:
        print(f"Error: {KEEP_COLUMNS_FILE} not found.")
        sys.exit(1)

    print(f"\nKeeping the following list of columns: {keep_columns}")

    # read in and parse the csv file
    df = pd.read_csv(input_csv)

    # drop all columns not in the keep_columns list
    df.drop(df.columns.difference(keep_columns), axis=1, inplace=True)

    return df

def remove_rows(df) -> pd.DataFrame:
    """
    Remove rows from a dataframe based on user input

    Args:
        df (dataframe): dataframe to be filtered

    Returns:
        df (dataframe): filtered dataframe
    """
    
    header_list = df.columns.values.tolist()

    filter_input = True
    index = pd.Index([])

    while filter_input:

        criteria = {}
        for header_name in header_list:
            criteria[header_name] = str(input(f"Enter {header_name}: "))

        df_mask = None

        print(index.empty)
        for i in index:
            print(i)


        for col, value in criteria.items():
            if value != "":
                if col == "Source address" or col == "Destination address":
                    
                    ip = df[col][0]
                    network = criteria[col]
                    condition = df[col].apply(lambda ip: check_ip_network(ip, network))


                else:
                    condition = df[col] == value  
                
                if df_mask is None:
                    df_mask = condition
                
                else:
                    df_mask &= condition
        
        try:
            df = df[~df_mask]

        except TypeError:
            pass

        df.reset_index(drop=True, inplace=True)

        while True:
            filter_repeat = input("Filter again? (y/n): ")
            if filter_repeat.lower() == "y" or filter_repeat.lower() == "yes":
                break
            elif filter_repeat.lower() == "n" or filter_repeat.lower() == "no":
                filter_input = False
                break
            else:
                print("Invalid input. Try again.")
                continue
    
    return df

def check_ip_network(ip, network) -> bool:
    """
    Check if an IP address is in a network

    Args:
        ip_address (str): IP address to check
        value (str): IP network to check

    Returns:
        True if IP address is in network, False otherwise
    """

    try:
        net = ipaddress.ip_network(network)
        ip = ipaddress.ip_address(ip)
        return ip in net
    except ValueError:
        print(f"Error: {network} is not a valid IP network.")
        sys.exit(1)
    
   
def __main__():
    """
    Main function
    """

    # parse command line arguments
    argparse = ArgumentParser(description = "Parse input csv file and keep only the columns listed in keep_columns.txt")
    argparse.add_argument("-i", "--infile", required=True, type=str, help="input csv file")
    argparse.add_argument("-o", "--outfile", required=False, type=str, help="output csv file")
    argparse.add_argument("-f", "--filter", required=False, action='store_true', help="filter csv file")
    args = argparse.parse_args()

    input_csv = args.infile
    output_csv = args.outfile or "output-" + TS + "-" + input_csv
    filter_rows = args.filter

    df = remove_columns(input_csv)

    if filter_rows:
        df = remove_rows(df)

    # df.to_csv(output_csv, index=False)

    # print filename to be nice
    print(f"\nOutput file: {output_csv}\n")



if __name__ == "__main__":
    __main__()
