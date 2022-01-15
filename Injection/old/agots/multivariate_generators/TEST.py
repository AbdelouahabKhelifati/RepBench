from Repair.Screen import screen
from Injection.old.agots.multivariate_generators.multivariate_variance_outlier_generator import \
    MultivariateVarianceOutlierGenerator

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
gen = MultivariateVarianceOutlierGenerator([(3,90)])

ser = pd.Series(np.arange(100)+10)

x = gen.add_outliers(ser)


datafile = "../../../datasets/stock/stock10k.Data"

def RMS( x, y): return np.mean(np.square(x - y[:len(x)])) ** (1 / 2)

def accuracy(truth,dirty):
    def a(repair):
        return 1-RMS(truth[:len(repair)],repair)/(RMS(repair,dirty[:len(repair)])+RMS(truth[:len(repair)],dirty[:len(repair)]))
    return a


series = (pd.read_csv(datafile, names=("timestamp", "Data", "truth")))


series  = series.iloc[:200]
series["Data"] = series["truth"].copy()

onlydataseries = series["Data"]


print(series)
print(series.size)

#repair = screen(series.copy().to_numpy())

gen = MultivariateVarianceOutlierGenerator([(3,50), (100,110) ,( 140,145)] +  [ (i,i+10) for i in range(120,140)],factor=20)

x = gen.add_outliers(onlydataseries)

series["Data"] = series["Data"] + x

rms_dirty = RMS(series["truth"], series["Data"])

repair = screen(series.copy().to_numpy())
rms = RMS(series["truth"],repair)

plt.plot(series["truth"] ,color = 'green' , alpha=0.5)
plt.plot(series["Data"])
plt.plot(repair[:-1])
