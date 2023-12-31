from testing_frame_work.parse_toml import load_toml_file
import injection.injection_config as ic
from testing_frame_work.parser_init import init_parser
import algorithms.algorithms_config as algc
import injection.injection_config as at


repair_estimators = algc.ALGORITHM_TYPES
estimator_choices = repair_estimators + ["all"]

scenarios = [ic.ANOMALY_SIZE, ic.CTS_NBR , ic.ANOMALY_RATE, ic.TS_LENGTH, ic.TS_NBR , ic.ANOMALY_FACTOR]
scenario_choices = scenarios + ["all"]

all_anomalies = [at.AMPLITUDE_SHIFT,at.DISTORTION,at.POINT_OUTLIER]
anomaly_choices =all_anomalies+["all"]

error_scores = ["rmse_full","rmse_partial","mae","mutual_info"]


def init_checked_parser(input):
    args = init_parser(input=input,
                       estimator_choices=estimator_choices,
                       scenario_choices=scenario_choices,
                       anomaly_choices=anomaly_choices)

    return args

def parse_scen_names(args):
    scen_params = args.scen
    scen_names = scenarios if "all" in scen_params else scen_params
    return scen_names

def parse_repair_algorithms(args):
    if "all" in args.alg:
        return algc.ALGORITHM_TYPES
    return args.alg

def parse_repair_algorithms_x(args):
    if args.algx is not None:
        filename = args.algx
        param_dict = load_toml_file(filename)
        repair_algos = []

        for alg_type, params in param_dict.items():
            direct_params = {k: v for k, v in params.items() if not isinstance(v, dict)}
            if len(direct_params) > 0:
                repair_algos.append({"type": alg_type , "name" : alg_type  , "params" : direct_params})
            for name, inner_params in params.items():
                if isinstance(inner_params, dict):
                    repair_algos.append({"type" : alg_type , "name" : name , "params" : inner_params})

        return repair_algos




def parse_anomaly_types(args):
    anomaly_types_param = args.a
    anomalies = [at.parse_anomaly_name(anomaly) for anomaly in anomaly_types_param] if "all" not in anomaly_types_param \
        else all_anomalies
    return anomalies


def parse_training_arguments(args):
    train_method = args.train
    train_error = args.train_error
    return train_method, train_error

