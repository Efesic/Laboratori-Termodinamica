import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
matplotlib.rcParams.update({'font.size': 20})

df = pd.read_excel('graphs/practica_Ib/dades_Ib.xlsx',usecols=(0,1,2,3),header=None)
R_0 = 49.1 #por alguna razón debe ser el doble
u_R_0 = 0.1
alpha = 0.0048
rad_0 = 0.21
u_rad_0 = 0.01
#Temperatura ambient
T_amb_list = df.iloc[:,3].dropna().tolist()
T_amb = np.mean(T_amb_list) + 273.15
u_T_amb = np.sqrt(0.01**2 + np.std(T_amb_list,ddof=1)**2)
print('La temperatura ambient del laboratori és: ',T_amb, 'amb un error de ',u_T_amb)
#Calculem la resistencia R
u_V = 0.1 #V
u_I =0.1*10**(-3) #A
V = df.iloc[:,0].dropna().tolist() #V
I = df.iloc[:,1].dropna().tolist() #mA
rad = df.iloc[:,2].dropna().tolist()
R = np.array(V[1:])/(np.array(I[1:])*10**(-3)) - 0.8 #Ohm
u_R = np.sqrt((u_V*np.array(I[1:])**(-1))**2 +(u_I*np.array(V[1:])*np.array(I[1:])**(-2))**2)

#Càlcul de temperatures
T = (-1+R/R_0)/alpha + T_amb + 273.15
DT = (-1+R/R_0)/alpha
u_T = np.sqrt((u_R/(alpha*R_0))**2 + (u_T_amb)**2)

#Càlcul potència elèctrica

P_el = np.array(V[1:])*np.array(I[1:])*10**(-3)
u_P_el = np.sqrt((u_I*np.array(V[1:]))**2+(u_V*np.array(I[1:])*10**(-3))**2)
# R vs P - Si solo hubiera convección, P/I^2 tiene cendria comportamiento lineal con Delta T, con R0 como ordenada

plt.figure(figsize=(8,6))
plt.errorbar(R,P_el,xerr=u_R,yerr=u_P_el,marker='D',linestyle='',color='darkblue',label='Punts experimentals',capsize=5,elinewidth=0.7)
plt.xlabel('$R$ [$\Omega$]')
plt.ylabel('$P_{e}$ [W]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/P_vs R',dpi=300)

#Comprovació de R_0
def model(x,m,b):
    return m*x+b
p = []
r = []
for i in range(0,5):
    p.append(P_el[i])
    r.append(R[i])

u_p = np.sqrt((u_I*np.array(V[1:6]))**2+(u_V*np.array(I[1:6])*10**(-3))**2)
u_r = np.sqrt((u_V*np.array(I[1:6])**(-1))**2 +(u_I*np.array(V[1:6])*np.array(I[1:6])**(-2))**2)
coef,cov = curve_fit(model,r,p)
# Càlcul de r2
y_data = np.array(p)
y_model = np.array([coef[0]*q + coef[1] for q in r])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)

print()
print('Coeficients de la regressió lineal de P vs R: ', coef, 'amb un error de', [np.sqrt(cov[0][0]),np.sqrt(cov[1][1])])
print()
print('Amb un coef r2 de ', r2)
x = np.linspace(R[0],R[5],100)
y = np.array(coef[0]*x+coef[1])
plt.figure(figsize=(8,6))
plt.plot(x,y,linestyle='--',color='k',label='Recta de regressió')
plt.errorbar(r,p,yerr=u_p,xerr=u_r,color='darkblue',marker='D',linestyle='',label='Punts experimentals',capsize=5,elinewidth=0.7)
plt.xlabel('$R$ [$\Omega$]')
plt.ylabel('$P_{e}$ [W]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/reg_P_vs_R.png',dpi=300)

# Calculem R_0 extrapolant només 5 punts de P vs R
print()
print('Extrapolant obtenim un valor per a R_0 ', -coef[1]/coef[0],'amb un error de ',np.sqrt((cov[1][1]/coef[0])**2+(cov[0][0]*coef[1]/coef[0]**2)**2))
print()

#logaritme del potencial elèctric vs logaritme de la temperatura

