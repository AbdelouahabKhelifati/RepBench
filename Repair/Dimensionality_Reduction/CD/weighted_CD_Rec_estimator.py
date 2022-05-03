# import pandas as pd
# from matplotlib import pyplot as plt
#
# from Repair.Algorithms_Config import CDREC
# from Repair.Dimensionality_Reduction.CDrec.weighted_cedomposition import weighted_centroid_decomposition
# from Repair.Dimensionality_Reduction.Dimensionality_Reduction_Estimator import DimensionalityReductionEstimator
# from Repair.Robust_PCA.loss import HuberLoss
# import numpy as np
#
#
# class weighted_CD_Rec_estimator(DimensionalityReductionEstimator):
#
#     def _reduce(self, matrix,truncation):
#         assert matrix[:,0].std() < 1.01 and matrix[:,0].mean() < 0.01 and matrix[:,0].mean() > -0.01
#
#         self.loss = HuberLoss(self.delta)
#         X = matrix.copy()
#         vectorized_loss = np.vectorize(self.loss.__call__)
#         vectorized_weights = np.vectorize(self.loss.weight)
#
#         n_samples, n_features = X.shape
#
#         self.weights_ = 1. / n_samples * np.ones(n_samples)
#         self.errors_ = [np.inf]
#         self.n_iterations_ = 0
#         not_done_yet = True
#         while not_done_yet:
#             self.mean_ = np.average(X, axis=0, weights=self.weights_)
#             X_centered = X - self.mean_
#
#             L, R, Z = weighted_centroid_decomposition(X_centered * 1, truncation=truncation, weights=self.weights_)
#             self.L = L
#             self.R = R
#             self.Z = Z
#             reduced = np.matmul(np.matmul(X_centered,R), R.T)
#             assert reduced.shape ==  X.shape
#             diff = X_centered - reduced
#             errors_raw = np.linalg.norm(diff, axis=1)
#             errors_loss = vectorized_loss(errors_raw)
#
#             self.weights_ = vectorized_weights(errors_raw)
#             self.n_iterations_ += 1
#             old_total_error = self.errors_[-1]
#             total_error = errors_loss.sum()
#
#             if not np.equal(total_error, 0.):
#                 rel_error = abs(total_error - old_total_error) / abs(total_error)
#             else:
#                 rel_error = 0.
#
#             self.errors_.append(total_error)
#             not_done_yet = self.n_iterations_ < self.max_iter
#
#         self.weights = self.weights_
#         return np.matmul(L, R.T) + self.mean_
#
#     @property
#     def alg_type(self):
#         return "weighted"+CDREC
#
#     def algo_name(self):
#         return "weighted_CDREC"  # ({self.n_components},{self.delta},{round(self.threshold,2)})'