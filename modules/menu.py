import pyfiglet
import pandas as pd

from modules.filter import *
from modules.reader import *
from modules.writer import *
from modules.data_to_information import data_to_information
from pathlib import Path

"""
================================================================================
# LISTS
================================================================================
"""
menu_list = ["Input file",
             "View results",
             "Exit"]

submenu_list = ["Show data",
                "Filter results",
                "Export statistics",
                "Export data",
                "Back"]

confirmation_menu_list = ['[n]: Stay',
                          '[y]: Leave']

exit_list = ['3',
             'exit',
             'end',
             'quit']

condition_list_1 = ['1',
                    'input file',
                    '-f',
                    '-i']

condition_list_2 = ['2',
                    'view',
                    '-v',
                    'show',
                    'sh']

condition_list_stay = ['n',
                       's',
                       'no',
                       'stay']

condition_list_leave = ['y',
                        'l',
                        'q',
                        'yes',
                        'leave',
                        'exit',
                        'end',
                        'quit',
                        'bye']

accepted_file_extensions = ['.csv',
                            'xlsx']

sorting_list = ["[a]: Ascending order",
                "[d]: Descending order",
                "0: I don\'t want to sort"]

ascending_sorting_list = ['a',
                          'asc',
                          'ascend',
                          'ascending']

descending_sorting_list = ['d',
                           'desc',
                           'descend',
                           'descending']

ascending_and_descending_sorting_list = ascending_sorting_list \
                                        + descending_sorting_list
"""
================================================================================
"""

"""
================================================================================
# MAIN
================================================================================
"""


def main():
    print("Welcome to")
    title = pyfiglet.figlet_format('GOTCHA!', font='slant')
    print(title)
    main_menu()


"""
================================================================================
"""

"""
================================================================================
# MAIN MENU
================================================================================
"""


def main_menu():
    input_file = None
    input_features = None
    file = None
    categories = None

    while True:
        print("What would you like to do today?")

        """
        # The main menu has 3 items: Input file, View results and Exit. However, 
        at the very start of the program, View results is not necesary since 
        users are required to input a file. 
        # This if-else block will check to see if user has already input a file 
        via the input_file variable. If user has not input, we create a new list 
        that excludes View results.  
        """
        if input_file is None:
            menu = [item for item in menu_list
                    if item != menu_list[1]]
        else:
            menu = menu_list

        """
        enumerate so we can get the index and use it as our options, 1 to 
        indicate that numbering should start from 1 (1, 2, 3) and not 0 
        (0, 1, 2, 3)
        """
        for index, item in enumerate(menu, 1):
            print(str(index) + ": " + item)

        """
        Users will type what option they want here
        """
        option_chosen = input(u"\u25B6 ").lower()
        print()

        """
        If user selects the option "Input file", users will be asked to input
        a file. This file will then call the file_check function to check if
        the input is of a valid file. If not, user will need to re-input. 
        After passing all the checks, user will repeat the process for the 
        featured files. 
        """
        if option_chosen in condition_list_1:
            try:
                while True:
                    input_file = input("Please enter log file: ")
                    file_check(input_file)
            except FileChecked:
                pass

            try:
                while True:
                    input_features = input("Please enter feature file: ")
                    print()
                    file_check(input_features)
            except FileChecked:
                pass

            file_suffix = Path(input_file).suffix
            absolute_file = Path(input_file).absolute()
            absolute_features = Path(input_features).absolute()

            if file_suffix == '.csv':
                file, categories, success = read_csv(absolute_file, absolute_features)
            elif file_suffix == '.xlsx':
                file, categories, success = read_xlsx(absolute_file, absolute_features)

        elif option_chosen in condition_list_2:
            submenu(file, categories)
        elif option_chosen in exit_list:
            confirm()
            break


"""
================================================================================
"""

"""
================================================================================
# FILE CHECK 
================================================================================
"""


class FileChecked(Exception):
    pass


"""
Check if the file exists, is not empty and is of the correct file extension. 
"""


