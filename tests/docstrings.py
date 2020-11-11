"""
Summary line.

Extended description of function.

Parameters
----------
arg1 : int
    Description of arg1
arg2 : str
    Description of arg2

Returns
-------
int
    Description of return value

"""




def my_function(my_arg, my_other_arg):
    """A function just for me.

    :param my_arg: The first of my arguments.
    :param my_other_arg: The second of my arguments.

    :returns: A message (just for me, of course).
    """




Google Docstrings Example

"""Gets and prints the spreadsheet's header columns

Args:
    file_loc (str): The file location of the spreadsheet
    print_cols (bool): A flag used to print the columns to the console
        (default is False)

Returns:
    list: a list of strings representing the header columns
"""

reStructured Text Example

"""Gets and prints the spreadsheet's header columns

:param file_loc: The file location of the spreadsheet
:type file_loc: str
:param print_cols: A flag used to print the columns to the console
    (default is False)
:type print_cols: bool
:returns: a list of strings representing the header columns
:rtype: list
"""

NumPy/SciPy Docstrings Example

"""Gets and prints the spreadsheet's header columns

Parameters
----------
file_loc : str
    The file location of the spreadsheet
print_cols : bool, optional
    A flag used to print the columns to the console (default is False)

Returns
-------
list
    a list of strings representing the header columns
"""

Epytext Example

"""Gets and prints the spreadsheet's header columns

@type file_loc: str
@param file_loc: The file location of the spreadsheet
@type print_cols: bool
@param print_cols: A flag used to print the columns to the console
    (default is False)
@rtype: list
@returns: a list of strings representing the header columns
"""






"""This is the summary line

This is the further elaboration of the docstring. Within this section,
you can elaborate further on details as appropriate for the situation.
Notice that the summary and the elaboration is separated by a blank new
line.
"""

# Notice the blank line above. Code should continue on this line.


"""summary

long description
"""




class SimpleClass:
    """Class docstrings go here."""

    def say_hello(self, name: str):
        """Class method docstrings go here."""

        print(f'Hello {name}')





Package and Module Docstrings

Package docstrings should be placed at the top of the package’s __init__.py file. This docstring should list the modules and sub-packages that are exported by the package.

Module docstrings are similar to class docstrings. Instead of classes and class methods being documented, it’s now the module and any functions found within. Module docstrings are placed at the top of the file even before any imports. Module docstrings should include the following:

    A brief description of the module and its purpose
    A list of any classes, exception, functions, and any other objects exported by the module

The docstring for a module function should include the same items as a class method:

    A brief description of what the function is and what it’s used for
    Any arguments (both required and optional) that are passed including keyword arguments
    Label any arguments that are considered optional
    Any side effects that occur when executing the function
    Any exceptions that are raised
    Any restrictions on when the function can be called








Script Docstrings

Scripts are considered to be single file executables run from the console. Docstrings for scripts are placed at the top of the file and should be documented well enough for users to be able to have a sufficient understanding of how to use the script. It should be usable for its “usage” message, when the user incorrectly passes in a parameter or uses the -h option.

If you use argparse, then you can omit parameter-specific documentation, assuming it’s correctly been documented within the help parameter of the argparser.parser.add_argument function. It is recommended to use the __doc__ for the description parameter within argparse.ArgumentParser’s constructor. Check out our tutorial on Command-Line Parsing Libraries for more details on how to use argparse and other common command line parsers.

Finally, any custom or third-party imports should be listed within the docstrings to allow users to know which packages may be required for running the script. Here’s an example of a script that is used to simply print out the column headers of a spreadsheet:

"""Spreadsheet Column Printer

This script allows the user to print to the console all columns in the
spreadsheet. It is assumed that the first row of the spreadsheet is the
location of the columns.

This tool accepts comma separated value files (.csv) as well as excel
(.xls, .xlsx) files.

This script requires that `pandas` be installed within the Python
environment you are running this script in.

This file can also be imported as a module and contains the following
functions:

    * get_spreadsheet_cols - returns the column headers of the file
    * main - the main function of the script
"""

import argparse

import pandas as pd


def get_spreadsheet_cols(file_loc, print_cols=False):
    """Gets and prints the spreadsheet's header columns

    Parameters
    ----------
    file_loc : str
        The file location of the spreadsheet
    print_cols : bool, optional
        A flag used to print the columns to the console (default is
        False)

    Returns
    -------
    list
        a list of strings used that are the header columns
    """

    file_data = pd.read_excel(file_loc)
    col_headers = list(file_data.columns.values)

    if print_cols:
        print("\n".join(col_headers))

    return col_headers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        'input_file',
        type=str,
        help="The spreadsheet file to pring the columns of"
    )
    args = parser.parse_args()
    get_spreadsheet_cols(args.input_file, print_cols=True)


if __name__ == "__main__":
    main()
