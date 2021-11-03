import pickle
import string
from pathlib import Path
from typing import Union, List

import pandas as pd

EXPECTED_COLUMNS = ['age', 'job', 'marital', 'education', 'default', 'balance', 'housing', 'loan', 'contact', 'day', 'month', 'duration', 'campaign', 'pdays', 'previous', 'poutcome']
CATEGORICAL_COLUMN_NAMES = ["job", "marital", "education", "default", "housing", "loan", "contact", "month", "poutcome", "y"]

PUNCTUATION_TRANSLATION = str.maketrans('', '', string.punctuation)
cat_lookup = pickle.load(open("category_lookup.p","rb"))

def coarce_csv(csv:pd.DataFrame, keep_target_col:bool=False) -> list:
    """
    Validate dataframe validity and coerce columns to needed form and type
    :param csv: CSV file as pandas dataframe
    :return: List of names of columns that weren't found in dataframe
    """

    missing_columns = EXPECTED_COLUMNS.copy()
    drop_columns: List = []
    columns: List = list(csv.columns)
    for i in range(len(columns)-1, -1, -1): # reverse iterate columns so can remove from columns list within loop

        col = columns[i]

        if col in missing_columns:
            missing_columns.remove(col)
        elif (clean_column:=col.lower().translate(PUNCTUATION_TRANSLATION)) in missing_columns:
            columns[i] = clean_column
            missing_columns.remove(clean_column)
        elif col=="y" and keep_target_col:
            continue
        else:
            drop_columns.append(col)
            del(columns[i]) # remove by index so duplicate columns don't break iteration

    if len(drop_columns) > 0:
        csv.drop(drop_columns, axis=1, inplace=True) # remove extra columns in-place so callers dataframe reference is updated too
    csv.columns = columns

    insert_pos = len(csv.columns)
    if len(missing_columns) >0:
        for col in missing_columns:
            try:
                if col in CATEGORICAL_COLUMN_NAMES:
                    csv.insert(insert_pos, col, "unknown")
                else:
                    csv.insert(insert_pos, col, -1)
            except ValueError: # don't try and reinsert for whatever reason
                continue

    return missing_columns

def type_check_variables(df:pd.DataFrame):
    """
    Categorialise variables according to categories recognised by original encoding and
    coarce numericals into correct type replacing invalid entries (strings) with NaN then NaN to -1
    :param df: Pandas dataframe
    :return: None. Updates occur in place.
    """

    for col in df.columns:
        if col in CATEGORICAL_COLUMN_NAMES: # force columns values to categories defined in original banking data file
            df[col] = pd.Categorical(df[col], categories=cat_lookup[col])
        else: # force invalid entries in numerical columns to be NaN then fill NaN values with -1
            df[col] = pd.to_numeric(df[col], errors="coerce").fillna(-1)

    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

def form_as_dataframe(form_dictionary:dict) -> (pd.DataFrame, List[str]):
    """
    Convert python diction object to a validated / type checked pandas dataframe
    :param form_dictionary: Dictionary where keys are form/dataframe columns and values are raw input values
    :return: (pandas dataframe, list of missing columns from input dictionary)
    """
    df = pd.DataFrame([form_dictionary.values()], columns=form_dictionary.keys())
    missing_columns = coarce_csv(df)
    type_check_variables(df)

    return df, missing_columns

def parse_csv(file_path:Union[str, Path])->(pd.DataFrame, List[str]):
    """
    Parse CSV file saved to disk, handling all variable type checking and
    field manipulation
    :param file_path: Path to file on disk
    :return: (csv file as dataframe, list of columns missing from csv file -- empty if all columns correct)
    """

    try:
        csv_data = pd.read_csv(file_path, usecols=EXPECTED_COLUMNS, delimiter=";")
        missing_columns = []
    except ValueError:
        is_bad_parse = True
        csv_data = pd.read_csv(file_path, delimiter=";", index_col=0)
        missing_columns = coarce_csv(csv_data)

    type_check_variables(csv_data)

    return csv_data, missing_columns
