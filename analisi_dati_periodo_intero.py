import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)

def converti_data_ora(x):
	ora = ("%06d" % (x.time % 1000000))
	return (x.time % 1000000)

#aggiungo un campo nel quale è presente solo l'orario
df['time2']  = df.apply(lambda x: (x.time % 1000000) , axis = 1)

#aggiungo un campo nel quale è presente solo la data
df['date']  = df.apply(lambda x: str(x.time / 1000000)[:8] , axis = 1)

# plt.style.use('ggplot')
fig, axs = plt.subplots(nrows = 3, ncols = 1)
fig.set_facecolor('lightsteelblue')
fig.tight_layout()

# print(df.head())
conteggio_dati = df.groupby(["date"])["date"].count()
#ragguppo i valori per data e faccio la media per ogni giorno
# medie_1 = df[(df.clientID=='iot_paride_1')].groupby(["date"])["t_stanza"].mean()

# date = df[(df.clientID=='iot_paride_1')].groupby(["date"])

# print(date["date"])

media_temperature = df[(df.clientID=='iot_paride_2')].groupby(["date"])["t_stanza"].mean()
minima_temperatura = df[(df.clientID=='iot_paride_2')].groupby(["date"])["t_stanza"].min()
massima_temperatura = df[(df.clientID=='iot_paride_2')].groupby(["date"])["t_stanza"].max()

# calcolo l'umidità media usando i dati del modulo numero 2
media_umidita = df[(df.clientID=='iot_paride_2')].groupby(["date"])["h_stanza"].mean()

solo_date = []
# creo un array con solo le date da usare come asse delle x
for d in df[(df.clientID=='iot_paride_2')].groupby(["date"]):
	solo_date.append(d[0])

row = 0
# grafico con i dati delle temperature
axs[row].set_title("Temperature del periodo")
axs[row].plot(solo_date, media_temperature, label='media', linestyle = '--')
axs[row].plot(solo_date, minima_temperatura, label='minima', linestyle = '-')
axs[row].plot(solo_date, massima_temperatura, label='massima', linestyle = ':')
axs[row].set_ylabel('°C')

for label in axs[row].xaxis.get_ticklabels():
	label.set_rotation(45)
	
axs[row].legend()
axs[row].grid(True)

solo_date = []
for d in df.groupby(["date"]):
	solo_date.append(d[0])

row = 1
# grafico con l'umidità media giornaliera
axs[row].set_title("Umidità media giornaliera nel periodo")
axs[row].plot(solo_date, media_umidita, label='umidità (%)', linestyle = '-')
axs[row].set_ylabel('Umidità (%)')
axs[row].grid(True)
for label in axs[row].xaxis.get_ticklabels():
	label.set_rotation(45)

row = 2
axs[row].bar(solo_date, conteggio_dati, label='dati', linestyle = '-')
axs[row].set_title("Numero di dati ricevuti nel periodo")
axs[row].set_ylabel('Qt')
axs[row].grid(True)
for label in axs[row].xaxis.get_ticklabels():
	label.set_rotation(45)

solo_date = []
for d in df[(df.clientID=='iot_paride_2')].groupby(["date"]):
	solo_date.append(d[0])



plt.show()
