import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
matplotlib.rcParams.update({'font.size': 23})

df = pd.read_excel('graphs/practica_IVc/PIV_C.xlsx',sheet_name='triple')
# Sencer fins a poc més del punt triple
t_s = df.iloc[12:650,0].tolist()           # [s]
p_s = df.iloc[12:650,1].tolist()           # [torr]
T_s = df.iloc[12:650,2].tolist()           # [ºC]

# Baixada al punt triple, sense el salt de pressió dle primer camí
t_b = df.iloc[120:670,0].tolist()           # [s]
p_b = df.iloc[120:670,1].tolist()           # [torr]
T_b = df.iloc[120:670,2].tolist()           # [ºC]

p_triple_raro = min(p_s,key = lambda x: abs(x-40.41))
index = p_s.index(p_triple_raro)

# Errors
u_p = 0.01                                  # [Torr]
u_T = 0.1                                   # [ºC]
u_t = 0.1                                   # [s]



# Gràfiques semi-senceres
plt.figure(figsize=(8,6))
plt.scatter(T_s,p_s, marker='D', s=10, color='firebrick',label='Punts experimentals')
plt.xlabel('$T$ [$^\circ$C]')
plt.ylabel('$p$ [Torr]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/diagrama_de_fases.png', dpi=300)

plt.figure(figsize=(8,6))
plt.scatter(t_s,p_s, marker='D', s=10, color='darkblue',label='Punts experimentals')
plt.xlabel('$t$ [s]')
plt.ylabel('$p$ [Torr]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/p_vs_t.png', dpi=300)

plt.figure(figsize=(8,6))
plt.scatter(t_s,T_s, marker='D', s=10, color='forestgreen',label='Punts experimentals')
plt.ylabel('$T$ [$^\circ$C]')
plt.xlabel('$t$ [s]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/T_vs_t.png', dpi=300)


#-------------------------------------------------------------------------------
#-------------------------------------------------------------------------------

# Gràfiques tallades
plt.figure(figsize=(8,6))
plt.scatter(T_b,p_b, marker='D', s=10, color='firebrick',label='Punts experimentals')
plt.xlabel('$T$ [$^\circ$C]')
plt.ylabel('$p$ [Torr]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/diagrama_de_fases_tallat.png', dpi=300)

print('CÀLCUL DE LES COORDENADES MESURADES DEL PUNT CRÍTIC: ')
print('El valor de pressió mínima que s\'ha mesurat és: ', min(p_b), 'a temps ', t_b[p_b.index(min(p_b))])
print(p_triple_raro,T_s[index])
rang = 6
p_triple_list = []
T_triple_list = []
for i in range(-rang,rang,1):
    p_triple_list.append(p_b[p_b.index(min(p_b))+i])
    T_triple_list.append(T_b[p_b.index(min(p_b))+i])

error_p_trip = np.sqrt((np.std(p_triple_list,ddof=1))**2 + u_p**2)
error_T_trip = np.sqrt((np.std(T_triple_list,ddof=1))**2 + u_T**2)
print()
print('La mitjana de pressió i temperatura de (suposadament) el punt triple del ciclohexà és: ', np.mean(p_triple_list), '±', error_p_trip, '[Torr], ', np.mean(T_triple_list), '±', error_T_trip, '[ºC]')
print(np.mean(p_triple_list))
plt.figure(figsize=(8,6))
plt.scatter(t_b,p_b, marker='D', s=10, color='darkblue',label='Punts experimentals')
plt.xlabel('$t$ [s]')
plt.ylabel('$p$ [Torr]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/p_vs_t_tallat.png', dpi=300)

plt.figure(figsize=(8,6))
plt.scatter(t_b,T_b, marker='D', s=10, color='forestgreen',label='Punts experimentals')
plt.ylabel('$T$ [$^\circ$C]')
plt.xlabel('$t$ [s]')
plt.minorticks_on()
plt.tick_params(which= 'major', direction='in',top = True,right =True,size = 10)
plt.tick_params(which= 'minor', direction='in',top = True,right =True,size = 5)
plt.grid(linestyle='--')
plt.legend()
plt.gca().get_legend().legend_handles[0].set_sizes([60])
plt.tight_layout(pad=0.2)
plt.savefig('graphs/practica_IVc/plots/T_vs_t_tallat.png', dpi=300)

