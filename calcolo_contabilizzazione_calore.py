
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)
fig, axs = plt.subplots(nrows = 3, ncols = 1)

fig.set_facecolor('lightsteelblue')
fig.tight_layout()

# df_filtered = df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")]
giorni_precedenti = 2
SECONDI_GIORNO = 60*60*24
# ----------------------------------------

giorno = 20220414
INIZIO_CONTEGGIO = 28.0 # gradi centigradi
DELTA_T_CONTEGGIO = 120 # secondi
GIORNOSINGOLO = False
VERBOSE = False

# ----------------------------------------

# inizio_periodo = 20220407000000
# fine_periodo = 20220408000000

inizio_periodo = giorno * 1e6
fine_periodo = inizio_periodo + 1e6
# (giorno+1)*1e6 = giorno*1e6+1*1e6 = inizio_periodo+1e6
inizio_periodo_prec = inizio_periodo - giorni_precedenti * 1e6
# (giorno-giorni_precedenti)*1e6 = giorno*1e6-giorni_precedenti*1e6 = inizio_giorni - giorni_precedenti*1e6

def converti_data_ora(time):
	return int(time%1e6) / 1e6

#aggiungo un campo nel quale è presente solo l'orario
df['time2']  = df["time"].apply(converti_data_ora)

#aggiungo un campo nel quale è presente solo la data

df['date']  = df["time"].apply(lambda x: str(x / 1e6)[:8])
df_filtered_1 = df[df.clientID=='iot_paride_1']


#filtro un giorno solo
if GIORNOSINGOLO:
	df_filtered_1_d = df_filtered_1[ df_filtered_1.time >= inizio_periodo
								   & df_filtered_1.time <= fine_periodo
								   & df_filtered_1.t_termosifone <= 60]
else:
	df_filtered_1_d = df_filtered_1[df_filtered_1.t_termosifone <= 60]
df_filtered_1_t = df_filtered_1_d[df_filtered_1_d.t_termosifone >= INIZIO_CONTEGGIO]
def ConvertiInSecondi(timestr):
	sec,min_,ora = map(int,(timestr[-2:],timestr[-4:-2],timestr[-6:-4]))
	giorno,mese,anno = map(int,(timestr[6:8],timestr[4:6],timestr[:4]))
	secondi = sec + min_ * 60 + ora * 3600
	giorniinizio = datetime(anno, mese, giorno).toordinal()
	return secondi + SECONDI_GIORNO * giorniinizio
elem = df_filtered_1_t['time'].values.tolist()[0]
# print (df_filtered_1_t[(df_filtered_1_t['time'] == elem)].values.tolist()[0])
lastcount = 0
contabilizzatore = 0
for (time, ip, str_sensore, h_stanza, t_stanza, t_termosifone,
	 count_sent, count_wifi_c, count_mqtt_c, time2, data) in df_filtered_1_t.values.tolist():
	time = str(time)
	if lastcount:
	
		if int(count_sent) == lastcount + 1:
			endtime = time
		else:
		
			secondi = ConvertiInSecondi(endtime) - ConvertiInSecondi(starttime)
			if (VERBOSE):
				print ("conteggio da %s a %s = %d secondi" % (starttime, endtime, secondi))
			unita_contabilizzate = int(secondi / DELTA_T_CONTEGGIO)
			if (VERBOSE):
				print ("unita contabilizzate %d / %d = %d" % (secondi, DELTA_T_CONTEGGIO, unita_contabilizzate))
			contabilizzatore +=  unita_contabilizzate 
			if (VERBOSE):
				print ("nuovo conteggio", contabilizzatore)
			starttime = time
	else:
		starttime = time
	lastcount = count_sent

print("Unita' contabilizzate: %d" % contabilizzatore)

'''
# axs.plot(df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")].time, df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")].t_termosifone)
zona_x = 0
zona_y = 0
df_ = df_filtered_1_t
# print(df_.time2, df_.t_termosifone)
axs[zona_x].plot(df_.time2, df_.t_termosifone, label='remoto', linestyle = '--')
ax2 = axs[zona_x].twinx()
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
ax2.plot(df_.time2, df_.t_stanza, label='integrato', color = 'red')
ax2.set_ylabel('°C')
ax2.legend()
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
# axs[zona_x, zona_y].plot(df_.time, df_.h_stanza)
axs[zona_x].set_xlabel('time')
axs[zona_x].set_ylabel('Sensore Termosifone')
axs[zona_x].grid(True)
axs[zona_x].legend(loc='upper left')
# axs[zona_x, zona_y].ticker(loc='upper left')

zona_x = 1
zona_y = 0
df_ = df_filtered_3_t
axs[zona_x].plot(df_.time2, df_.t_termosifone, label='remoto', linestyle = '--')
ax2 = axs[zona_x].twinx()
ax2.plot(df_.time2, df_.t_stanza, label='integrato', color = 'red')
ax2.set_ylabel('°C')
ax2.legend()
# axs[zona_x].plot(df_.time2, df_.t_stanza, label='integrato')
# axs[zona_x, zona_y].plot(df_.time, df_.h_stanza)
axs[zona_x].set_xlabel('time')
axs[zona_x].set_ylabel('Sensore condiz.')
axs[zona_x].legend()
axs[zona_x].grid(True)
axs[zona_x].legend(loc='upper left')

zona_x = 2
zona_y = 0
df_ = df_filtered_2_t
axs[zona_x].plot(df_.time2, df_.t_termosifone, label='remoto')
# ax2 = axs[zona_x].twinx()
# ax2.plot(df_.time2, df_.t_stanza, label='integrato')
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
# ax2.set_ylabel('°C')
axs[zona_x].plot(df_.time2, df_.t_stanza)
axs[zona_x].set_xlabel('time')
axs[zona_x].set_ylabel('Sensore stanza')
axs[zona_x].legend()
axs[zona_x].grid(True)


# zona_x = 3
# zona_y = 0

# axs[zona_x].set_title(giorno)
# axs[zona_x].plot(df_filtered_1_t.time2, df_filtered_1_t.h_stanza, label='termosifone')
# axs[zona_x].plot(df_filtered_2_t.time2, df_filtered_2_t.h_stanza, label='stanza')
# axs[zona_x].plot(df_filtered_3_t.time2, df_filtered_3_t.h_stanza, label='condizionatore')
# axs[zona_x].set_xlabel('time')
# axs[zona_x].set_ylabel('umidita\' nella stanza')
# axs[zona_x].legend()
# axs[zona_x].grid(True)


# axs.plot(df[df.clientID=='iot_paride_3'].time, df[df.clientID=='iot_paride_3'].t_termosifone)
# df[df.clientID=='iot_paride_1'].plot(x="time", y="t_termosifone", color="r")
# df[df.clientID=='iot_paride_2'].plot(x="time", y="t_termosifone", color="g")
# df[df.clientID=='iot_paride_3'].plot(x="time", y="t_termosifone", color="b")

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
# plt.savefig("termico.png", dpi=600)
plt.title("Giorno :" + str(giorno))
plt.show()
'''