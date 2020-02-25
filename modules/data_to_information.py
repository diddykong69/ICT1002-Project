# import csv
import pandas as pd
# import matplotlib.pyplot as plt
# from vincent.colors import brews
from collections import Counter


def dataframe(reader, name):
    list2 = []
    df = pd.DataFrame(data=reader, columns=[name])
    list1 = df.values.tolist()

    for i in list1:
        for a in i:
            list2 += [a]
    dict1 = Counter(list2)

    df2 = pd.DataFrame([dict1], index=['count'])
    return df2


# function to create chart
def createchart(type, dataframe, name):
    sheet_name = str(name)
    dataframe.to_excel(writer, sheet_name=sheet_name)

    # Access the XlsxWriter workbook and worksheet objects from the dataframe.
    workbook = writer.book
    worksheet = writer.sheets[sheet_name]
    if type == 'pie':
        # Create a chart object.
        chart = workbook.add_chart({'type': 'pie'})

        # Or using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'categories': [sheet_name, 0, 1, 0, 125],
            'values': [sheet_name, 1, 1, 1, 125],
            'name': name

        })
    if type == 'column':
        # Create a chart object.
        chart = workbook.add_chart({'type': 'column'})

        # Or using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'categories': [sheet_name, 0, 1, 0, 15],
            'values': [sheet_name, 1, 1, 1, 15],
            'name': name

        })

    # Insert the chart into the worksheet.
    worksheet.insert_chart('B4', chart)
    # Close the Pandas Excel writer and output the Excel file.
    print('here')


# Create a Pandas Excel writer using XlsxWriter as the engine.

def data_to_information(file, location):
    # excel_file = 'information.xlsx'
    excel_file = location
    #file = pd.read_csv("UNSW-NB15_1_test.csv")
    writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
    createchart('pie', dataframe(file, 'srcip'), 'source host')
    createchart('pie', dataframe(file, 'dstip'), 'destination host')
    createchart('column', dataframe(file, 'dsport'), 'destination port')
    writer.save()
    writer.close()


