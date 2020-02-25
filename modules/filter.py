def search_data_frame(data_frame, searchedValue):
    sheet = data_frame.values.tolist()

    filtered_row = []

    for rowOfCellObjects in sheet:
        for cellObj in rowOfCellObjects:
            if searchedValue == cellObj:
                current_row = []
                for cell in rowOfCellObjects:
                    current_row.append(cell)
                filtered_row.append(current_row)

    return filtered_row
