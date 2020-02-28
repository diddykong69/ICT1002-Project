"""
Author      : Raymous Ang
Description : The data_to_information modules consists of functions that makes use of dataframe from other modules
            and functions to create graphs and charts in a form of an excel file .xlsx when user exports statistics
"""

import pandas as pd
from collections import Counter

# bring data and put into dataframe. Input require reader: dataset, columns: variable
def dataframe(reader, name):
    list2 = []
    dict3 = {}
    df = pd.DataFrame(data=reader, columns=[name])
    list1 = df.values.tolist()

    for i in list1:
        for a in i:
            list2 += [str(a)]
    dict1 = (Counter(list2).most_common(10))
    for a, b in dict1:
        dict3[a] = b
    df2 = pd.DataFrame([dict3], index=['count'])
    return df2

# bring data and put into dataframe for line graph only. Input require reader: dataset, will only select Stime for the timeline
def timelinedict(reader2):

    df = pd.DataFrame(data=reader2, columns=['Stime'])
    list1 = df.values.tolist()
    list2 = []
    dict2 = {}
    # ensure the data are in string format
    for i in list1:
        for a in i:
            list2 += [str(a)]
    dict1 = (Counter(list2))
    # from the dictionary dict1, convert all the keys into unix time(hours only) and place into the list hours
    hours = [(pd.to_datetime(time, unit='s').hour, time) for time in dict1.keys()]
    # create another list hours_2 with the keys 0-23 to represent the hours of the day with the value 0
    hours_2 = {hour: 0 for hour in range(24)}
    
    dict1_keys = [key for key in dict1.keys()]
    # comparing the keys from hours and dict1, if same append to hours_2
    for i in range(len(dict1.items())):
        if hours[i][1] == dict1_keys[i]:
            hours_2[hours[i][0]] += int(dict1.get(dict1_keys[i]))
    df2 = pd.DataFrame([hours_2], index=['count'])
    return df2


# function to create chart
def createchart(type, dataframe, name, writer):
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
            'categories': [sheet_name, 0, 1, 0, 10],
            'values': [sheet_name, 1, 1, 1, 10],
            'name': name

        })
    if type == 'column':
        # Create a chart object.
        chart = workbook.add_chart({'type': 'column'})

        # Or using a list of values instead of category/value formulas:
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'categories': [sheet_name, 0, 1, 0, 10],
            'values': [sheet_name, 1, 1, 1, 10],
            'name': name

        })
    if type == 'line':
        # Create a chart object.
        chart = workbook.add_chart({'type': 'line'})

        # Configure the series of the chart from the dataframe data.
        #     [sheetname, first_row, first_col, last_row, last_col]
        chart.add_series({
            'categories': [sheet_name, 0, 1, 0, 24],
            'values': [sheet_name, 1, 1, 1, 24],
            'name': name
        })
        # Configure the chart axes.
        chart.set_x_axis({'name': 'Time(H)', 'position_axis': 'on_tick'})
        chart.set_y_axis({'name': 'Total Packets', 'major_gridlines': {'visible': False}})

        # Turn off chart legend. It is on by default in Excel.
        chart.set_legend({'position': 'none'})

    # Insert the chart into the worksheet.
    worksheet.insert_chart('B4', chart)
    # Close the Pandas Excel writer and output the Excel file.


# Create a Pandas Excel writer using XlsxWriter as the engine.

def data_to_information(file, location):
    try:
        excel_file = location
        # execute all the function to write out the chart
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        createchart('pie', dataframe(file, 'srcip'), 'source host', writer)
        createchart('column', dataframe(file, 'sport'), 'source port', writer)
        createchart('pie', dataframe(file, 'dstip'), 'destination host', writer)
        createchart('column', dataframe(file, 'dsport'), 'destination port', writer)
        createchart('line', timelinedict(file), 'Timeline', writer)
        writer.save()
        writer.close()
        return True
    except:
        #in case of error
        return False

