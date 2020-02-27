def search_data_frame(data_frame, searched_value):
    sheet = data_frame.values.tolist()

    filtered_row = []

    for row_of_cell_objects in sheet:
        for cell_objects in row_of_cell_objects:
            if searched_value == cell_objects:
                current_row = []
                for cell in row_of_cell_objects:
                    current_row.append(cell)
                filtered_row.append(current_row)

    return filtered_row
