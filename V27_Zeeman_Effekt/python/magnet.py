# wechsle die Working Directory zum Versuchsordner, damit das Python-Script von überall ausgeführt werden kann
import os,pathlib
project_path = pathlib.Path(__file__).absolute().parent.parent
os.chdir(project_path)
# benutze die matplotlibrc und header-matplotlib.tex Dateien aus dem default Ordner
os.environ['MATPLOTLIBRC'] = str(project_path.parent/'default'/'python'/'matplotlibrc')
os.environ['TEXINPUTS'] =  str(project_path.parent/'default'/'python')+':'

# Imports
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import json

# JSON Datei einlesen (am Anfang)
json_file_path = 'data/Ergebnisse.json'
try:
    with open(json_file_path,'r') as json_file:
        Ergebnisse = json.load(json_file)
except FileNotFoundError as err:
    # Falls Datei noch nicht existiert, leere Dictionary erstellen
    # Allerdings sollte der Ordner 'data' schon existieren
    Ergebnisse = {}

# Daten einlesen
I,B = np.genfromtxt('data/magnet.csv',delimiter=',',skip_header=1,unpack=True)

# Ausgleichsrechnungs-Funktion
def f(x,a,b):
    return a*x+b

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,I,B)
# Parameter
a = params[0]
b = params[1]
# Unsicherheiten
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5

# berechnete Werte in der Dictionary speichern (am besten in Kategorien)
if not 'Magnet' in Ergebnisse:
    Ergebnisse['Magnet'] = {}
Ergebnisse['Magnet']['a'] = f'{a:.5f}'
Ergebnisse['Magnet']['b'] = f'{b:.5f}'
Ergebnisse['Magnet']['a_err'] = f'{a_err:.5f}'
Ergebnisse['Magnet']['b_err'] = f'{b_err:.5f}'

# Plotten
# Plot der Ausgleichskurve
I_linspace = np.linspace(np.min(I), np.max(I), 100)
plt.plot(I_linspace, f(I_linspace,*params), 'k-', label='Ausgleichsgerade')
# Plot der Daten
plt.plot(I,B,'ro',label='Messwerte')

plt.xlabel(r'$I \:/\: A$')
plt.ylabel(r'$B \:/\: mT$')

plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_magnet.pdf')

# Ergebnisse als JSON Datei speichern
with open(json_file_path,'w') as json_file:
    json.dump(Ergebnisse, json_file, indent=4)