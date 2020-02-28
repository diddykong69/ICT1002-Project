def search_data_frame(data_frame, searchedValue):
    """
    This function searches for searchedValue inside the data_frame
    :param data_frame: data_frame is received by read_csv after reading the csv/xlsx file input by the user
    :param searchedValue: searchedValue input by the user to filter results
    :return: filtered_row: list of rows that are filtered based on searchedValue
    """
    sheet = data_frame.values.tolist()

    filtered_row = []

    for rowOfCellObjects in sheet:
        for cellObj in rowOfCellObjects:
            if str(searchedValue).lower() == str(cellObj).lower():
                current_row = []
                for cell in rowOfCellObjects:
                    current_row.append(cell)
                filtered_row.append(current_row)
    return filtered_row


def sort_row_datetime(data_frame, ascending=True):
    """
    This function sort the data based on Stime(start time) on ascending or descending order depending on user
    :param data_frame: dataframe is received by read_csv after reading the csv/xlsx file input by the user
    :param ascending: Order is sorted by ascending order(= true) or descending order (= false)
    :return: data_frame: data_frame that is sorted according to user's needs
    """
    data_frame.sort_values('Stime', ascending=ascending, inplace=True)
    data_frame.reset_index(inplace=True, drop=True)
    return data_frame

