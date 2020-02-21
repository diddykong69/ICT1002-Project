import pandas as pd


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
            return dataSet, category.index, success
        except FileNotFoundError:
            success = False
            return success
        except pd.errors.ParserError:
            success = False
            return success


# Calls function if file is called as a script
if __name__ == "__main__":
    read_csv()
    read_xlsx()
