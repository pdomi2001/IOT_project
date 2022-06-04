import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)


fig, axs = plt.subplots(nrows = 3, ncols = 1)
fig.set_facecolor('lightsteelblue')
fig.tight_layout()
# df_filtered = df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")]

giorno = 20220428
giorni_precedenti = 2

# inizio_periodo = 20220407000000
# fine_periodo = 20220408000000
inizio_periodo = giorno * 1000000
fine_periodo = (giorno + 1) * 1000000

inizio_periodo_prec = (giorno - giorni_precedenti) * 1000000

#aggiungo un campo nel quale è presente solo l'orario
df['time2'] = df.apply(lambda x: (x.time % 1000000), axis = 1)

min = df["time"].min()
num_elements = 0
def converti_data_ora(x):
	global num_elements
	num_elements = num_elements + 1
	return (num_elements)

# print (min)
#aggiungo un campo nel quale è presente solo la data
df['date'] = df.apply(lambda x: str(x.time / 1000000)[:8] , axis = 1)
# df['time3'] = df.apply(lambda x: int((x.time / 100) % 100000000) , axis = 1)
df['time3'] = df.apply(converti_data_ora , axis = 1)
# df['time3'] = df.apply(lambda x: int(x.time) - min , axis = 1)
# df['count_sent'] = df.apply(lambda x: x["count"] , axis = 1)

# print(df.head())
# print(df)

# estraggo i dati dei tre sensori separatamente
df_filtered_1 = df[(df.clientID=='iot_paride_1')]
df_filtered_2 = df[(df.clientID=='iot_paride_2')]
df_filtered_3 = df[(df.clientID=='iot_paride_3')]

zona_y = 0

axs[zona_y].plot(df_filtered_1.time3, df_filtered_1.count_wifi_c, label='termosifone')
axs[zona_y].plot(df_filtered_2.time3, df_filtered_2.count_wifi_c, label='stanza', linestyle = 'dashed')
axs[zona_y].plot(df_filtered_3.time3, df_filtered_3.count_wifi_c, label='condizionatore', linestyle = 'dotted')
axs[zona_y].set_title("Connessioni a wifi")
axs[zona_y].set_xlabel('N° dati ricevuti')
axs[zona_y].set_ylabel('Connessioni')
axs[zona_y].legend()
axs[zona_y].grid(True)

zona_y = 1

axs[zona_y].plot(df_filtered_1.time3, df_filtered_1.count_mqtt_c, label='termosifone')
axs[zona_y].plot(df_filtered_2.time3, df_filtered_2.count_mqtt_c, label='stanza', linestyle = 'dashed')
axs[zona_y].plot(df_filtered_3.time3, df_filtered_3.count_mqtt_c, label='condizionatore', linestyle = 'dotted')
axs[zona_y].set_title('Connessioni al Broker MQTT')
axs[zona_y].set_xlabel('N° dati ricevuti')
axs[zona_y].set_ylabel('Connessioni')
axs[zona_y].legend()
axs[zona_y].grid(True)

zona_y = 2

axs[zona_y].plot(df_filtered_1.time3, df_filtered_1.count_sent, label='termosifone')
axs[zona_y].plot(df_filtered_2.time3, df_filtered_2.count_sent, label='stanza', linestyle = 'dashed')
axs[zona_y].plot(df_filtered_3.time3, df_filtered_3.count_sent, label='condizionatore', linestyle = 'dotted')
axs[zona_y].set_title("Reset del modulo")
axs[zona_y].set_xlabel('N° dati ricevuti')
axs[zona_y].set_ylabel('Connessioni')
axs[zona_y].legend()
axs[zona_y].grid(True)

# print (df_filtered_1)

manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.savefig("connessioni.png", dpi=150)
plt.show()
