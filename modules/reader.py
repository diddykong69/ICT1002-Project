import pandas as pd
import csv

def read_csv(file, feature):
    success = True
    while True:
        try:
            # Display maximum number of columns
            pd.set_option("display.width", None)
            # Index 1 / Column 2 of features csv is stored as category
            category = pd.read_csv(feature, encoding="ISO-8859-1", index_col=1)
            # Reads data from file and stores in dataSet variable with category as column names
            dataSet = pd.read_csv(file, encoding="ISO-8859-1", names=category.index, dtype="unicode").fillna(0)
            # Change the name of the text file to the name that user input
            to_text(dataSet, get_filename(file, ".csv"))
            return dataSet, category.index, success
        except FileNotFoundError:
            success = False
            return success
        except pd.errors.ParserError:
            success = False
            return success


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
            to_text(dataSet, get_filename(file, ".xlsx"))
            return dataSet, category.index, success
        except FileNotFoundError:
            success = False
            return success
        except pd.errors.ParserError:
            success = False
            return success
  
# Outputs data of file read into a text file for database purposes
def to_text(data, location):
    csv_file = data.to_csv("data.csv", index=False)
    with open(location, "w") as output_file:
        with open("data.csv", "r") as input_file:
            [output_file.write("\t".join(row)+'\n') for row in csv.reader(input_file)]
        output_file.close()
        
 
# When function is called, prints output to the user in a user friendly manner
def show_output(data):
    lines = len(data.index)
    i = 0
    while i < lines:
        print(data.iloc[i:i+5])
        input("Press enter to read more...")
        i += 5

 
def get_filename(filename, filetype):
    s = "\\"
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
