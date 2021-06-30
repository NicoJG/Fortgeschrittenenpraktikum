# wechsle die Working Directory zum Versuchsordner, damit das Python-Script von überall ausgeführt werden kann
import os,pathlib
project_path = pathlib.Path(__file__).absolute().parent.parent
os.chdir(project_path)

# Imports
import numpy as np
from scipy import stats
import uncertainties.unumpy as unp
from uncertainties import ufloat
from uncertainties.unumpy import std_devs as stds , nominal_values as noms
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

I_B = {
    'rot': 5.0,
    'blau_pi': 5.0,
    'blau_sigma': 3.24
} # A

d = 4*10**6 # nm
L = 120 # mm

h = 6.62607015*10**(-34) # J Hz^-1
c_licht = 299792458 # m s^-1
mu_B = 9.2740100783*10**(-24) # J T^-1

# JSON Datei einlesen
json_file_path = 'data/Ergebnisse.json'
try:
    with open(json_file_path,'r') as json_file:
        Ergebnisse = json.load(json_file)
except FileNotFoundError as err:
    Ergebnisse = {}

# für B-Feld
def B_Ausgleichskurve(I,a,b,c):
    return (a*I**2+b*I+c)*10**(-3) # T

a = ufloat(Ergebnisse['Magnet']['a'], Ergebnisse['Magnet']['a_err'])
b = ufloat(Ergebnisse['Magnet']['b'], Ergebnisse['Magnet']['b_err'])
c = ufloat(Ergebnisse['Magnet']['c'], Ergebnisse['Magnet']['c_err'])

for key in keys:
    # Daten einlesen
    Ordnung,delta_s,d_s = np.genfromtxt(f'data/{key}.csv',delimiter=',',skip_header=1,unpack=True)
    delta_s = unp.uarray(delta_s,5)
    d_s = unp.uarray(d_s,5)

    # wellenlängenaufspaltung
    delta_lambda_D = lambda_[key]**2 / (2*d)/np.sqrt(n[key]**2-1)
    delta_lambda_D *= 10**3 # pm

    d_lambda = d_s/delta_s*delta_lambda_D/2

    d_lambda_mean = d_lambda.sum()/len(d_lambda)

    # Ergebnisse
    if not key in Ergebnisse:
        Ergebnisse[key] = dict()
    Ergebnisse[key]['delta_lambda_D[pm]'] = delta_lambda_D
    Ergebnisse[key]['d_lambda_mean[pm]'] = d_lambda_mean.n
    Ergebnisse[key]['d_lambda_mean_err[pm]'] = d_lambda_mean.s

    # Lande Faktoren
    B = B_Ausgleichskurve(I_B[key],a,b,c)

    g = d_lambda_mean*10**(-12)*h*c_licht/(mu_B*B*(lambda_[key]*10**(-9))**2)

    Ergebnisse[key]['g'] = g.n
    Ergebnisse[key]['g_err'] = g.s

    # Daten speichern
    data = list(zip(Ordnung, noms(delta_s), stds(delta_s), noms(d_s), stds(d_s), noms(d_lambda), stds(d_lambda)))
    np.savetxt(f'data/{key}_result.csv', data, header='Ordnung,delta_s[pixel],d_s[pixel],d_lambda[pm]', comments='', fmt='%i,%i+-%i,%i+-%i,%.2f+-%.2f')

# Ergebnisse als JSON Datei speichern
with open(json_file_path,'w') as json_file:
    json.dump(Ergebnisse, json_file, indent=4)