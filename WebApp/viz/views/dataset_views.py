import json
import numpy as np
import pandas as pd
from django.shortcuts import render
from django.views import View

from WebApp.viz.views import data_loader
import WebApp.viz.datasetsConfig as datasetsConfig
from WebApp.viz.models import DataSet, InjectedContainer


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return round(float(obj), 3)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, float):
            return round(obj, 3)
        if isinstance(obj,np.nan):
            return None

        return json.JSONEncoder.default(self, obj)


class DatasetView(View):
    default_nbr_of_ts_to_display = 5
    template = 'displayDataset.html'
    encoder = NpEncoder
    data_fetch_url_name = "get_data"
    load_data_container = data_loader.load_data_container

    def data_set_info_context(self, setname):
        dataSet = DataSet.objects.get(title=setname)
        df = dataSet.df
        corr = df.corr().round(3)
        correlation_html = df.corr().round(3).to_html(classes=["table table-sm table-dark"],
                                                      table_id='correlation_table')
        corr_data = []
        for i, row in enumerate(corr.values):
            for j, v in enumerate(row):
                corr_data.append([i, j, v])
        columns = df.columns.tolist()

        context = {"correlation_html": correlation_html}

        context["data_info"] = dataSet.get_info()
        context["columns"] = columns
        context["corr_data"] = corr_data
        context.update(dataSet.get_catch_22_features())
        return context

    def data_set_default_context(self, request, setname=datasetsConfig.default_set):
        data_container = data_loader.load_data_container(setname)
        df = data_container.original_data
        context = {"setname": setname}
        context["viz"] = int(request.GET.get("viz", self.default_nbr_of_ts_to_display))
        context["data_fetch_url_name"] = self.data_fetch_url_name
        return context, df

    def get(self, request, setname=datasetsConfig.default_set):
        context, df = self.data_set_default_context(request, setname)
        context.update(self.data_set_info_context(setname))
        return render(request, self.template, context=context)


def sliders_view(request,setname="BAFU"):
    template = "sub/catch22sliders.html"
    dataSet = DataSet.objects.get(title=setname)
    context =   dataSet.get_catch_22_features()
    return render(request, template,context)


def display_datasets(request=None):
    context = {"datasets": {dataSet.title: dataSet.get_info()
                            for dataSet in DataSet.objects.all()}}

    context["syntheticDatasets"] = {dataSet.title: dataSet.get_info()
                                    for dataSet in InjectedContainer.objects.all() if dataSet.title is not None and dataSet.title != ""}
    return render(request, 'data_set_options/displayDatasets.html', context=context)
