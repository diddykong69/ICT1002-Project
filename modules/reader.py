"""
Author      : How Shun Han
Description : The reader module parses input data from the user into a pandas data frame that will be used in other
            modules and functions for processing and exporting
"""

import pandas as pd
import pathlib


def read_csv(file, feature):
    success = True
    while True:
        try:
            # Display maximum number of columns
            pd.set_option("display.width", None)
            # Index 1 / Column 2 of features csv is stored as category
            category = pd.read_csv(feature, encoding="ISO-8859-1", index_col=1)
            # Reads data from file and stores in dataSet variable with category as column names
            dataSet = pd.read_csv(file, names=category.index, dtype="unicode").fillna(0)
            # Change the name of the text file to the name that user input
            filename = get_filename(file, ".csv")
            return dataSet, category.index, success
        except FileNotFoundError:
            success = False
            return None, None, success
        except pd.errors.ParserError:
            success = False
            return None, None, success


def read_xlsx(file, feature):
    success = True
    while True:
        try:
            # Display maximum number of columns
            pd.set_option("display.width", None)
            # Index 1 / Column 2 of features csv is stored as category
            category = pd.read_csv(feature, encoding="ISO-8859-1", index_col=1)
            # Reads data from file and stores in dataSet variable with category as column names
            dataSet = pd.read_excel(file, names=category.index).fillna(0)
            # Change the name of the text file to the name that user input
            filename = get_filename(file, ".xlsx")
            return dataSet, category.index, success
        except FileNotFoundError:
            success = False
            return success
        except pd.errors.ParserError:
            success = False
            return success

 
# When function is called, prints output to the user in a user friendly manner
def show_output(data):
    lines = len(data.index)
    i = 0
    while i < lines:
        print(data.iloc[i:i+5])
        user_input = input("Press enter to read more or 'q' to exit...")
        if user_input == 'q':
            break
        i += 5

 
def get_filename(filename, filetype):
    s = "\\"
    if isinstance(filename, pathlib.Path):
        filename = filename.name
    else:
        filename = filename
    if s in filename:
        filename = filename.split(s)[-1].replace(filetype, ".txt")
        return filename
    else:
        filename = filename.replace(filetype, ".txt")
        return filename


# Calls function if file is called as a script
if __name__ == "__main__":
    read_csv()
    read_xlsx()
    show_output()
