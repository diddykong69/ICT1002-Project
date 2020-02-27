def search_data_frame(data_frame, searchedValue):
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
    data_frame.sort_values('Stime', ascending=ascending, inplace=True)
    data_frame.reset_index(inplace=True, drop=True)
    return data_frame

