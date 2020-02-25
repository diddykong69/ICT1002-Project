import pyfiglet

"""
================================================================================
# LISTS
================================================================================
"""
menu_list = ["1: Input file",
             "2: View Results",
             "3: Exit"]

submenu_list = ["1: Show statistics",
                "2: Filter results",
                "3: Export",
                "4: Back"]

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
            # input file function
            pass
        elif option_chosen in condition_list_2:
            submenu()


"================================================================================"

"""
================================================================================
# SUBMENU
================================================================================
"""


def submenu():
    while True:
        print("What would you like to do today?")

        for item in submenu_list:
            print(item)
        option_chosen = input(u"\u25B6 ").lower()
        print()

        if option_chosen == '1':
            # Show statistics function
            pass
        elif option_chosen == '2':
            # filter function
            pass
        elif option_chosen == '3':
            # export function
            print("export")
            pass
        elif option_chosen == '4':
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
