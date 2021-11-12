# generate low rank synthetic data
# we need structure in the data e.g weeks
import numpy as np
import matplotlib.pyplot as plt
from Robust_PCA import R_pca
from evaluation.file_manipulation import get_df_from_file
import pandas as pd

file = "../data/YAHOO/YAHOO.csv"
df = pd.read_csv(file)

D  =np.array(df)

# decimate 20% of data
n1, n2 = D.shape
S = np.random.rand(n1, n2)
#[S < 0.2] = 0
#print(D.shape)
# use R_pca to estimate the degraded data as L + S, where L is low

rpca = R_pca(D)
L, S = rpca.fit(max_iter=100000, iter_print=100)

rpca.plot_fit()
plt.show()

L = L.reshape(-1)
treshhold = 7
#plt.plot(x, label = "injected")
plt.plot(L.reshape(-1), label = "L")
plt.plot(S,label = "S")
plt.legend()
plt.show()
