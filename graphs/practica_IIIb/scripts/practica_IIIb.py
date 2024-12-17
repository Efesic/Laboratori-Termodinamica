import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
from scipy.optimize import curve_fit
from scipy.optimize import newton
matplotlib.rcParams.update({'font.size': 20})


#AQUÍ SE PONE EL CÓDIGO PARA GENERAR TODOS LOS GRÉFICOS A LA VEZ
df = pd.read_excel('graphs/practica_IIIb/datos_isotermas.xlsx')


# Estructura iso_T = [p,V_sist,pV,1/V]
iso_10 = [df.iloc[35:57,11],df.iloc[35:57,12],df.iloc[35:57,26], df.iloc[35:57,27]]
iso_15 = [df.iloc[35:55,3],df.iloc[35:55,4],df.iloc[35:55,20],df.iloc[35:55,21]]
iso_20 = [df.iloc[3:24,11],df.iloc[3:24,12],df.iloc[3:24,26],df.iloc[3:24,27]]
iso_25 = [df.iloc[3:26,3],df.iloc[3:26,4],df.iloc[3:26,20],df.iloc[3:26,21]]
iso_30 = [df.iloc[35:57,15],df.iloc[35:57,16],df.iloc[35:57,29],df.iloc[35:57,30]]
iso_35 = [df.iloc[35:55,7],df.iloc[35:55,8],df.iloc[35:55,23],df.iloc[35:55,24]]
iso_40 = [df.iloc[3:23,15],df.iloc[3:23,16],df.iloc[3:23,29],df.iloc[3:23,30]]
iso_45 = [df.iloc[3:26,7],df.iloc[3:26,8],df.iloc[3:26,23],df.iloc[3:26,24]]

# Estructura punts_sat = [p_sat,V_sat]
punts_sat = [df.iloc[62:78,3].dropna(),df.iloc[62:78,4].dropna()]

# Dades de p i T a una corba isocòrica de volum entorn a 0.2ml

T_isocor = df.iloc[:,32].dropna().tolist()
p_isocor = df.iloc[:,33].dropna().tolist()

#--------------DIAGRAMA DE CLAPEYRON-----------------------
plt.figure(figsize=(8,6))
lines= []

line, = plt.plot(iso_10[1],iso_10[0], marker = 'o', markersize = 5,label='10',color='lightblue',linestyle='--')
lines.append(line)

line, = plt.plot(iso_15[1],iso_15[0],marker = 'o', markersize = 5,label='15',color='lightskyblue',linestyle='--')
lines.append(line)

line, = plt.plot(iso_20[1],iso_20[0],marker = 'o', markersize = 5,label='20',color='cadetblue',linestyle='--')
lines.append(line)

line, = plt.plot(iso_25[1],iso_25[0],marker = 'o', markersize = 5,label='25',color='lightslategray',linestyle='--')
lines.append(line)
line, = plt.plot(iso_30[1],iso_30[0],marker = 'o', markersize = 5,label='30',color='rosybrown',linestyle='--')
lines.append(line)
line, = plt.plot(iso_35[1],iso_35[0],marker = 'o', markersize = 5,label='35',color='indianred',linestyle='--')
lines.append(line)

line, = plt.plot(iso_40[1],iso_40[0],marker = 'o', markersize = 5,label='40',color='firebrick',linestyle='--')
lines.append(line)
line, = plt.plot(iso_45[1],iso_45[0],marker = 'o', markersize = 5,label='45',color='darkred',linestyle='--')
lines.append(line)

line_long = plt.scatter(punts_sat[1],punts_sat[0], s =30, color = 'k',marker ='D',label='Punts de saturació')

plt.xlabel('$V_{sist}$ [ml]')
plt.ylabel('$p$ [bar]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')

legend1 = plt.legend(handles=lines, ncol=4,bbox_to_anchor=(1, 1), title="Temperatura [$^\circ$C]",fontsize=13,loc="upper right",title_fontsize=18)
plt.gca().add_artist(legend1)
legend2 = plt.legend(handles=[line_long], loc="upper right", bbox_to_anchor=(1, 0.785), frameon=True,ncol=1,fontsize=13)
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IIIb/plots/Clapeyron.png',dpi=300)

#-------------------------------AJUST CORBA DE SATURACIÓ----------------------------------------------
def poly3(x,a,b,c,d):
    return a*x**3 + b*x**2 + c*x + d