#Algoritmo para escoger los puntos de la parte lineal
# Busquem quins punts maximitzen r^2
r2_list=[]
for k in range(3,20): # Començem des de 3 per a no obtenir un r2=1 al fer una regressió de 2 punts, acabem en 20 per que és un punt experimental situat a on es veu que la tendència de la corba canvia.
    p = []
    theta = []
    for i in range(0,k):
        p.append(np.log(P_el[i]))
        theta.append(np.log(DT[i]))
    coef,cov = curve_fit(model,theta,p)

    y_data = np.array(p)
    y_model = np.array([coef[0]*q + coef[1] for q in theta])
    res = y_data - y_model
    ss_res = np.sum(res**2)
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    r2= 1 -(ss_res/ss_tot)
    r2_list.append(r2)

# Calculem i grafiquem la regressió amb el valor màxim de r2:
p = []
theta = []
print('El nombre de punts on la r2 és màxima és a',r2_list.index(max(r2_list)),'amb un valor de', r2_list[r2_list.index(max(r2_list))])
for i in range(0,r2_list.index(max(r2_list))):
    p.append(np.log(P_el[i]))
    theta.append(np.log(DT[i]))

coef,cov = curve_fit(model,theta,p)
print('Coeficients de la regressió lineal: ', coef, 'amb un error de', [np.sqrt(cov[0][0]),np.sqrt(cov[1][1])])
x = np.linspace(np.log(DT[0]),np.log(DT[r2_list.index(max(r2_list))]),100)
y = np.array(coef[0]*x+coef[1])

# Errors dels logaritmes
u_ln_DT = u_T/DT
u_ln_P_el = u_P_el/P_el

plt.figure(figsize=(8,6))
plt.axvline(x=np.log(DT[11]),color='red',linestyle='--',label='Separació de regions')
plt.plot(x,y,linestyle='--',color='k',label='Recta de regressió')
plt.errorbar(np.log(DT),np.log(P_el),yerr=u_ln_P_el,xerr=u_ln_DT,marker='D', color='forestgreen',linestyle='',label='Punts experimentals',capsize=5,elinewidth=0.7)
plt.text(5,1,'Convecció',fontsize=16,ha='center',bbox= dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="grey", alpha=0.2))
plt.text(7.3,-1,'Convecció\n+\nRadiació',fontsize=16,ha='center',bbox= dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="grey", alpha=0.2))
plt.xlabel('$\ln{\Delta T}$')
plt.ylabel('$\ln{P_{e}}$')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/lnP_el_vs_lnT.png',dpi=300)

# Grafiquem els punts experimentals de la segona regió i la corresponent extrapolació dels punts de la recta calculada.

p=[]
theta=[]
for i in range(r2_list.index(max(r2_list))-3,len(DT)):
        p.append(np.log(P_el[i]))
        theta.append(np.log(DT[i]))
p_extrapol = [coef[0]*a+ coef[1] for a in theta[3:]]  
#Error experimental
u_ln_DT = u_ln_DT[r2_list.index(max(r2_list))-3:]
u_ln_P_el = u_ln_P_el[r2_list.index(max(r2_list))-3:]
u_p_extrapol = np.sqrt((np.sqrt(cov[0][0])*np.array(theta[3:]))**2+(u_ln_DT[3:]*coef[0])**2+cov[1][1])

x = np.linspace(np.log(DT[r2_list.index(max(r2_list))-3]),np.log(DT[-1]),100)
y = np.array(coef[0]*x+coef[1])



plt.figure(figsize=(8,6))
plt.axvline(x=np.log(DT[11]),color='red',linestyle='--',label='Separació de regions')
plt.errorbar(theta,p,yerr=u_ln_P_el,xerr=u_ln_DT,marker='D', color='forestgreen',linestyle='',label='Punts experimentals',capsize=5,elinewidth=0.7)
plt.errorbar(theta[3:],p_extrapol,yerr=u_p_extrapol,xerr=u_ln_DT[3:],color='k',marker='D',label='Punts extrapolats',linestyle='',capsize=5,elinewidth=0.7)
plt.plot(x,y,linestyle='--',color='blue',label='Recta extrapolada')
plt.text(6.8,2.8,'Convecció\n+\nRadiació',fontsize=16,ha='center',bbox= dict(boxstyle="round,pad=0.5", edgecolor="black", facecolor="grey", alpha=0.2))
plt.xlabel('$\ln{\Delta T}$')
plt.ylabel('$\ln{P_{e}}$')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/extrapolació.png',dpi=300)

