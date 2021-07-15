# Erstelle aus gegebnen Daten eine Ausgleichskurve
# Und Plotte diese Kurve + die Daten

# wechsle die Working Directory zum Versuchsordner, damit das Python-Script von überall ausgeführt werden kann
import os,pathlib
project_path = pathlib.Path(__file__).absolute().parent.parent
os.chdir(project_path)
# benutze die matplotlibrc und header-matplotlib.tex Dateien aus dem default Ordner
os.environ['MATPLOTLIBRC'] = str(project_path.parent/'default'/'python'/'matplotlibrc')
os.environ['TEXINPUTS'] =  str(project_path.parent/'default'/'python')+':'

# Imports
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# Daten einlesen
x,y = np.genfromtxt('data/T2_Messung_MG_off.csv',delimiter=',',skip_header=2,unpack=True)

# Plot der Daten
plt.plot(x, y, 'b-', linewidth = 0.5, label='Spannung')

# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_mgoff.pdf')