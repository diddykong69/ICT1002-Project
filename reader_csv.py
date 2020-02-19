import pandas as pd


def read():
    # Keeps prompting user to enter file location until a valid file location is entered
    while True:
        try:
            file = input("File location: ")
            # Display maximum number of columns
            pd.set_option("display.width", None)
            # Index 1 / Column 2 of features csv is stored as category
            category = pd.read_csv("NUSW-NB15_features.csv", encoding="ISO-8859-1", index_col=1)
            # Reads data from file and stores in dataSet variable with category as column names
            dataSet = pd.read_csv(file, encoding="ISO-8859-1", names=category.index, dtype="unicode").fillna(0)
            return dataSet
        except FileNotFoundError:
            print("Error: File not found")
        else:
            break


# Calls function if file is called as a script
if __name__ == "__main__":
    read()