# Calculem la potència per radiació a partir de les resta de potencies

p_elec = np.exp(p[3:])
p_conv = np.exp(p_extrapol)
p_rad  = p_elec - p_conv
p_rad = p_rad.tolist()
theta_rad = theta[3:]

#Errors
u_p_rad = np.sqrt((u_ln_P_el[3:]*p_elec)**2+(u_p_extrapol*p_conv)**2)
u_ln_p_rad = u_p_rad/p_rad
u_theta_rad = u_ln_DT[3:]
u_theta_rad = [float(i) for i in u_theta_rad]
u_p_rad = [float(i) for i in u_p_rad]
u_ln_p_rad = [float(i) for i in u_ln_p_rad]
# Eliminaió d'outliers - Treiem els primers quatre punts ja que es desvien molt de la recta i tenen un error molt alt
del p_rad[0:3]
del theta_rad[0:3]
del u_p_rad[0:3]
del u_ln_p_rad[0:3]
del u_theta_rad[0:3]

# Calculem coeficients de regressió
coef,cov = curve_fit(model,theta_rad,np.log(p_rad))
x = np.linspace(theta_rad[0],theta_rad[-1],100)
y = coef[0]*x+coef[1]
# Grafiquem ln_P_rad vs ln_Delta_T

plt.figure(figsize=(8,6))
plt.errorbar(theta_rad,np.log(p_rad),xerr=u_theta_rad,yerr=u_ln_p_rad,marker='D',label='Punts calculats',linestyle='',capsize=5,elinewidth=0.7,color='rebeccapurple')
plt.plot(x,y,linestyle='--',color='darkslategrey',label='Recta de regressió')
plt.xlabel('$\ln{\Delta T}$')
plt.ylabel('$\ln{P_{r}}$')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/lnp_rad_vs_lnDelta_T.png',dpi=300)

print()
print('REGRESSIÓ LINEAL LN(P_RAD) VS LN(DELTA_T)')
print('Els coeficients de la regressió són', coef, 'amb una incertesa de', [np.sqrt(cov[0][0]),np.sqrt(cov[1][1])])
y_data = np.array(np.log(p_rad))
y_model = np.array([coef[0]*q + coef[1] for q in theta_rad])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print('El coeficient de regressió r2 és',r2)

# Rad vs T - Ajuste polinomi quàrtic
print()
print('AJUST POLINOMIC RAD VS T: y=ax^b')
def poly4(x,a,b):
     return a*x**b

coef4, cov4 = curve_fit(poly4,T,rad[1:])
y_data = np.array(rad[1:])
y_model = np.array([coef4[0]*q**coef4[1] for q in T])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print()
print('Coeficients del ajust quàrtic: ', coef4)
print('Coeficient de regressió r2: ',r2)
x= np.linspace(T[0],T[-1],100)
y= coef4[0]*x**coef[1]


plt.figure(figsize=(8,6))
plt.plot(x,y,linestyle='--',color='k',label='Ajust polinòmic')
plt.scatter(T,rad[1:],label='Dades experimentals',marker='D',color='forestgreen')
plt.xlabel('$T$')
plt.ylabel('$Rad$')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/T_vs_Rad.png',dpi=300)

# ln_rad vs ln_T - Ajust lineal
print()
print('AJUST LINEAL LN_RAD VS LN_T: y=a*x+b')
coef4,cov4 = curve_fit(model,np.log(T),np.log(rad[1:]))
x= np.linspace(np.log(T[0]),np.log(T[-1]),100)
y= coef4[0]*x + coef4[1]

y_data = np.array(np.log(rad[1:]))
y_model = np.array([coef4[0]*q +coef4[1] for q in np.log(T)])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)

print()
print('Coeficients del ajust lineal: ', coef4)
print('Coeficient de regressió r2: ',r2)

plt.figure(figsize=(8,6))
plt.plot(x,y,linestyle='--',color='k',label='Ajust lineal')
plt.scatter(np.log(T),np.log(rad[1:]),label='Dades experimentals',marker='D',color='forestgreen')
plt.xlabel('$\ln{(T)}$')
plt.ylabel('$\ln{(Rad)}$')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14)
plt.tight_layout()
plt.savefig('graphs/practica_Ib/plots/ln_T_vs_ln_Rad.png',dpi=300)