def file_check(arg_file):
    file_exists = Path(arg_file).is_file()

    if file_exists is False:
        print("I'm sorry but I can't find your file anywhere."
              " Please try again.")
    else:
        file_path = Path(arg_file)
        file_has_content = file_path.stat().st_size
        file_suffix = file_path.suffix
        empty_file = file_has_content == 0
        not_allowed_suffix = file_suffix not in accepted_file_extensions

        if empty_file and not_allowed_suffix:
            print("Not only is this file not supported (.csv/.xlsx only) but"
                  " it's also empty ")
        elif empty_file:
            print("This file is empty.")
        elif not_allowed_suffix:
            print("File not supported. Please input only .csv or .xlsx!")
        else:
            raise FileChecked


"""
================================================================================
"""

"""
================================================================================
# SUBMENU
================================================================================
"""


def submenu(file, categories):
    while True:
        print("What would you like to do today?")

        for index, item in enumerate(submenu_list, 1):
            print(str(index) + ": " + item)
        option_chosen = input(u"\u25B6 ").lower()
        print()

        if option_chosen == '1':
            show_output(file)

        elif option_chosen == '2':
            to_filter = input("Filter: ")
            print()

            print("How would you like your data to be sorted?")
            for item in sorting_list:
                print(item)
            option_chosen = input(u"\u25B6 ").lower()

            sorting_ascending = False

            if option_chosen in ascending_and_descending_sorting_list:
                if option_chosen in ascending_sorting_list:
                    sorting_ascending = True

                search_results = pd.DataFrame(search_data_frame
                                              (sort_row_datetime
                                               (file,
                                                sorting_ascending),
                                               to_filter)
                                              )
            else:
                search_results = pd.DataFrame(search_data_frame
                                              (file,
                                               to_filter)
                                              )

            if search_results.empty:
                print("We've searched far and wide but can\'t find anything.")
            else:
                search_results.columns = categories.tolist()
                show_output(search_results)

            exporting_option = input("Do you wish to export this filtered "
                                     "result as a csv file? ([y]: Yes, "
                                     "[any other key]: No):\n")

            if exporting_option.lower() == 'y':
                export_file = input("Please enter a name for the file: ")
                if Path(export_file).suffix is not '':
                    export_file = Path(export_file).with_suffix('')

                export_csv(search_results, export_file)

        elif option_chosen == '3':
            export_file = input("Please enter a name for the file: ")

            if export_file.endswith('.xlsx'):
                write_success = data_to_information(file, export_file)
                if write_success:
                    print("Woohoo! We've successfully exported the statistics! You can find it here: "
                          "{}".format(Path(export_file).absolute()))
                else:
                    print("Uh-oh. We were unfortunately unable to export the"
                          "statistics :(")
            else:
                print("Exporting statistics to file types besides Excel files "
                      "is NOT supported.")

        elif option_chosen == '4':
            export_file = input("Please enter a name for the file: ")

            if Path(export_file).suffix is not '':
                export_file = Path(export_file).with_suffix('')

            export_csv(file, export_file)

        elif option_chosen == '5':
            break
        print()


"""
================================================================================
"""

"""
================================================================================
# CONFIRMATION MENU
================================================================================
"""


def confirm():
    while True:
        print("Are you all done for the day?")

        for item in confirmation_menu_list:
            print(item)
        option_chosen = input(u"\u25B6 ").lower()

        if option_chosen in condition_list_stay:
            main_menu()
            break
        elif option_chosen in condition_list_leave:
            break


"""
================================================================================
"""

"""
================================================================================
# EXPORT CSV
================================================================================
"""


def export_csv(search_results, export_file):
    write_success = write_csv(search_results,
                              Path(export_file).with_suffix(''))

    if write_success:
        print("Woohoo! We've successfully exported the data! You can find it here: "
              "{}".format(Path(export_file).absolute()))
    else:
        print("Uh-oh. We were unfortunately unable to export the"
              "data :(")


"""
================================================================================
"""

main()
