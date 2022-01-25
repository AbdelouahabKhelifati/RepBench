from copy import deepcopy
from skopt import gp_minimize



#chalenge ts not i.i.d
class BayesianOptimization():
    def __init__(self, clf, param_grid,  n_jobs=-1 , **kargs):
        self.clf = deepcopy(clf) #todo check if this works
        self.n_jobs = n_jobs
        self.set_param_grid(param_grid)
        self.best_params_ = None
        self.best_estimator_ = clf
        self._ParamTuner__name_ = "BayesianOptimization"


    def set_param_grid(self,paramgrid):
        self.param_grid = {}
        for k , v in paramgrid.items():
            self.param_grid[k]  = (min(v),max(v))  if len(v)>2 else v



    def fit(self, X, y , groups = None):
        gp_minimize_result = bayesian_opt(X, y, self.clf, self.param_grid,self.n_jobs)
        self.best_params_ = { k : v for k,v  in zip(self.param_grid.keys(), gp_minimize_result.x) }
        self.clf.__dict__.update(self.best_params_)
        self.best_estimator_ = self.clf.fit(X,y)

# todo sampling
def select_data(data, truth, samples, sample_offset=0):
    return data, truth
    # np.random.seed(20)
    # indexes = np.random.randint(len(data), size=samples, dtype=int)
    # return data.iloc[indexes, :], truth.iloc[indexes, :]
    #

def bayesian_opt(data, truth, model, params_bounds, scoring , samples=-1, n_jobs=-1):
    """  wrap   """
    x = params_bounds.values()

    def f(x):
        params = {k: v for k, v in zip(params_bounds.keys(), x)}
        # for k, v in params.items():
        #     setattr(model, k, v)
        model.__dict__.update(params)

        selected_data, selected_truth = select_data(data, truth, samples)
        model.fit(selected_data ,selected_truth )
        result = -model.score(data, truth)
        return result

    return gp_minimize(f, x, n_jobs=n_jobs,n_calls=20,  n_initial_points=20, n_restarts_optimizer=2, n_points=1000,acq_func='EI')


#
# if __name__ == "__main__":
#     file_name = searchfile("temp.csv")
#     print(file_name)
#     df = get_df_from_file(file_name)[0]
#     b = BaseScenario()
#     results = b.transform_df(df)["full_set"]
#     truth = results["original"]
#     injected = results["injected"]
#
#     # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
#     #     print(injected.corr())
#
#     try:
#         truth.drop("class", axis=1)
#         injected.drop("class", axis=1)
#         df = df.drop("class", axis=1)
#     except:
#         pass
#
#     param_grid = {"threshold": list(np.arange(0.5, 3., 0.2)),
#                   "n_components": [1,2],
#                   "delta": [0.5 ** i for i in range(11)],
#                   "component_method" : [  "TruncatedSVD", "svd"   ],
#                     "interpolate_anomalies": [ False,True]
#
#     }
#
#     default_params = {"cols": [0,1,2,3,4,5,6,7,8,9]}
#
#     bayesian_params = bayesian_opt(injected, truth, Robust_PCA_estimator, default_params, param_grid, samples=-1)
#     model_b = Robust_PCA_estimator(**bayesian_params)
#     d, t = select_data(injected, truth, samples=1000)
#     model_b.fit(d)
#     result_b = pd.DataFrame(model_b.predict(injected))
#     truth.plot()
#     plt.show()
#     result_b.plot()
#     plt.show()
#     injected.plot()
#     plt.show()
#     reduced = pd.DataFrame(model_b.reduce(injected))
#     reduced.plot()
#     plt.show()
#
