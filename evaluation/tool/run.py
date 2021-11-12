import argparse
import os
import pandas as pd
import numpy as np
import sys
#problems :
#labels , before anomaly yes no?
#-> either data contains an entry labels or label will be randomly generated (but how)
#idea folder or subfolder
#if no parameter

#
#-data file1,file2,folder


sys.path.append('../../')

from evaluation.eval_methods import evaluate, evaluate_from_df
from evaluation.file_manipulation import files_from_comma_string, get_df_from_file, search_json, anom_dict_from_json

os.chdir("/".join(os.getcwd().split("/")[:-2]))

parser = argparse.ArgumentParser()
parser.add_argument("-data","-d" ,nargs=1, type=str , default="")
parser.add_argument('-algo',   nargs=1, default=[])
parser.add_argument('-algox',nargs=1, default=[])

parser.add_argument('-save',  nargs="*", type=str , default=False )
parser.add_argument('-plotoff', action='store_false')
parser.add_argument('-withoutlegend', action='store_false')

args = parser.parse_args()

files = args.data[0]
print("files" ,files)
print(files_from_comma_string(files))
for file in files_from_comma_string(files):
    df = get_df_from_file(file)
    try:
        data = anom_dict_from_json(file)
        labels = [0, 1, 2]
        for anom in data.values():
            print(anom)
            labels += anom["index_range"][0:min(3, len(anom["index_range"]))]
        labels = np.concatenate((labels, np.random.randint(0, high=len(df["truth"]), size=15)), axis=None)
    except:
        print("no marked anomaly start found for IMR random labels assigned")
        labels = np.random.randint(0, high=len(df["truth"]),size= int(len(df["truth"])/15))
        pass

    for i in args.algo:
        algos = [{"name": alg, "parameters": {}} for alg in i.split(",")]

        eval = evaluate_from_df(df, algos = algos , labels= labels)
        print("eval" ,eval)

    for i in args.algox:
        print(i)
        eval = evaluate_from_df(df,paramfile = i, labels= labels)


