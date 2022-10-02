from abc import ABC
import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator
import sklearn.metrics as sm


class Estimator(ABC, BaseEstimator):

    uses_labels = False

    def copy(self):
        copy_ = type(self)
        copy_.score_f = self.score_f
        return copy_

    def set_score_f(self,score):
        self.score_f = score

    def scores(self, injected, truth , columns_to_repair, labels , predicted=None , score = None):

        X = injected
        y = truth
        predicted = predicted if predicted is not None else self.repair(X, y,columns_to_repair,labels)
        labels = labels.values if isinstance(labels,pd.DataFrame) else labels

        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        full_weights = np.zeros_like(predicted.values).astype(bool)
        full_weights[:,columns_to_repair] = True
        full_weights[labels] = False
        full_weights_flattened = full_weights.flatten()

        scores_ = {}

        if score is None or score == "mae":
            scores_["mae"] = sm.mean_absolute_error(flatten_y[full_weights_flattened], flatten_predicted[full_weights_flattened])
        if score is None or score == "full_rmse":
            scores_["full_rmse"] = sm.mean_squared_error(flatten_y[full_weights_flattened], flatten_predicted[full_weights_flattened],squared=False)
            scores_["original_rmse"] = sm.mean_squared_error(flatten_y[full_weights_flattened], injected.values.flatten()[full_weights_flattened], squared=False)


        partial_weights = np.invert(np.isclose(X.values, y.values))
        partial_weights[labels] = False
        partial_weights_flattened = partial_weights.flatten() # anomaly_weights

        if score is None or score == "partial_rmse":
            try:
                scores_["partial_rmse"] = sm.mean_squared_error(flatten_y[partial_weights_flattened], flatten_predicted[partial_weights_flattened], squared=False)
                scores_["original_partial_rmse"] = sm.mean_squared_error(flatten_y[partial_weights_flattened], injected.values.flatten()[partial_weights_flattened], squared=False)
            except:
                scores_["partial_rmse"] =  -1
                scores_["original_partial_rmse"] = -1
        from sklearn.feature_selection import mutual_info_regression as mi

        # if score is None or score in ["partial_mutual_info","full_mutual_info"]:
        #
        #     try:
        #         scores_["partial_mutual_info"] = -mi(flatten_predicted[partial_weights_flattened].reshape(-1, 1),flatten_y[partial_weights_flattened],discrete_features=False,n_neighbors=20)[0]
        #         scores_["full_mutual_info"] = -mi(flatten_predicted[full_weights_flattened].reshape(-1, 1),flatten_y[full_weights_flattened],discrete_features=False,n_neighbors=20)[0]
        #     except:
        #         try:
        #             scores_["partial_mutual_info"] = - \
        #             mi(flatten_predicted[partial_weights_flattened].reshape(-1, 1), flatten_y[partial_weights_flattened],
        #                discrete_features=False)[0]
        #             scores_["full_mutual_info"] = - \
        #             mi(flatten_predicted[full_weights_flattened].reshape(-1, 1), flatten_y[full_weights_flattened],
        #                discrete_features=False)[0]
        #         except:
        #             pass
        #         pass

        return scores_

    def mae_score(self, X, y , labels):
        predicted = self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.ones_like(predicted.values).astype(bool)
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_absolute_error(flatten_y[weights], flatten_predicted[weights])
        return score_

    def full_rmse(self, X, y, labels):
        predicted  =self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.ones_like(predicted.values).astype(bool)
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_squared_error(flatten_y[weights], flatten_predicted[weights],squared=False)
        return score_


    def partial_rmse(self, X, y, labels):
        predicted = self.predict(X, y, labels)
        flatten_y = y.values.flatten()
        flatten_predicted = predicted.values.flatten()
        weights = np.invert(np.isclose(X.values,y.values))
        weights[labels] = False
        weights = weights.flatten()
        score_ = sm.mean_squared_error(flatten_y[weights], flatten_predicted[weights],squared=False)
        return score_


    def fit(self, X, y=None):
        raise NotImplementedError(self)


    def repair(self,injected, truth, columns_to_repair , labels=None):
        raise NotImplementedError(self)

    def laybeled_repair(self):
        raise NotImplementedError(self)

    def runt_time_repair(self):
        raise NotImplementedError(self)

    def get_params(self, deep= False):
        return  self.get_fitted_params()

    def get_fitted_params(self, **args):
        raise NotImplementedError(self)

    def suggest_param_range(self, X):
        "parameter ranges used for training depending on data X, data is normalized for training"
        raise NotImplementedError(self)


    @property
    def alg_type(self):
        "e.g for colors in plot"
        raise NotImplementedError(self)

    def algo_name(self):
        raise NotImplementedError(self)


    def addiotnal_plotting_args(self) -> dict:
        return {}

