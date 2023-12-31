import json

from django.db import models
import pandas as pd

from RepBenchWeb.ts_manager.HighchartsMapper import map_repair_data
from injection.injected_data_container import InjectedDataContainer
from recommendation.recommend import get_recommendation


class DataSet(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=True)
    dataframe = models.JSONField(null=False, blank=False)
    ref_url = models.CharField(max_length=200, null=True, blank=True)
    url_text = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    additional_info = models.JSONField(blank=False)

    def __str__(self):
        return self.title

    @property
    def df(self):
        data_frame = pd.read_json(self.dataframe)
        data_frame.columns = [c if isinstance(c, int) else c.replace(" ", "") for c in data_frame.columns]
        return data_frame

    def get_info(self):
        shape = None
        additional_info = json.loads(str(self.additional_info))

        if shape in additional_info:
            shape = self.additional_info["shape"]
        else:
            shape = tuple(self.df.shape)
            additional_info["shape"] = shape
        self.additional_info = json.dumps(additional_info)

        n, m = shape
        return {
            "values": n * m,
            "ts_nbr": m,
            "title": self.title,
            "ref_url": self.ref_url,
            "url_text": self.url_text,
            "description": self.description,
        }

    def get_catch_22_features(self):
        additional_info = json.loads(self.additional_info)
        # additional_info["catch22"] = {k if isinstance(k, int) else k.replace(" ", "") : v for k, v in additional_info["catch22"].items()}
        #
        # self.additional_info = json.dumps(additional_info)
        # self.save()
        # print("save")
        return {"catch22": additional_info["catch22"],
                "catch22_min_max": additional_info["catch22_min_max"]
                }


score_map = {"mae": "MAE",
             "mse": "MSE",
             "rmse": "RMSE",
             "partial_rmse": "RMSE on Anomaly"
             }

class InjectedContainer(models.Model):
    title = models.CharField(max_length=64, null=False, blank=False, unique=False)
    injectedContainer_json = models.JSONField(null=False, blank=False)
    description = models.TextField(max_length=200, null=True, blank=True)
    info = models.JSONField(blank=False, null=True)  # orginal data titel
    original_data_set = models.CharField(max_length=100, null=True)


    recommendation = models.JSONField(blank=False, null=True)  # recomendation for the model

    @property
    def injected_container(self):
        injected_container_: InjectedDataContainer = InjectedDataContainer.from_json(self.injectedContainer_json)
        return injected_container_

    def get_info(self):
        injectedDataContainer: InjectedDataContainer = self.injected_container
        n, m = injectedDataContainer.injected.shape
        a_rates = injectedDataContainer.get_a_rate_per_col()
        scores = injectedDataContainer.original_scores
        scores = {score_map[k]: round(v, 4) for k, v in scores.items() if k in score_map.keys()}
        return {
            "length": n,
            "values": n * m,
            "ts_nbr": m,
            "title": self.title,
            "description": self.description,
            "anomaly_rates": a_rates,
            "injected_rates": {ts: r for ts, r in a_rates.items() if r > 0},
            "scores": scores,
            "original_data_set": self.original_data_set
        }

    def __str__(self):
        return self.title

    def recommendation_context(self):
        if True or self.recommendation is None:
            # recommendation_dict = json.loads(self.recommendation)
            original_data = DataSet.objects.get(title=self.original_data_set)
            df_original = original_data.df
            injected_data_container  = self.injected_container
            truth = injected_data_container.truth
            recommendation_results = get_recommendation(injected_data_container)
            repairs = recommendation_results["alg_repairs"]

            repair_converted ={}
            for alg_name,repair in repairs.items():
                mean, std = truth.mean(), truth.std()  # injected.mean(), injected.std()
                repair_norm = (repair - mean) / std
                # normalize truth data w.r.t injected series

                repair_converted[alg_name] = map_repair_data(repair_norm, injected_data_container, alg_name=alg_name, links=None, df_original= truth)
            recommendation_results["alg_repairs"] = repair_converted

            self.recommendation = json.dumps(recommendation_results)
            self.save()
        else:
            recommendation_results = json.loads(self.recommendation)
        return  recommendation_results

""" how to delete a model in shell

python3 manage.py shell

from RepBenchWeb.models import InjectedContainer

Select the title to delete
InjectedContainer.objects.all()

InjectedContainer.objects.filter(title="test").delete()
"""

""" how to add a new field without reinitlalizing the whole table
https://stackoverflow.com/questions/24311993/how-to-add-a-new-field-to-a-model-with-new-django-migrations
"""
