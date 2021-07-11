# wechsle die Working Directory zum Versuchsordner, damit das Python-Script von überall ausgeführt werden kann
import os,pathlib
project_path = pathlib.Path(__file__).absolute().parent.parent
os.chdir(project_path)
# benutze die matplotlibrc und header-matplotlib.tex Dateien aus dem default Ordner
os.environ['MATPLOTLIBRC'] = str(project_path.parent/'default'/'python'/'matplotlibrc')
os.environ['TEXINPUTS'] =  str(project_path.parent/'default'/'python')+':'

# Imports
import json
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit, root
from uncertainties import ufloat

# Ergebnisse JSON Datei einlesen (am Anfang)
json_file_path = 'data/Ergebnisse.json'
try:
    with open(json_file_path,'r') as json_file:
        Ergebnisse = json.load(json_file)
except FileNotFoundError as err:
    Ergebnisse = {}

# Reflektivitätsscan:
angle_refl, intensity_refl = np.genfromtxt('data/Omega2ThetaScan1.UXD', unpack=True)
# Diffuser Scan
angle_diff, intensity_diff = np.genfromtxt('data/Omega2ThetaScan2.UXD', unpack=True)

if (angle_refl!=angle_diff).any():
    print('Der Diffuse Scan und der Reflektivitätsscan passen nicht zueinander!')

angle = angle_refl
intensity = intensity_refl - intensity_diff

# Reflektivitäts Scan Plotten
print('Plot: Mess-Scan...')
plt.plot(angle_refl, intensity_refl, '-', label='Reflektivitätsscan')
plt.plot(angle_diff, intensity_diff, '-', label='Diffuser Scan')
plt.plot(angle, intensity, '-', label='korrigierter Reflektivitätsscan')
plt.xlabel(r'$\alpha \:/\: \si{\degree}$')
plt.ylabel(r'$I \:/\: ???$')
plt.xlim(0,2.0)
plt.yscale('log')
plt.legend()
plt.tight_layout(pad=0.15, h_pad=1.08, w_pad=1.08)
plt.savefig('build/plot_messung.pdf')
# plt.show()
plt.clf()


# Ergebnisse als JSON Datei speichern (am Ende)
with open(json_file_path,'w') as json_file:
    json.dump(Ergebnisse, json_file, indent=4)