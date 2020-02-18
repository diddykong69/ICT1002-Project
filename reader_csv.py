import pandas as pd

while True:
    try:
        file = input("File location: ")
        pd.set_option("display.width", None)
        category = pd.read_csv("NUSW-NB15_features.csv", encoding="ISO-8859-1", index_col=1)
        print(pd.read_csv(file, encoding="ISO-8859-1", names=category.index, dtype="unicode").fillna(0))
    except FileNotFoundError:
        print("Error: File not found")
    else:
        break
