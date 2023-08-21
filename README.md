# CsvCleaner
Clean CSV columns for less noise

## Requirements
* **Python 3.5+**

* **keep_columns.txt**: list of columns to keep

## Installation
First make sure you have python 3.4+ and the python package manger (pip).
    
    python3 --version
    which pip3
    
Download all the dependencies using the package manager:

    pip3 install -r requirements.txt
    
**Thats it!**

Optionally, you can use virtual_env or other tools to manage your packages.


## Usage

    python3 csv_cleaner.py -i csv_file.csv
    
**Specify output filename**

Default filename prepends date time stamp to the input filename.

    python3 csv_cleaner.py -i csv_file.csv -o output_file.csv
    

## Future

 - Expand to include a drop columns function
 