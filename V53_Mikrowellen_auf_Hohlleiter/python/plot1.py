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
#print(f'{a1 = :.3f}+-{a1_err:.3f}')
#print(f'{b1 = :.3f}+-{b1_err:.3f}')
#print(f'{c1 = :.3f}+-{c1_err:.3f}')
#
#print(f'{a2 = :.3f}+-{a2_err:.3f}')
#print(f'{b2 = :.3f}+-{b2_err:.3f}')
#print(f'{c2 = :.3f}+-{c2_err:.3f}')
#
#print(f'{a3 = :.3f}+-{a3_err:.3f}')
#print(f'{b3 = :.3f}+-{b3_err:.3f}')
#print(f'{c3 = :.3f}+-{c3_err:.3f}')

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
plt.savefig('build/plot_moden.pdf')

#a1 = -0.008+-inf
#b1 = 1.234+-inf
#c1 = -49.067+-inf
#a2 = -0.006+-inf
#b2 = 1.511+-inf
#c2 = -101.667+-inf
#a3 = -0.008+-inf
#b3 = 3.285+-inf
#c3 = -358.800+-inf

plt.clf()


V1 = 211
V0 = 220
V2 = 235

F1 = 9005
F0 = 9028
F2 = 9053

A = (F2 * 10**3 - F1* 10**3)/(V2 - V1)
print("A:", A) #Hz/V

B = (F2 - F1) * 10**3
print("B:", B) #Hz

#A: 2000.0
#B: 48000

c = 3*10**8 #m/s
lambda_h = 50.4 * 10**-3 #meter
a = 22.8 * 10**-3 #meter

fr = c * np.sqrt((1/(lambda_h))**2 + (1/(2 * a))**2)
#print("fr:", fr)

# Ausgleichskurven Funktion (hier Ausgleichsgerade)
def f(x,a,b,c):
    return a*x**2 + b*x +c

d,D = np.genfromtxt('data/dämpfung.csv',delimiter=',',skip_header=2,unpack=True)
d_t = [0, 1.0, 1.4, 1.75, 2.0, 2.3]
D_neu = D + 12.1

params,pcov = curve_fit(f,d_t,D)

a = params[0]
b = params[1]
c = params[2]

a_err = np.absolute(pcov[0][0])**0.5
b_err = np.absolute(pcov[1][1])**0.5
c_err = np.absolute(pcov[2][2])**0.5

#print(f'{a = :.3f}+-{a_err:.3f}')
#print(f'{b = :.3f}+-{b_err:.3f}')
#print(f'{c = :.3f}+-{c_err:.3f}')

x_linspace = np.linspace(0, 5, 100)
plt.plot(x_linspace, f(x_linspace,*params), 'k-', label='Ausgleichskurve')

plt.plot(d, D, 'ro', label='Dämpfung')
plt.plot(d, D_neu, 'go', label='Korrigierete Dämpfung')
plt.plot(d_t,D, 'bo', label='Theorie-Dämpfung')

#a = 1.749+-0.134
#b = 0.403+-0.316
#c = -0.031+-0.173

# Achsenbeschriftung mit LaTeX (nur wenn matplotlibrc benutzt wird)
plt.xlabel(r'$d \:/\: \si{\milli\meter}$')
plt.ylabel(r'$D \:/\: \si{\decibel}$')

# in matplotlibrc leider (noch) nicht möglich
plt.legend()
plt.tight_layout(pad=0, h_pad=1.08, w_pad=1.08)

# Plot als PDF speichern
plt.savefig('build/plot_dämpfung.pdf')

plt.clf()

d1 = 63.5 * 10**-3
d2 = 61.8 * 10**-3
diff = d1 - d2
lambda_h2 = 2 * (90.7 - 67.0) * 10**-3
#print("Lambda:", lambda_h2)

S1 = np.sqrt(  1 + 1/( (np.sin(np.pi * diff/lambda_h2)  )**2   )          )
S2 = lambda_h2/(np.pi * diff)

#print("S_genau:", S1)
#print("S_näh:", S2)

#Lambda: 0.047400000000000005
#S_genau: 8.950076197328022
#S_näh: 8.875228591242163

S3 = 10 ** (23/20)
print("S_3", S3)
#S_3 14.12537544622754