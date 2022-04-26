import itertools
import os.path

from matplotlib import pyplot as plt

from Repair.Dimensionality_Reduction.CDrec.CD_Rec_estimator import CD_Rec_estimator
from Repair.Dimensionality_Reduction.RobustPCA.Robust_pca_estimator import Robust_PCA_estimator
from Repair.IMR.IMR_estimator import IMR_estimator
from Repair.Screen.SCREENEstimator import SCREEN_estimator
import  Scenarios.Anomaly_Types as at
from Scenarios.scenario_saver.Scenario_saver import save_scenario
from Scenarios.scenario_types.BaseScenario import BaseScenario
import Scenarios.scenario_types.ScenarioConfig as sc
from run_ressources.parser_init import init_parser
from run_ressources.parser_results_extraction import *

current_path = os.getcwd()
folder = "MA"
path = folder.join(current_path.split(folder)[:-1]) + folder
os.chdir(path)


repair_estimators = {"rpca" : Robust_PCA_estimator , "screen": SCREEN_estimator , "cdrec" : CD_Rec_estimator , "imr" : IMR_estimator }
estimator_choices = list(repair_estimators.keys()) + ["all"]

scenarios = [sc.TS_NBR,sc.ANOMALY_RATE, sc.ANOMALY_SIZE, sc.CTS_NBR , sc.TS_LENGTH]
scenario_choices = scenarios + ["all"]

all_anomalies = [at.AMPLITUDE_SHIFT,at.DISTORTION,at.POINT_OUTLIER,at.GROWTH_CHANGE]
anomaly_choices =all_anomalies+["all"]

def main(input = None):
    data_dir =  os.listdir("Dataa")
    data_dir_trim = [txt.split(".")[0] for txt in data_dir]
    args = init_parser( input = input ,
                        estimator_choices = estimator_choices,
                        scenario_choices=scenario_choices ,
                        data_choices=data_dir_trim + ["all"],
                        anomaly_choices = anomaly_choices)

    scen_params = args.scenario
    data_params = args.data
    estim_params = args.alg
    anomaly_types_param = args.a_type

    # map scenario input
    cols = [0] #(args.col)
    scenario_constructors = [SCENARIO_CONSTRUCTORS[scen] for scen in scenarios] if "all" in scen_params \
        else [SCENARIO_CONSTRUCTORS[scen] for scen in scen_params]

    # map data input
    data_files = [f'{data_param}.csv' for data_param in data_params] if "all" not in data_params \
        else [d for d in data_dir if os.path.isfile(f"Dataa/{d}")]

    # map repair estimator input
    scenario_constructors_data_names = itertools.product(scenario_constructors, data_files)
    estimators =  [repair_estimators[estim_param](columns_to_repair=cols) for estim_param in estim_params] if "all" not in estim_params\
        else [estim(columns_to_repair=cols) for estim in repair_estimators.values()]

    anomalies = [parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in estim_params \
        else all_anomalies


    for (scenario_constructor, data_name , anomaly_type) in itertools.product(scenario_constructors, data_files , anomalies):
        print(str(scenario_constructor).split(".")[-1][:-2], data_name ,anomaly_type )
        # todo map scenarioinput and anomaly input -> scen anonaly a ,  scen anonaly a,b if scenario suppoerst mutiple anomalies
        injected_scenario: BaseScenario = scenario_constructor(data_name, cols_to_inject=cols,
                                                               anomaly_type=anomaly_type)
        for estim in estimators:
            for name, train, test in injected_scenario.name_train_test_iter:
                data_params = {}
                data_params["truth"] = test["original"]
                injected = test["injected"]
                truth = test["truth"]

                data_params["cols"] = test["columns"]
                train_injected, train_truth = train["injected"], train["original"]

                estim.train(train_injected, train_truth)
                repair_out_put = estim.repair(injected, truth)
                injected_scenario.add_repair(name, repair_out_put, repair_out_put["type"])

                # logging.info(
                #     f'failed repair: scen: {scenario_constructor} . data_name: {data_name} , estimator: {estim}')
                # logging.error(f'{e})')

        save_scenario(injected_scenario,repair_plot=True)
        # logging.info(
        #     f'failed save: scen: {scenario_constructor} . data_name: {data_name} , estimator: {estim}')
        # logging.error(f'{e})')


if __name__ == '__main__':
    main()