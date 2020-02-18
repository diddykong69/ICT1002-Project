import pandas as pd

# Keeps prompting user to enter file location until a valid file location is entered
while True:
    try:
        file = input("File location: ")
        # Display maximum number of columns
        pd.set_option("display.width", None)
        # Index 1 / Column 2 of features csv is stored as category
        category = pd.read_csv("NUSW-NB15_features.csv", encoding="ISO-8859-1", index_col=1)
        # Reads data from file and stores in dataSet variable with category as column names
        dataSet = pd.read_excel(file, names=category.index).fillna(0)
        print(dataSet)
    except FileNotFoundError:
        print("Error: File not found")
    else:
        break