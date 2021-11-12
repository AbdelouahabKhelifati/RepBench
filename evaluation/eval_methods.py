import os

import numpy as np

from IMR import IMR
from Screen.Local import screen
from evaluation.file_manipulation import read_params, search_json
from evaluation.plotter import Plotter
import csv




def evaluate_parameter_file(injected, truth , filename, index = [] , labels = [] , plot = True, errors =  ["rmse","pearson"]):
    evaluate(injected, truth, algos=read_params(filename), index=index, labels=labels, plot=plot, errors=errors)


def evaluate_from_df(df , paramfile = None ,algos = {} , labels = []   , errors = ["rmse","pearson"]   ):

    labels = np.concatenate((labels, np.random.randint(0, high=len(df["truth"]), size=15)), axis=None)

    if paramfile is None:
        return evaluate(df["injected"], df["truth"] , algos = algos , labels = labels , errors=errors)
    else:
        return evaluate_parameter_file(df["injected"], df["truth"] , filename=paramfile , labels = labels , errors=errors)


def evaluate( injected , truth ,algos = {}  , index = [] , labels= [] , plot = True , errors = ["rmse","pearson"] ):
    """
    Running multiple algorithms and repair evaluations on the same data
    :param injected:
    :param truth:
    :param algos: list of dicts [  {"name" : "imr" , "parameters" : { "param1" : int , "param2"  : .. }  ,... ]
    :param labels:
    :param plot:
    :param errors:
    """
    observed = injected
    observed = np.array(observed)
    truth = np.array(truth)
    index =  index if (index != []) else np.arange(len(observed))

    for alg in algos:
            if alg["name"] == "imr":
                y_0 = observed.copy()
                y_0[labels] = truth[labels]
                imr_results = IMR.imr2(observed, y_0, labels,**alg["parameters"] )


                alg["repair"] = imr_results["repair"]
                alg["title"] = f'IMR{imr_results["p"],imr_results["tau"]}'
            if alg["name"] == "screen":
                screen_result = screen(np.array([index, observed]).T, **alg["parameters"])
                alg["repair"] = screen_result["repair"]
                alg["title"] = f'SCREEN{screen_result["T"],screen_result["smax"]}'


    plotter = Plotter(injected,truth,labels,index)

    for alg in algos:
        plotter.add(alg["repair"], name = alg["title"], type = alg["name"])

    plt = plotter.plotsats(eval = errors)
    plt.show()