coef, cov = curve_fit(poly3,punts_sat[1].tolist(), punts_sat[0].tolist())

xp = np.linspace(min(punts_sat[1]), max(punts_sat[1]), 100)
yp = coef[0]*xp**3 + coef[1]*xp**2 + coef[2]*xp + coef[3]

plt.figure(figsize=(8,6))
plt.scatter(punts_sat[1],punts_sat[0], label = 'Punts de saturació', s =20, color = 'k',marker ='D')
plt.plot(xp,yp,linestyle='--', color = 'indigo',label='Ajust polinòmic')
plt.xlabel('$V_{sist}$ [ml]')
plt.ylabel('$p$ [bar]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=16)
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/Corba_Saturacio.png",dpi=300)

y_data = np.array(punts_sat[0])
y_model = np.array([coef[0]*q**3 + coef[1]*q**2 + coef[2]*q + coef[3] for q in punts_sat[1]])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print()
print('Els coeficients del polinomi de tercer grau són:',coef, 'amb error de ', [float(np.sqrt(cov[a][a])) for a in range(0,4)])
print()
print('VALOR DE R2 PER A P3: ', r2)

p_sat = punts_sat[0].tolist()
V_sat = punts_sat[1].tolist()

# Valors crítics a priori
p_crit = max(p_sat)
V_crit = V_sat[p_sat.index(p_crit)]

# Valors crítics aplicant el model:
# 1) Calculem el volum crític
f = lambda x: 3*coef[0]*x**2 + 2*coef[1]*x + coef[2]
df = lambda x: 6*coef[0]*x + 2*coef[1]
x0 = 1
V_critt= newton(f,x0, fprime=df)
u_V_critt = np.sqrt(abs(f(V_critt))**2 + 0.2**2)

# Calculem la pressió crítica:
p_critt = poly3(V_critt,coef[0],coef[1],coef[2],coef[3])
u_p_critt = np.sqrt((u_V_critt*(f(V_critt)))**2 + (np.sqrt(cov[0][0])*V_critt**3)**2 + (np.sqrt(cov[1][1])*V_critt**2)**2 + (np.sqrt(cov[2][2])*V_critt)**2 + cov[0][0])

print()
print('El punt (V_crit,p_crit) màxim de les dades mesurades és: ', [V_crit,p_crit], 'amb un error igual al de les mesures experimentals')
print()
print('El punt (V_crit,p_crit) màxim de la corba ajustada és: ', [float(V_critt),float(p_critt)],'amb un error experimental de ', [u_V_critt,float(u_p_critt)])


#------------------// POLINOMI DE GRAU 4 - PROVA//--------------------------
"""
def poly6(x,a,b,c,d,e):
    return a*x**4 + b*x**3 + c*x**2 + d*x + e 
coef, cov = curve_fit(poly6,punts_sat[1].tolist(), punts_sat[0].tolist())

xp = np.linspace(min(punts_sat[1]), max(punts_sat[1]), 100)
yp = coef[0]*xp**4+ coef[1]*xp**3 + coef[2]*xp**2 + coef[3]*xp + coef[4]

plt.figure(figsize=(8,6))
plt.scatter(punts_sat[1],punts_sat[0], label = 'Punts de saturació', s =20, color = 'k',marker ='D')
plt.plot(xp,yp)
plt.savefig("graphs/practica_IIIb/plots/Corba_Saturacio_pol6.png")

y_data = np.array(punts_sat[0])
y_model = np.array([coef[0]*q**4+ coef[1]*q**3 + coef[2]*q**2 + coef[3]*q + coef[4] for q in punts_sat[1]])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print()
print('Els coeficients del polinomi de quart grau són:',coef, 'amb error de ', [float(np.sqrt(cov[a][a])) for a in range(0,4)])
print()
print('VALOR DE R2 PER A P4: ', r2)

p_critt = max(yp)
V_critt = xp[yp.tolist().index(p_critt)]
print()
print('Valors crítics p-V amb polinomi de grau 4', [p_critt,V_critt]) # Amb això l'error dona 46.37,  un valor massa gran

u_V = 0.2
u_p_critt = np.sqrt((u_V*(4*coef[0]*V_critt**3 + 3*coef[1]*V_critt**2 + 2*coef[2]*V_critt + coef[3]))**2 + (np.sqrt(cov[0][0])*V_critt**4)**2 + (np.sqrt(cov[1][1])*V_critt**3)**2 + (np.sqrt(cov[2][2])*V_critt**2)**2 + (np.sqrt(cov[3][3])*V_critt)**2 + cov[4][4])
print()
print('Error de p_crit ajustant a un polinomi de grau 4 ', u_p_critt)
"""
#-------------------------------------------------------------
# Calculem la temperatura crítica a partir d'una regressió de T_isocor vs p_isocor i d'una regressió T_isocor vs p_vap

p_vap = [17,19.5,21.5,24,27,30,33.5,37.5]
def lin_model(x,a,b):
    return a*x + b

lin_coef, lin_cov = curve_fit(lin_model,T_isocor,p_isocor)
lin_coef2, lin_cov2 = curve_fit(lin_model,T_isocor,p_vap)

x = np.linspace(min(T_isocor), max(T_isocor),100)
y = lin_coef[0]*x + lin_coef[1]
y2 = lin_coef2[0]*x + lin_coef2[1]
# Càlcul de r2

#Per a isocor
y_data = np.array(p_isocor)
y_model = np.array([lin_coef[0]*q + lin_coef[1] for q in T_isocor])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print()
print('DADES REGRESSIÓ P VS T ISOCORIC:')
print()
print('Valors coeficients isocor: ', lin_coef, 'amb uns errors de ', [float(np.sqrt(lin_cov[0][0])),float(np.sqrt(lin_cov[1][1]))])
print('Coeficient r2 de la regressió: ', r2)

#Per a vap
y_data = np.array(p_vap)
y_model = np.array([lin_coef2[0]*q + lin_coef2[1] for q in T_isocor])
res = y_data - y_model
ss_res = np.sum(res**2)
ss_tot = np.sum((y_data - np.mean(y_data))**2)
r2= 1 -(ss_res/ss_tot)
print('Valors coeficients vap: ', lin_coef2, 'amb uns errors de ', [float(np.sqrt(lin_cov2[0][0])),float(np.sqrt(lin_cov2[1][1]))])
print('Coeficient r2 de la regressió: ', r2)

plt.figure(figsize=(8,6))
#plt.scatter(T_isocor,p_isocor)
plt.scatter(T_isocor,p_vap,label='Punts experimentals',marker='D',s =30, color = 'k')
#plt.plot(x,y,linestyle='--',color = 'k', label='Isocor')
plt.plot(x,y2,linestyle='--',color = 'firebrick', label='Refressió lineal')

plt.xlabel('$T$ [$^\circ$C]')
plt.ylabel('$p_{vap}$ [bar]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=16)
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/p_vs_T_vap.png",dpi=300)

T_critt = (p_critt-lin_coef[1])/lin_coef[0]
T_crittt= (p_critt-lin_coef2[1])/lin_coef2[0]

u_T_critt = np.sqrt((np.sqrt(lin_cov[0][0])*(p_critt-lin_coef[1])/(lin_coef[0])**2)**2 + (u_p_critt/lin_coef[0])**2 + (np.sqrt(lin_cov[1][1])/lin_coef[0])**2)
u_T_crittt = np.sqrt((np.sqrt(lin_cov2[0][0])*(p_critt-lin_coef2[1])/(lin_coef2[0])**2)**2 + (u_p_critt/lin_coef2[0])**2 + (np.sqrt(lin_cov2[1][1])/lin_coef2[0])**2)
print()
print('Assumint que la temperatura pren un comportament lineal amb la pressió podem extrapolar la temperatura crítica, aquesta pren el valor de: ', T_critt, 'amb un error de ', u_T_critt, 'per a un comportament isocoric o de ', T_crittt, 'amb un error de ', u_T_crittt, 'fent servir les pressions de vapor.')
print()
print('El valor mig és ', float(np.mean([T_critt,T_crittt])), 'amb un error de ', u_T_crittt)

#--------------------DIAGRAMA D'AMAGAT-----------------------------

plt.figure(figsize=(8,6))
plt.plot(iso_10[0],iso_10[2],label='10',color='lightblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_15[0],iso_15[2],label='15',color='lightskyblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_20[0],iso_20[2],label='20',color='cadetblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_25[0],iso_25[2],label='25',color='lightslategray',linestyle='--',marker='D',markersize=4)
plt.plot(iso_30[0],iso_30[2],label='30',color='rosybrown',linestyle='--',marker='D',markersize=4)
plt.plot(iso_35[0],iso_35[2],label='35',color='indianred',linestyle='--',marker='D',markersize=4)
plt.plot(iso_40[0],iso_40[2],label='40',color='firebrick',linestyle='--',marker='D',markersize=4)
plt.plot(iso_45[0],iso_45[2],label='45',color='darkred',linestyle='--',marker='D',markersize=4)

plt.xlabel('$p$ [bar]')
plt.ylabel('$pV$ [bar$\cdot$ml]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=14,title='Temperatura [$^\circ$C]',title_fontsize='16',ncol=2)
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/Amagat.png",dpi=300)

#----------------Diagrama pV vs 1/V---------------------

plt.figure(figsize=(8,6))
plt.plot(iso_10[3],iso_10[2],label='10',color='lightblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_15[3],iso_15[2],label='15',color='lightskyblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_20[3],iso_20[2],label='20',color='cadetblue',linestyle='--',marker='D',markersize=4)
plt.plot(iso_25[3],iso_25[2],label='25',color='lightslategray',linestyle='--',marker='D',markersize=4)
plt.plot(iso_30[3],iso_30[2],label='30',color='rosybrown',linestyle='--',marker='D',markersize=4)
plt.plot(iso_35[3],iso_35[2],label='35',color='indianred',linestyle='--',marker='D',markersize=4)
plt.plot(iso_40[3],iso_40[2],label='40',color='firebrick',linestyle='--',marker='D',markersize=4)
plt.plot(iso_45[3],iso_45[2],label='45',color='darkred',linestyle='--',marker='D',markersize=4)

plt.xlabel('$1/V_{sist}$ [1/ml]')
plt.ylabel('$pV$ [bar$\cdot$ml]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=16,title='Temperatura [$^\circ$C]',title_fontsize=18,ncol=2,loc='upper right',bbox_to_anchor=(0.95,0.95))
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/pV_vs_V(-1).png",dpi=300)

#------------------TEOREMA DEL VIRIAL-----------------

# Primer per a la primera isoterma: T = 15 ºC
T_list = [10,15,20,25,30,35,40,45]
color_list = ['lightblue','lightskyblue','cadetblue','lightslategray','rosybrown','indianred','firebrick','darkred']
R = 83.14466
T_isocor = [a + 273.15 for a in T_isocor]
mols_list = []
u_mols_list = []
print()
print('VALORS DE REGRESSIÓ PV VS 1/V PER A CADA ISOTERMA')
plt.figure(figsize=(8,6))
for T in T_list:
    # Busquem la llista de punts que maximitzi r2
    inverse_V_list = [globals()[f"iso_{T}"][3].tolist()[0],globals()[f"iso_{T}"][3].tolist()[1],globals()[f"iso_{T}"][3].tolist()[2]]
    pV_list = [globals()[f"iso_{T}"][2].tolist()[0],globals()[f"iso_{T}"][2].tolist()[1],globals()[f"iso_{T}"][2].tolist()[2]]
    r2_list = []
    for k in range(3,len(globals()[f"iso_{T}"][2].tolist())):
        inverse_V_list.append(globals()[f"iso_{T}"][3].tolist()[k])
        pV_list.append(globals()[f"iso_{T}"][2].tolist()[k])

        coef,cov = curve_fit(lin_model,inverse_V_list,pV_list)

        y_data = np.array(pV_list)
        y_model = np.array([coef[0]*q + coef[1] for q in inverse_V_list])
        res = y_data - y_model
        ss_res = np.sum(res**2)
        ss_tot = np.sum((y_data - np.mean(y_data))**2)
        r2= 1 -(ss_res/ss_tot)
        r2_list.append(float(r2))
    # Trobem màxim i fem la regressió
    n_max = r2_list.index(max(r2_list))
    print()
    print(f'    Nombre màxim de punts per a T = {T} ºC: ',n_max)
    print('    Valor de r2: ',max(r2_list))
    inverse_V_list = []
    pV_list = []
    for k in range(n_max+1):
        inverse_V_list.append(globals()[f"iso_{T}"][3].tolist()[k])
        pV_list.append(globals()[f"iso_{T}"][2].tolist()[k])

    coef,cov = curve_fit(lin_model,inverse_V_list,pV_list)
    print('    Coeficients de regressió ', coef, 'amb un error de ',[float(np.sqrt(cov[0][0])),float(np.sqrt(cov[1][1]))])
    plt.scatter(inverse_V_list,pV_list,color=color_list[T_list.index(T)],marker='D',s=35,label=f'{T}')
    x = np.linspace(min(inverse_V_list),max(inverse_V_list),100)
    y = coef[0]*x+coef[1]
    plt.plot(x,y, marker='',color=color_list[T_list.index(T)], linestyle='--')
    mols = coef[1]/(R*T_isocor[T_list.index(T)-1])
    mols_list.append(mols)
    u_mols = np.sqrt((np.sqrt(cov[1][1])/(R*T_isocor[T_list.index(T)-1]))**2 + (0.2/(R*T_isocor[T_list.index(T)-1]**2))**2)
    u_mols_list.append(u_mols)
    print('    Valor de n ', mols, 'amb un error de ', u_mols)
plt.xlabel('$1/V_{sist}$ [1/ml]')
plt.ylabel('$pV$ [bar$\cdot$ml]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend(fontsize=16,title='Temperatura [$^\circ$C]',title_fontsize=18,ncol=2,loc='upper right',bbox_to_anchor=(0.95,0.95))
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/regs_virial.png",dpi=300)
print()
print('CÀLCUL GLOBAL DE MOLS: ', np.mean(mols_list), 'amb un error de ', max(u_mols_list))
print()
print('Calculem el valor de v_c (V_c/n): ', V_critt*10**(-3)/np.mean(mols_list), '[L/mol], amb un error de ', np.sqrt((u_V_critt*10**(-3)/np.mean(mols_list))**2+(max(u_mols_list)/(np.mean(mols_list)**2))**2), '[L/mol]')

# -------------------------VAN DER WAALS----------------------------
v_crit_tab = 198 # [ml/mol]
T_crit_tab = 318.71 # [K]
p_crit_tab = 37.586

a_VdW = 9*R*T_crit_tab*v_crit_tab/8
b_VdW = v_crit_tab/3

print()
print(f'COEFICIENTS DE VAN DER WAALS PER A VALORS TABULATS: a = {a_VdW} [bar.ml2/mol2], b = {b_VdW} [ml/mol]' )

# Gràfica comparativa entre les dades experimentals i un gas de Van der Waals amb a i b calculades amb les dades tabulades:

# Primer només les de Van der Waals
def Waals(T,v):
    return R*T/(v/mols - b_VdW) - a_VdW/((v/mols)**2)

lines = []
plt.figure(figsize=(8,6))
x=np.linspace(0.2,2,100)
line_long, = plt.plot(x,Waals(T_crit_tab,x),label='Isoterma crítica',color = 'k',linewidth=2.5,linestyle='-.')
for T in T_list:
    line, = plt.plot(x,Waals(T+273.15,x),label=f'{T}',color=color_list[T_list.index(T)], linestyle = '--')
    lines.append(line)

plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.ylabel('$p$ [bar]')
plt.xlabel('$V$ [ml]')
legend1 = plt.legend(handles=lines, ncol=2,bbox_to_anchor=(1, 1), title="Temperatura [$^\circ$C]",fontsize=16,loc="upper right",title_fontsize=19)
plt.gca().add_artist(legend1)
legend2 = plt.legend(handles=[line_long], loc="upper right", bbox_to_anchor=(1, 0.65), frameon=True,ncol=1,fontsize=16)
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/Van_der_Waals.png",dpi=300)

# Ara comparem dues isotermes, una a 45ºC i altra a 25ºC
lines = []
lines_2 = []
plt.figure(figsize=(8,6))
x=np.linspace(0.2,4,100)

line, = plt.plot(x,Waals(25+273.15,x),label='25',color='lightslategray', linestyle = '-.')
lines.append(line)
line, = plt.plot(x,Waals(45+273.15,x),label='45',color='darkred', linestyle = '-.')
lines.append(line)

line, = plt.plot(iso_25[1],iso_25[0],marker = 'D', markersize = 5,label='25',color='lightslategray',linestyle='--')
lines_2.append(line)
line, = plt.plot(iso_45[1],iso_45[0],marker = 'D', markersize = 5,label='45',color='darkred',linestyle='--')
lines_2.append(line)

plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.ylabel('$p$ [bar]')
plt.xlabel('$V$ [ml]')

legend1 = plt.legend(handles=lines, ncol=2,bbox_to_anchor=(1, 0.78), title="Temperatura per \n a Van der Waals [$^\circ$C]",fontsize=16,loc="upper right",title_fontsize=18)
plt.gca().add_artist(legend1)
legend2 = plt.legend(handles=lines_2, loc="upper right", bbox_to_anchor=(1, 1), frameon=True,ncol=2,fontsize=16, title='Temperatura per \n a dades experimentals [$^\circ$C]',title_fontsize=18)
legend1.get_title().set_horizontalalignment('center')
legend2.get_title().set_horizontalalignment('center')
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/Van_der_Waals_comparativa.png",dpi=300)
# Càlcul de pV/nRT = 3/8
print()
print('VALOR DEL COEFICIENT KAPPA:')
kappa_t = p_crit_tab*v_crit_tab/(R*T_crit_tab)
print('    Tabulada NIST: ', kappa_t)
v_crit_tab = 197 # [ml/mol]
T_crit_tab = 318.723 # [K]
p_crit_tab = 37.7
kappa_t = p_crit_tab*v_crit_tab/(R*T_crit_tab)
print('    Tabulada CRC: ', kappa_t)

u_z = np.sqrt((u_p_critt*V_critt/(mols*R*(T_crittt+273.15)))**2 + (u_V_critt*p_critt/(mols*R*(T_crittt + 273.15)))**2 + (u_mols*p_critt*V_critt/(R*(T_crittt+273.15)*mols**2))**2 + (u_T_crittt*p_critt*V_critt/(mols*R*(T_crittt+273.15)**2))**2)

kappa_e = p_critt*V_critt/(mols*R*(T_critt+273.15))
print('    Experimental: ', kappa_e, 'amb un error de ',u_z)
kappa_w = 3/8
print('    Van der Waals: ', kappa_w)

# Gràfica completa comparant VdW amb Experimental:

plt.figure(figsize=(8,6))
x=np.linspace(0.2,4,100)

lines = []
lines_2 = []
plt.figure(figsize=(8,6))
x=np.linspace(0.2,4,100)
for T in T_list:
    line, = plt.plot(x,Waals(T+273.15,x),label=f'{T}',color=color_list[T_list.index(T)], linestyle = '-',linewidth=0.8)
    lines.append(line)

line, = plt.plot(iso_10[1],iso_10[0], marker = 'o', markersize = 5,label='10',color='lightblue',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_15[1],iso_15[0],marker = 'o', markersize = 5,label='15',color='lightskyblue',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_20[1],iso_20[0],marker = 'o', markersize = 5,label='20',color='cadetblue',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_25[1],iso_25[0],marker = 'o', markersize = 5,label='25',color='lightslategray',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_30[1],iso_30[0],marker = 'o', markersize = 5,label='30',color='rosybrown',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_35[1],iso_35[0],marker = 'o', markersize = 5,label='35',color='indianred',linestyle='--')
lines_2.append(line)

line, = plt.plot(iso_40[1],iso_40[0],marker = 'o', markersize = 5,label='40',color='firebrick',linestyle='--')
lines_2.append(line)
line, = plt.plot(iso_45[1],iso_45[0],marker = 'o', markersize = 5,label='45',color='darkred',linestyle='--')
lines_2.append(line)

plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.ylabel('$p$ [bar]')
plt.xlabel('$V$ [ml]')

legend1 = plt.legend(handles=lines, ncol=4,bbox_to_anchor=(1, 0.74), title="Temperatura per \n a Van der Waals [$^\circ$C]",fontsize=14,loc="upper right",title_fontsize=16)
plt.gca().add_artist(legend1)
legend2 = plt.legend(handles=lines_2, loc="upper right", bbox_to_anchor=(1, 1), frameon=True,ncol=4,fontsize=14, title='Temperatura per \n a dades experimentals [$^\circ$C]',title_fontsize=16)
legend1.get_title().set_horizontalalignment('center')
legend2.get_title().set_horizontalalignment('center')
plt.tight_layout(pad=0.2)
plt.savefig("graphs/practica_IIIb/plots/Van_der_Waals_comparativa_completa.png",dpi=300)
