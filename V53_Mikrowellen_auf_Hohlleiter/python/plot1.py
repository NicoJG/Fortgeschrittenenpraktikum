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
U,A = np.genfromtxt('data/data1.csv',delimiter=',',skip_header=2,unpack=True)

U1 = [U[0],U[1],U[2]]
U2 = [U[3],U[4],U[5]]
U3 = [U[6],U[7],U[8]]
A1 = [A[0],A[1],A[2]]
A2 = [A[3],A[4],A[5]]
A3 = [A[6],A[7],A[8]]


# Ausgleichskurven Funktion (hier Ausgleichsgerade)
def f(x,a,b,c):
    return a*x**2 + b*x +c


# Ausgleichskurve berechnen
params1,pcov1 = curve_fit(f,U1,A1)
params2,pcov2 = curve_fit(f,U2,A2)
params3,pcov3 = curve_fit(f,U3,A3)


# Parameter
a1 = params1[0]
b1 = params1[1]
c1 = params1[2]

a2 = params2[0]
b2 = params2[1]
c2 = params2[2]

a3 = params3[0]
b3 = params3[1]
c3 = params3[2]

# Unsicherheiten
a1_err = np.absolute(pcov1[0][0])**0.5
b1_err = np.absolute(pcov1[1][1])**0.5
c1_err = np.absolute(pcov1[2][2])**0.5

a2_err = np.absolute(pcov2[0][0])**0.5
b2_err = np.absolute(pcov2[1][1])**0.5
c2_err = np.absolute(pcov2[2][2])**0.5

a3_err = np.absolute(pcov3[0][0])**0.5
b3_err = np.absolute(pcov3[1][1])**0.5
c3_err = np.absolute(pcov3[2][2])**0.5

# Werte irgendwie ausgeben lassen
# z.B. mit print, aber besser als JSON Datei abspeichern
print(f'{a1 = :.3f}+-{a1_err:.3f}')
print(f'{b1 = :.3f}+-{b1_err:.3f}')
print(f'{c1 = :.3f}+-{c1_err:.3f}')

print(f'{a2 = :.3f}+-{a2_err:.3f}')
print(f'{b2 = :.3f}+-{b2_err:.3f}')
print(f'{c2 = :.3f}+-{c2_err:.3f}')

print(f'{a3 = :.3f}+-{a3_err:.3f}')
print(f'{b3 = :.3f}+-{b3_err:.3f}')
print(f'{c3 = :.3f}+-{c3_err:.3f}')

# Plot der Ausgleichskurve
x_linspace1 = np.linspace(np.min(U1), np.max(U1), 100)
x_linspace2 = np.linspace(np.min(U2), np.max(U2), 100)
x_linspace3 = np.linspace(np.min(U3), np.max(U3), 100)
plt.plot(x_linspace1, f(x_linspace1,*params1), 'k-', label='Ausgleichskurven')
plt.plot(x_linspace2, f(x_linspace2,*params2), 'k-')
plt.plot(x_linspace3, f(x_linspace3,*params3), 'k-')
# Plot der Daten
plt.plot(U, A, 'ro', label='Daten')

# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$U \:/\: \si{\volt}$')
plt.ylabel(r'$A \:/\: \si{\volt}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend(loc = "upper left")
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_NAME.pdf')

#a1 = -0.008+-inf
#b1 = 1.234+-inf
#c1 = -49.067+-inf
#a2 = -0.006+-inf
#b2 = 1.511+-inf
#c2 = -101.667+-inf
#a3 = -0.008+-inf
#b3 = 3.285+-inf
#c3 = -358.800+-inf
