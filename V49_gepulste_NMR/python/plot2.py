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

t,A1,A2 = np.genfromtxt('data/G_Messung.csv',delimiter=',',skip_header=2,unpack=True)

# Plot der Daten
plt.plot(t, A1, 'r-', label='Realteil')
plt.plot(t, A2, 'b-', linewidth = 0.5, label='Imaginärteil')
# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$A \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_Diff.pdf')

plt.clf()

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
tau, A3 = np.genfromtxt('data/Diffusion.csv',delimiter=',',skip_header=2,unpack=True)

tau = tau * 10**-3
A3 = A3 * 10**-3

plt.plot(tau ** 3, np.log(A3) - tau/1.696, 'ro', label='Daten')

# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$\tau^3 \:/\: \si{\second\cubed}$')
plt.ylabel(r'$\ln{A} - \frac{\tau}{T_2} \:/\: \ln{\si{\volt}}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_Diff2.pdf')

plt.clf()

# Ausgleichskurven Funktion (hier Ausgleichsgerade)
def f(tau,a,b,c):
    return (a * np.exp(-2*tau/1.696 ) * np.exp(-tau**3 / b) + c)

# a = M0
# b = TD

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,tau,A3,p0=(1,40,0.00001))

# Parameter
a = params[0]
b = params[1]
c = params[2]


# Unsicherheiten
a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5
c_err = np.absolute(pcov[2][2])**0.5

# Werte irgendwie ausgeben lassen
# z.B. mit print, aber besser als JSON Datei abspeichern
print(f'M0 = {a}+-{a_err}')
print(f'TD = {b}+-{b_err}')
print(f'M1 = {c}+-{c_err}')

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(tau), np.max(tau), 100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')
# Plot der Daten
plt.plot(tau, A3, 'ro', label='Daten')

# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$\tau \:/\: \si{\second}$')
plt.ylabel(r'$A \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_Diff3.pdf')