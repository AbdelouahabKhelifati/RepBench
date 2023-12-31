import json

import numpy as np
import pandas as pd
import os

from injection import inject_data_df
from recommendation.feature_extraction.feature_extraction import extract_features
import csv

from recommendation.utils.file_parsers import read_file_to_pandas

default_data_folder = "recommendation/datasets/train"


def load_data(injection_parameters,
              return_truth=True,
              data_folder=default_data_folder,
              row_cap=20000, col_cap=20 , normalize= True):
    """
    Args:
    injection_parameters: dict = {
            "seed": seed,
            "factor": factor,
            "cols" (int): columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }
        return_truth (bool): Whether to return the original dataset as well as the injected dataset
            (default is True).
        data_folder (str): The path to the folder where the CSV dataset file is located (default is
            default_data_folder).
        row_cap (int): The maximum number of rows to load from the dataset file (default is 20000).
        col_cap (int): The maximum number of columns to load from the dataset file (default is 20).

    Returns:
        If return_truth is True, returns a tuple containing two pandas DataFrames: the injected dataset
        and the original dataset (before injection). If return_truth is False, returns only the injected
        dataset as a pandas DataFrame.

    """
    injection_parameters = injection_parameters.copy()
    dataset = injection_parameters.pop("dataset")
    cols = injection_parameters["cols"]
    truth_df: pd.DataFrame = read_file_to_pandas(f"{data_folder}/{dataset}")


    # z-score  normalization and cutting
    n, m = truth_df.shape

    truth_df = truth_df.iloc[:min(n, row_cap), :min(m, col_cap)]
    truth_mean, truth_std = truth_df.mean(), truth_df.std()

    truth_df = (truth_df - truth_mean) / truth_std

    injected_df, col_range_map = inject_data_df(truth_df, **injection_parameters)
    assert injected_df.shape == truth_df.shape
    assert not np.allclose(injected_df.iloc[:, cols[0]].values, truth_df.iloc[:, cols[0]].values)

    if not normalize:
        injected_df = injected_df * truth_std + truth_mean
        truth_df = truth_df * truth_std + truth_mean

    if return_truth:
        return injected_df, truth_df
    return injected_df




def load_features(injection_parameters,data_folder,use_rawdata=False):
    """
    param: injection_parameters: dict
       injection_parameters = {
            "seed": seed,
            "factor": factor,
            "cols": columns,
            "dataset": dataset,
            "a_type": a_type,
            "a_percent": a_percentage
        }

    return: features: dict of features for the selected column
    """
    injected_df, _ = load_data(injection_parameters, data_folder=data_folder, normalize= not use_rawdata)
    features = extract_features(injected_df, column=injection_parameters["cols"][0])
    return features

def get_injection_parameter_hashes_checker(file_name):
    if not os.path.exists(file_name):
        return lambda x: False

    with open(file_name, "r") as f:
        lines = f.readlines()

    injection_parameters_strings = set()
    for line in lines:
        injection_parameters = json.loads(line)["injection_parameters"]
        str_value = str(injection_parameters.values())
        injection_parameters_strings.add(str_value)

    def checker(injection_parameters):
        new_value = str(injection_parameters.values())
        return new_value in injection_parameters_strings

    return checker


def compute_features(load_filename,  store_filename, data_folder, use_rawdata=True):
    """
    Args:
        load_filename (str): The path to the file containing the injection parameters.
        store_filename (str): The path to the file where the features will be stored.
        use_rawdata (bool): Whether undo normalization to compute the features (default is True).

    Returns:
        A list of dictionaries containing the injection parameters and the features for each injection.
    """

    if not os.path.exists(store_filename):
        os.makedirs(os.path.dirname(store_filename), exist_ok=True)

    with open(store_filename, "w") as f:
        f.write("")

    with open(load_filename, "r") as f:
        lines = f.readlines()
    results = []
    total_lines = len(lines)
    for i,line in enumerate(lines):
        results_line = json.loads(line)
        injection_parameters = results_line["injection_parameters"]
        features = load_features(injection_parameters,data_folder=data_folder , use_rawdata=use_rawdata)
        results_line["features"] = features
        results.append(results_line)
        # store result to file
        with open(store_filename, "a") as f:
            # for result in results:
            f.write(json.dumps(results_line) + "\n")
        show_progress_bar(i + 1, total_lines, prefix='Loading features:', suffix='Complete', length=50)
    return results

def show_progress_bar(iteration, total, prefix='', suffix='', decimals=1, length=50, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    bar = fill * filled_length + '-' * (length - filled_length)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end='\r')
    # Print New Line on Complete
    if iteration == total:
        print()
