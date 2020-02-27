# import pyfiglet
#
# """
# ================================================================================
# # LISTS
# ================================================================================
# """
# menu_list = ["1: Input file",
#              "2: View Results",
#              "3: Exit"]
#
# submenu_list = ["1: Show statistics",
#                 "2: Filter results",
#                 "3: Export",
#                 "4: Back"]
#
# confirmation_menu_list = ['[n]: Stay',
#                           '[y]: Leave']
#
# exit_list = ['3',
#              'exit',
#              'end',
#              'quit']
#
# condition_list_1 = ['1',
#                     'input file',
#                     '-f',
#                     '-i']
#
# condition_list_2 = ['2',
#                     'view',
#                     '-v',
#                     'show',
#                     'sh']
#
# condition_list_stay = ['n',
#                        's',
#                        'no',
#                        'stay']
#
# condition_list_leave = ['y',
#                         'l',
#                         'q',
#                         'yes',
#                         'leave',
#                         'exit',
#                         'end',
#                         'quit',
#                         'bye']
# """
# ================================================================================
# """
#
# """
# ================================================================================
# # MAIN
# ================================================================================
# """
#
#
# def main():
#     print("Welcome to")
#     title = pyfiglet.figlet_format('GOTCHA!', font='slant')
#     print(title)
#     menu()
#
#
# """
# ================================================================================
# """
#
# """
# ================================================================================
# # MAIN MENU
# ================================================================================
# """
#
#
# def menu():
#     while True:
#         print("What would you like to do today?")
#
#         for item in menu_list:
#             print(item)
#         option_chosen = input(u"\u25B6 ").lower()
#         print()
#
#         if option_chosen in exit_list:
#             confirm()
#             break
#         elif option_chosen in condition_list_1:
#             # input file function
#             pass
#         elif option_chosen in condition_list_2:
#             submenu()
#
#
# "================================================================================"
#
# """
# ================================================================================
# # SUBMENU
# ================================================================================
# """
#
#
# def submenu():
#     while True:
#         print("What would you like to do today?")
#
#         for item in submenu_list:
#             print(item)
#         option_chosen = input(u"\u25B6 ").lower()
#         print()
#
#         if option_chosen == '1':
#             # Show statistics function
#             pass
#         elif option_chosen == '2':
#             # filter function
#             pass
#         elif option_chosen == '3':
#             # export function
#             print("export")
#             pass
#         elif option_chosen == '4':
#             break
#         print()
#
# """
# ================================================================================
# """
#
# """
# ================================================================================
# # CONFIRMATION MENU
# ================================================================================
# """
#
#
# def confirm():
#     while True:
#         print("Are you all done for the day?")
#
#         for item in confirmation_menu_list:
#             print(item)
#         option_chosen = input(u"\u25B6 ").lower()
#
#         if option_chosen in condition_list_stay:
#             menu()
#             break
#         elif option_chosen in condition_list_leave:
#             break
#
#
# """
# ================================================================================
# """
#
# main()

import pyfiglet

from modules.filter import *

from modules.writer import *
from modules.reader import *
from modules.data_to_information import data_to_information
import pandas as pd
import os

"""
================================================================================
# LISTS
================================================================================
"""
menu_list = ["1: Input file",
             "2: View Results",
             "3: Exit"]

submenu_list = ["1: Export statistics",
                "2: Filter results",
                "3: Export",
                "4: View data set",
                "5: Back"]

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
    menu()


"""
================================================================================
"""

"""
================================================================================
# MAIN MENU
================================================================================
"""


def menu():
    while True:
        print("What would you like to do today?")

        for item in menu_list:
            print(item)
        option_chosen = input(u"\u25B6 ").lower()
        print()

        if option_chosen in exit_list:
            confirm()
            break
        elif option_chosen in condition_list_1:
            input_file = input("Please enter log file: ")
            input_features = input("Please enter feature file: ")
            if input_file.split('.')[-1] == 'csv':
                file, categories, success = read_csv(input_file, input_features)
            elif input_file.split('.')[-1] == 'xlsx':
                file, categories, success = read_xlsx(input_file, input_features)
            else:
                print("File not supported. Please input only .csv or .xlsx!")
        elif option_chosen in condition_list_2:
            submenu(file, categories)


"================================================================================"

"""
================================================================================
# SUBMENU
================================================================================
"""


def submenu(file, categories):
    while True:
        print("What would you like to do today?")

        for item in submenu_list:
            print(item)
        option_chosen = input(u"\u25B6 ").lower()
        print()

        if option_chosen == '1':
            export_file = input("Please enter name of file to export to: ")
            if export_file.endswith('.xlsx'):
                write_success = data_to_information(file, export_file)
                if write_success:
                    print("Export Statistics Operation: Successful")
                else:
                    print("Export Statistics Operation: Failure")
            else:
                print("Exporting statistics to file types other than Excel files is *not* supported.")
            # Show statistics function
            pass
        elif option_chosen == '2':
            # filter function
            to_filter = input("Filter: ")
            # print("File: ", file)
            # print("To filter: ", to_filter)
            # while True:
            sorting_option = input("Sort it in ascending (a) or descending (d) (Press 0 to continue without sorting): ").lower()
            sorting = False
            sorting_ascending = False
            if sorting_option in ['a', 'd']:
                sorting = True
            if sorting_option == 'a':
                sorting_ascending = True

            if sorting:
                search_results = pd.DataFrame(search_data_frame(sort_row_datetime(file, sorting_ascending), to_filter))
            else:
                search_results = pd.DataFrame(search_data_frame(file, to_filter))
            if search_results.empty:
                print("No results found.")
            else:
                search_results.columns = categories.tolist()
                show_output(search_results)

            exporting_option = input("Do you wish to export this filtered result? ('y' for yes and 'n' for no): ").lower()
            if exporting_option == 'y':
                export_file = input("Please enter name of file to export to: ")
                if export_file.endswith('.csv'):
                    write_success = write_csv(search_results, os.path.splitext(export_file)[0])
                    if write_success:
                        print("Export Search Results Operation: Successful")
                    else:
                        print("Export Search Results Operation: Failure")
                else:
                    print("Exporting search results to file types other than csv files is *not* supported.")
            pass
        elif option_chosen == '3':
            export_file = input("Please enter name of file to export to: ")
            if export_file.endswith('.csv'):
                write_success = write_csv(file, os.path.splitext(export_file)[0])
                if write_success:
                    print("Export Data Set Operation: Successful")
                else:
                    print("Export Data Set Operation: Failure")
            else:
                print("Exporting data set to file types other than csv files is *not* supported.")
            pass
        elif option_chosen == '4':
            show_output(file)
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
            menu()
            break
        elif option_chosen in condition_list_leave:
            break


"""
================================================================================
"""

main()
