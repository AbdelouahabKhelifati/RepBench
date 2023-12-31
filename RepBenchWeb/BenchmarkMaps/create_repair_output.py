from testing_frame_work.repair import AnomalyRepairer
from RepBenchWeb.BenchmarkMaps.repairCreation import injected_container_None_Series
from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data


def repair_from_None_series(alg_type,params, truth_df, injected_series):
    injected_data_container = injected_container_None_Series(truth_df, injected_series)

    repairer = AnomalyRepairer(1, 1)
    repair_info = repairer.repair_data_part(alg_type, injected_data_container, params)

    repair = repair_info["repair"]
    scores = repair_info["scores"]

    error_map = { "rmse" :  "RMSE", "mae" : "MAE", "partial_rmse" : "RMSE on Anomaly" , "runtime" : "runtime"}
    data = {"data" : [{"name": error_map[k], "y": v} for k, v in scores.items() if  k in error_map.keys() ] }
    metrics = list(scores.keys())
    alg_name = f"{alg_type}{tuple((v for v in params.values()))}"
    scores = {"name": alg_name, "colorByPoint": "true", "data": data}


    links = { inj_object["linkedTo"]: inj_object["id"] for inj_object in injected_series }
    repaired_series = map_repair_data(repair, injected_data_container,alg_name,links)
    return {"repaired_series": repaired_series, "scores": scores ,"metrics" : metrics}




