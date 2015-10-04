from sys import stdin
from pandas import read_table


def read_indata(input_file, noheader, sep="\t"):

    """Reads a sep-delimited file and returns a dataframe.

    Utility function to account for the fact that there are three types
    of possible delimited files you want to handle: those with a full header,
    those with no header and those lacking a header in the index column.
    """

    infile = stdin if input_file == "-" else input_file

    header_row = None if noheader else 0

    df = read_table(infile, header=header_row, dtype=str,
                    sep=sep)

    df = _turn_index_into_regular_column_if_it_contains_data(df)

    return df


def _turn_index_into_regular_column_if_it_contains_data(df):

    if not all(df.index == range(len(df))):
        df = df.reset_index()

    return df
