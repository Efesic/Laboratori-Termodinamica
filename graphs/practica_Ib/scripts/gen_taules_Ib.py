import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit


df = pd.read_excel('graphs/practica_Ib/dades_Ib.xlsx',usecols=(0,1,2,3,4,5,6,7,8,9),header=None)
R_0 = 49.1
alpha = 0.0048
#Temperatura ambient
T_amb_list = df.iloc[:,3].dropna().tolist()
T_amb = np.mean(T_amb_list) + 273.15
u_T_amb = np.sqrt(0.01**2 + np.std(T_amb_list,ddof=1)**2)
print('La temperatura ambient del laboratori és: ',T_amb, 'amb un error de ',u_T_amb)

# ----------------TAULA DC ----------------------

#Calculem la resistencia R
u_V = 0.1 #V
u_I =0.1*10**(-3) #A
V = df.iloc[:,4].dropna().tolist() #V
I = df.iloc[:,5].dropna().tolist() #mA
R = np.array(V[1:])/(np.array(I[1:])*10**(-3)) - 0.8 #Ohm
u_R = np.sqrt((u_V*np.array(I[1:])**(-1))**2 +(u_I*np.array(V[1:])*np.array(I[1:])**(-2))**2)

#Càlcul de temperatures
T = (-1+R/R_0)/alpha + T_amb + 273.15
DT = (-1+R/R_0)/alpha
u_T = np.sqrt((u_R/(alpha*R_0))**2 + (u_T_amb)**2)

#Càlcul potència elèctrica
P_el = np.array(V[1:])*np.array(I[1:])*10**(-3)
u_P_el = np.sqrt((u_I*np.array(V[1:]))**2+(u_V*np.array(I[1:])*10**(-3))**2)
print()
print('R,T,P')
print('TAULA DC')
for i in range(0,len(R)):
    print(f'${round(R[i],3)} \pm {round(u_R[i],3)}$ & ${round(T[i],2)} \pm {round(u_T[i],2)}$ & ${round(P_el[i]*100,2)} \pm {round(u_P_el[i]*100,2)}$ \\\ ')

print()
# ----------------TAULA AC ----------------------
#Calculem la resistencia R
u_V = 0.1 #V
u_I =0.1*10**(-3) #A
V = df.iloc[:,7].dropna().tolist() #V
I = df.iloc[:,8].dropna().tolist() #mA
R = np.array(V)/(np.array(I)*10**(-3)) - 0.8 #Ohm
u_R = np.sqrt((u_V*np.array(I)**(-1))**2 +(u_I*np.array(V)*np.array(I)**(-2))**2)

#Càlcul de temperatures
T = (-1+R/R_0)/alpha + T_amb + 273.15
DT = (-1+R/R_0)/alpha
u_T = np.sqrt((u_R/(alpha*R_0))**2 + (u_T_amb)**2)

#Càlcul potència elèctrica
P_el = np.array(V)*np.array(I)*10**(-3)
u_P_el = np.sqrt((u_I*np.array(V))**2+(u_V*np.array(I)*10**(-3))**2)
print()
print('TAULA AC')
for i in range(0,len(R)):
    print(f'${round(R[i]*1000,1)} \pm {round(u_R[i]*1000,1)}$ & ${round(T[i],2)}$ & ${round(P_el[i]*10,2)} \pm {round(u_P_el[i]*10,2)}$ \\\ '.replace('.', ','))

