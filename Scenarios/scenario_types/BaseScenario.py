import pandas as pd

from Scenarios.Anomaly_Types import *
import numpy as np
from Injection.injection_methods.basic_injections import add_anomaly
from Injection.injection_methods.index_computations import get_random_ranges
from Scenarios.scenario_types.Scenario_Types import BASE_SCENARIO, scenario_specifications


class BaseScenario():
    scenario_type = BASE_SCENARIO
    small_data_description = "data size"

    def __init__(self, anomaly_type=AMPLITUDE_SHIFT,
                 anomaly_percentage=None,
                 anomaly_length=None,
                 default_params=scenario_specifications[scenario_type]):

        self.anomaly_percentage = anomaly_percentage or default_params["anomaly_percentage"]
        self.anomaly_length = anomaly_length or default_params["anomaly_length"]
        self.anomaly_type = anomaly_type

    def get_amount_of_anomalies(self, data):
        anom_amount = round(len(data) * self.anomaly_percentage / self.anomaly_length)
        return anom_amount

    def inject_single(self, data,seed  =100):
        index_ranges = get_random_ranges(data, self.anomaly_length
                                         , number_of_ranges=self.get_amount_of_anomalies(data),seed  =seed)
        anomaly_infos = []
        if self.anomaly_length == 6:
            print(index_ranges)
        for range_ in index_ranges:
            data, info = add_anomaly(anomaly_type=self.anomaly_type, data=data, index_range=range_)
            anomaly_infos.append(info)
        return data, anomaly_infos

    @staticmethod
    def get_class(injected, original):
        """ generates common class where entries are different"""
        return original.ne(injected)

    def create_scenario_part_output(self, injected, original, cols):
        original = original.reset_index(drop=True)
        injected = injected.reset_index(drop=True)
        return {
            "injected": injected,
            "original": original.copy(),
            "class": self.get_class(injected, original),
            "columns": cols}

    def transform_df(self, df, cols=[0],seed = 100):
        data = df.copy()
        for col in cols:
            data.iloc[:, col], anomaly_infos = self.inject_single(np.array(data.iloc[:, col]),seed = seed)

        return {"full_set": self.create_scenario_part_output(data, df, cols)}