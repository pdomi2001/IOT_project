import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)

fig, axs = plt.subplots(nrows = 3, ncols = 1)
fig.set_facecolor('lightsteelblue')
fig.tight_layout()
# df_filtered = df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")]

giorno = 20220414
giorni_precedenti = 2

# inizio_periodo = 20220407000000
# fine_periodo = 20220408000000
inizio_periodo = giorno * 1000000
fine_periodo = (giorno + 1) * 1000000

inizio_periodo_prec = (giorno - giorni_precedenti) * 1000000

def converti_data_ora(x):
	# ora = str(x.time % 1000000)
	ora = ("%06d" % (x.time % 1000000))
	# print (x.time)
	# print (ora[0:2] + ":" + ora[2:4] + ":" + ora[4:6])
	# return (ora[0:2] + ":" + ora[2:4] + ":" + ora[4:6])
	return (int(x.time % 1000000) / 10000.0)

#aggiungo un campo nel quale è presente solo l'orario
df['time2']  = df.apply(converti_data_ora, axis = 1)

#aggiungo un campo nel quale è presente solo la data
df['date']  = df.apply(lambda x: str(x.time / 1000000)[:8] , axis = 1)

# print(df.head())

df_filtered_1 = df[
									(df.clientID=='iot_paride_1')
								]
# ----------------------------------------
temp_inizio_conteggio = 28.0 # gradi centigradi
delta_tempo_conteggio = 120 # secondi
giornosingolo = False
verbose = False
# ----------------------------------------
#filtro un giorno solo
if (giornosingolo):
	df_filtered_1_d = df_filtered_1[
									 (df_filtered_1.time >= inizio_periodo)
									 & (df_filtered_1.time <= fine_periodo)
									 & (df_filtered_1.t_termosifone <= 60)
								]
else:					
	df_filtered_1_d = df_filtered_1[
									 (df_filtered_1.t_termosifone <= 60)
								]
df_filtered_1_t = df_filtered_1_d[
									(df_filtered_1_d.t_termosifone >= temp_inizio_conteggio)
								]

# print (df_filtered_1_t)
# print (df_filtered_2)
# print (df_filtered_3)

def ConvertiInSecondi(timestr):
	# print ("Converto [%s]" % timestr)
	sec = int(timestr[-2:])
	min = int(timestr[-4:-2])
	ora = int(timestr[-6:-4])
	giorno = int(timestr[6:8])
	mese = int(timestr[4:6])
	anno = int(timestr[0:4])
	# print (type(giorno), type(mese), type(anno))
	secondi = sec + min * 60 + ora * 3600
	giorniinizio = datetime(int(anno), int(mese), int(giorno)).toordinal()
	secondi = secondi + 60 * 60 * 24 * giorniinizio 
	# secondi = secondi + giorno * 3600 * 24
	# secondi = secondi + mese * 3600 * 24 * 31
	# secondi = secondi + anno * 3600 * 24 * 31 * 12
	# print(secondi)
	return secondi

elem = df_filtered_1_t['time'].values.tolist()[0]
# print (df_filtered_1_t[(df_filtered_1_t['time'] == elem)].values.tolist()[0])
lastcount = 0
contabilizzatore = 0
for elem in df_filtered_1_t['time'].values.tolist():
	time, ip, str_sensore, h_stanza, t_stanza, t_termosifone, count_sent, count_wifi_c, count_mqtt_c, time2, data \
		= df_filtered_1_t[(df_filtered_1_t['time'] == elem)].values.tolist()[0]
	# print(e['count_sent'])
	# print(lastcount)
	time = str(time)
	if lastcount != 0:
		# if elem == lastelem + 1:
		# if int(e['count_sent']) == lastcount + 1:
		if int(count_sent) == lastcount + 1:
			# contabilizzatore = contabilizzatore + 1
			endtime = time
			# endtime = e['time'].astype("string")
			# print("tipo endtime", type(endtime))
		else:
			secondi = ConvertiInSecondi(endtime) - ConvertiInSecondi(starttime)
			if (verbose):
				print ("conteggio da %s a %s = %d" % (starttime, endtime, secondi))
			unita_contabilizzate = int(secondi / delta_tempo_conteggio)
			if (verbose):
				print ("unita contabilizzate %d / %d = %d" % (secondi, delta_tempo_conteggio, unita_contabilizzate))
			contabilizzatore = contabilizzatore + unita_contabilizzate 
			if (verbose):
				print ("nuovo conteggio", contabilizzatore)
			starttime = time
			# starttime = e['time'].to_string()
			# print("tipo starttime", type(starttime))
	else:
		starttime = time
		# starttime = e['time'].to_string()
		# print("tipo starttime", type(starttime))
	lastcount = count_sent
	# lastcount = pd.to_numeric(e['count_sent'])
	# print("tipo lastcount", type(lastcount))
	# print(lastcount)
	# print(e['count_sent'])
	# print(e)
	# print('----')
	# print (elem, count, df_filtered_1_t[(df_filtered_1_t['count_sent'] == elem)])
	# print (df_filtered_1_t[(df_filtered_1_t['time'] == elem)])

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