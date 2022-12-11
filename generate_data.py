import logging

import pandas as pd
from ctgan import CTGAN
from os.path import exists
from copulas.multivariate import GaussianMultivariate
from videofuzzer.pipeline.pipeline import Pipeline
from videofuzzer.json_unflatten import get_data
from videofuzzer.json_flatten import flatten
import csv

dat = pd.read_csv('./project/media/new_file.csv')

logging.basicConfig(format='[%(asctime)s] %(process)s %(filename)s:%(lineno)d %(levelname)s - %(message)s',
                            level=logging.INFO)

ctgan = CTGAN(epochs=100, batch_size=100, cuda=True)
if exists('ctgan-1000.pkl'):
    ctgan = CTGAN.load('ctgan-1000.pkl')
else:
    ctgan.fit(dat)
    ctgan.save('ctgan-1000.pkl')

# Create synthetic data
synthetic_data = None
if exists('ctgan-100.csv'):
    synthetic_data = pd.read_csv('ctgan-100.csv')
else:
    synthetic_data = ctgan.sample(100)
    synthetic_data.to_csv('ctgan-100.csv')



dist = GaussianMultivariate()
if exists('copula.pkl'):
    dist = GaussianMultivariate.load('copula.pkl')
else:
    dist.fit(dat)
    dist.save('copula.pkl')

gcopuladat = None
if exists('copula.csv'):
    gcopuladat = pd.read_csv('copula.csv')
else:
    gcopuladat = dist.sample(100)
    gcopuladat.to_csv('copula.csv')




pipeline = Pipeline()

gaussian_results = []
ctgan_results = []

for i in range(10):
    result = get_data(synthetic_data.iloc[i].values.tolist())
    ctgan_results.append(result)
cr = pipeline.apply(data_dict=ctgan_results, ncpus=32)
crlist = []
for i in cr:
    crlist.append(flatten(i))

with open("ctgan-clean.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(crlist)




for i in range(10):
    result = get_data(gcopuladat.iloc[i].values.tolist())
    gaussian_results.append(result)

gr = pipeline.apply(data_dict=gaussian_results, ncpus=32)

grlist = []
for i in gr:
    grlist.append(flatten(i))


with open("copula-clean.csv", "w+") as my_csv:
    csvWriter = csv.writer(my_csv, delimiter=',')
    csvWriter.writerows(grlist)
