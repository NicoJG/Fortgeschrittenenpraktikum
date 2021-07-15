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
from scipy.signal import argrelmax

t,M = np.genfromtxt('data/T2_Messung_MG_on_2.csv', delimiter=',', skip_header=1, unpack=True)
mask = (t >= 0)
t = t[mask]
M = M[mask]

M_max = argrelmax(M,order = 10)[0]
M_max = np.append(M_max,0)

# Ausgleichskurven Funktion (hier Ausgleichsgerade)
def f(t,M0,M1,T2):
    return M0 * np.exp(- t / T2) + M1
# oder als Lambda Funktion
#f = lambda x,a,b: a*x + b

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,t[M_max],M[M_max])

# Parameter
M0 = params[0]
M1 = params[1]
T2 = params[2]


# Unsicherheiten
M0_err = np.absolute(pcov[0][0])**0.5
M1_err = np.absolute(pcov[1][1])**0.5
T2_err = np.absolute(pcov[2][2])**0.5

# Werte irgendwie ausgeben lassen
# z.B. mit print, aber besser als JSON Datei abspeichern


#print(f'M0 = {M0}+-{M0_err}')
#print(f'T2 = {T2}+-{T2_err}')
#print(f'M1 = {M1}+-{M1_err}')


# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(t[M_max]), np.max(t[M_max]), 100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Exponentielle Ausgleichskurve')
# Plot der Daten
plt.plot(t, M, 'b-', linewidth = 0.5, label='Spannung')
plt.plot(t[M_max], M[M_max], 'r.', label='Maxima der Spannung')
# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_T2.pdf')

# M0 = 0.9071261549408218+-0.04213233913418248
# M1 = 0.07968654395684359+-0.04720177614981682
# T2 = 1.6960956968852023+-0.1623201369753522

plt.clf()

tau,A = np.genfromtxt('data/T1_Messung.csv', delimiter=',', skip_header=2, unpack=True)

tau = tau * 10**-3 
A = A * 10**-3

# Ausgleichskurven Funktion (hier Ausgleichsgerade)
def f(tau,U0,U1,T1):
    return U0 * np.exp(- tau / T1) + U1
# oder als Lambda Funktion
#f = lambda x,a,b: a*x + b

# Ausgleichskurve berechnen
params,pcov = curve_fit(f,tau,A,p0=(-1,1,0.5))

# Parameter
U0 = params[0]
U1 = params[1]
T1 = params[2]


# Unsicherheiten
U0_err = np.absolute(pcov[0][0])**0.5
U1_err = np.absolute(pcov[1][1])**0.5
T1_err = np.absolute(pcov[2][2])**0.5

# Werte irgendwie ausgeben lassen
# z.B. mit print, aber besser als JSON Datei abspeichern

#print(f'U0 = {U0}+-{U0_err}')
#print(f'U1 = {U1}+-{U1_err}')
#print(f'T1 = {T1}+-{T1_err}')

# Plot der Ausgleichskurve
x_linspace = np.linspace(np.min(tau), np.max(tau), 100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Exponentielle Ausgleichskurve')
# Plot der Daten
plt.plot(tau, A, 'ro', label='Spannung')
plt.semilogx()
# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$t \:/\: \si{\second}$')
plt.ylabel(r'$U \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_T1.pdf')

#U0 = -1.5452811230393828+-0.0337661937832072
#U1 = 0.5347194520934632+-0.03339023242461304
#T1 = 1.9259873137661128+-0.11529234563368615