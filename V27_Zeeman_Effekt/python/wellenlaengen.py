# wechsle die Working Directory zum Versuchsordner, damit das Python-Script von überall ausgeführt werden kann
import os,pathlib
project_path = pathlib.Path(__file__).absolute().parent.parent
os.chdir(project_path)

# Imports
import numpy as np
from scipy import stats
import uncertainties.unumpy as unp
import json

keys = ['rot','blau_pi','blau_sigma']

# Konstanten
lambda_ = {
    'rot':643.8,
    'blau_pi':480.0,
    'blau_sigma':480.0,
} # nm

n = {
    'rot':1.4567,
    'blau_pi':1.4635,
    'blau_sigma':1.4635
}

d = 4*10**6 # nm
L = 120 # mm

# JSON Datei einlesen
json_file_path = 'data/Ergebnisse.json'
try:
    with open(json_file_path,'r') as json_file:
        Ergebnisse = json.load(json_file)
except FileNotFoundError as err:
    Ergebnisse = {}

for key in keys:
    # Daten einlesen
    Ordnung,delta_s,d_s = np.genfromtxt(f'data/{key}.csv',delimiter=',',skip_header=1,unpack=True)
    delta_s = unp.uarray(delta_s,5)
    d_s = unp.uarray(d_s,5)

    delta_lambda_D = lambda_[key]**2 / (2*d)/np.sqrt(n[key]**2-1)
    delta_lambda_D *= 10**3 # pm

    d_lambda = d_s/delta_s*delta_lambda_D/2

    d_lambda_mean = np.mean(unp.nominal_values(d_lambda))
    d_lambda_mean_err = stats.sem(unp.std_devs(d_lambda))

    # Ergebnisse
    if not key in Ergebnisse:
        Ergebnisse[key] = dict()
    Ergebnisse[key]['delta_lambda_D[pm]'] = delta_lambda_D
    Ergebnisse[key]['d_lambda_mean[pm]'] = d_lambda_mean
    Ergebnisse[key]['d_lambda_mean_err[pm]'] = d_lambda_mean_err

    # Daten speichern
    data = list(zip(Ordnung, unp.nominal_values(delta_s), unp.std_devs(delta_s), unp.nominal_values(d_s), unp.std_devs(d_s), unp.nominal_values(d_lambda), unp.std_devs(d_lambda)))
    np.savetxt(f'data/{key}_result.csv', data, header='Ordnung,delta_s[pixel],d_s[pixel],d_lambda[pm]', comments='', fmt='%i,%i+-%i,%i+-%i,%.5f+-%.5f')

# Ergebnisse als JSON Datei speichern
with open(json_file_path,'w') as json_file:
    json.dump(Ergebnisse, json_file, indent=4)