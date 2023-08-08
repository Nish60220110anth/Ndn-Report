import pandas as pd
import os

def clean_file(file_name):
    """
    Replaces the unwanted characters present in the file with valid characters.

    Presence of those characters introduces bugs while reading the file 
    as csv or other format  using pandas.
    """
    with open(file_name, "r") as file:
        data = file.read()
        new_data = data.replace("\t\n", "\n")
        with open(file_name, "w+") as fl:
            fl.write(new_data)


def get_dataframe(file_name):

    if os.path.exists(file_name):
        clean_file(file_name=file_name)  # clean file if exist
        df = pd.read_csv(filepath_or_buffer=file_name,
                         sep="\t")  # read as csv with the sep of columns  = "\t"
        return df
    else:
        print("file : {0} doesn't exist".format(file_name))
        return pd.DataFrame()


def check_file_exist(file_name):
    """
    Abstraction for the os.path.exists
    """
    return os.path.exists(file_name)
