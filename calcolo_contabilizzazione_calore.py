
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)

# df_filtered = df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")]
giorni_precedenti = 2
SECONDI_GIORNO = 60*60*24
# ----------------------------------------

giorno = 20220414
INIZIO_CONTEGGIO = 28.0 # gradi centigradi
DELTA_T_CONTEGGIO = 120 # secondi
GIORNOSINGOLO = True # filtra i dati per il giorno indicato
SHOWGRAFICO = True  # crea mostra un grafico con l'andamento della temperatura
					# e delle attivazioni del conteggio

VERBOSE = False # mostra più informazioni 
# ----------------------------------------

inizio_periodo = giorno * 1e6
fine_periodo = inizio_periodo + 1e6
# (giorno+1)*1e6 = giorno*1e6+1*1e6 = inizio_periodo+1e6
#inizio_periodo_prec = inizio_periodo - giorni_precedenti * 1e6
# (giorno-giorni_precedenti)*1e6 = giorno*1e6-giorni_precedenti*1e6 = inizio_giorni - giorni_precedenti*1e6

def converti_data_ora(time):
	return int(time % 1e6) / 1e4
def check_conteggio_attivo(temp):
	if (temp >= INIZIO_CONTEGGIO):
		return 1
	else:
		return 0

#aggiungo un campo nel quale è presente solo l'orario
df['time2']  = df["time"].apply(converti_data_ora)

#aggiungo un campo nel quale è indicato se il conteggio è attivo
df['conteggio_attivo']  = df["t_termosifone"].apply(check_conteggio_attivo)

#aggiungo un campo nel quale è presente solo la data
df['date']  = df["time"].apply(lambda x: str(x / 1e6)[:8])
df_filtered_1 = df[df.clientID=='iot_paride_1']

#filtro un giorno solo
if GIORNOSINGOLO:
	df_filtered_1_d = df_filtered_1[ (df_filtered_1.time >= inizio_periodo)
								   & (df_filtered_1.time <= fine_periodo)
								   & (df_filtered_1.t_termosifone <= 60)]
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
lastcount = 0
contabilizzatore = 0
for (time, ip, str_sensore, h_stanza, t_stanza, t_termosifone,
	 count_sent, count_wifi_c, count_mqtt_c, time2, conteggio_attivo, data) in df_filtered_1_t.values.tolist():
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

if (SHOWGRAFICO):
	fig, axs = plt.subplots(nrows = 1, ncols = 1)

	fig.set_facecolor('lightsteelblue')
	fig.tight_layout()
	df_ = df_filtered_1_d
	axs.plot(df_.time2, df_.t_termosifone, label='remoto', linestyle = '--')
	ax2 = axs.twinx()
	ax2.plot(df_.time2, df_.conteggio_attivo, label='conteggio', color = 'red')
	ax2.fill_between(df_.time2, 0, 1, where=df_.conteggio_attivo> 0, facecolor='green', alpha=0.5)
	ax2.set_ylabel('')
	ax2.legend()

	axs.set_xlabel('time')
	axs.set_ylabel('Sensore Termosifone')
	axs.grid(True)
	axs.legend(loc='upper left')

	# plt.axhline(y = INIZIO_CONTEGGIO, color = 'b', linestyle = ':', label = "blue line")
	axs.axhline(y = INIZIO_CONTEGGIO, color = 'y', linestyle = '-', label = "blue line")
	plt.title("Giorno :" + str(giorno))
	plt.show()
