import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('registrazioni_new.txt', sep="\t", header=0)

# print(df[df.clientID=='iot_paride_1'].head)
# print(df[df.clientID=='iot_paride_2'].head)
# print(df[df.clientID=='iot_paride_3'].head)

# df[df.clientID=='iot_paride_1'].t_termosifone.plot()

# plt.figure()
# plt.title("la funzione seno")

fig, axs = plt.subplots(nrows = 4, ncols = 2)
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

def converti_data_ora(x):
	# ora = str(x.time % 1000000)
	ora = ("%06d" % (x.time % 1000000))
	# print (x.time)
	# print (ora[0:2] + ":" + ora[2:4] + ":" + ora[4:6])
	# return (ora[0:2] + ":" + ora[2:4] + ":" + ora[4:6])
	return (x.time % 1000000)

#aggiungo un campo nel quale è presente solo l'orario
df['time2']  = df.apply(converti_data_ora, axis = 1)

#aggiungo un campo nel quale è presente solo la data
df['date']  = df.apply(lambda x: str(x.time / 1000000)[:8] , axis = 1)

print(df.head())

df_filtered_1 = df[
									(df.clientID=='iot_paride_1')
								]
df_filtered_2 = df[
									(df.clientID=='iot_paride_2')
								]
df_filtered_3 = df[
									(df.clientID=='iot_paride_3')
								]
df_filtered_1_t = df_filtered_1[
									(df_filtered_1.time >= inizio_periodo)
									& (df_filtered_1.time <= fine_periodo)
									& (df_filtered_1.t_termosifone <= 60)
								]
df_filtered_2_t = df_filtered_2[
									(df_filtered_2.time >= inizio_periodo)
									& (df_filtered_2.time <= fine_periodo)
									& (df_filtered_2.t_termosifone <= 60)
								]
df_filtered_3_t = df_filtered_3[
									(df_filtered_3.time >= inizio_periodo)
									& (df_filtered_3.time <= fine_periodo)
									& (df_filtered_3.t_termosifone <= 60)
								]

df_filtered_1_t_prec = df_filtered_1[
									(df_filtered_1.time >= inizio_periodo_prec)
									& (df_filtered_1.time <= fine_periodo)
									& (df_filtered_1.t_termosifone <= 60)
								]
df_filtered_2_t_prec = df_filtered_2[
									(df_filtered_2.time >= inizio_periodo_prec)
									& (df_filtered_2.time <= fine_periodo)
									& (df_filtered_2.t_termosifone <= 60)
								]
df_filtered_3_t_prec = df_filtered_3[
									(df_filtered_3.time >= inizio_periodo_prec)
									& (df_filtered_3.time <= fine_periodo)
									& (df_filtered_3.t_termosifone <= 60)
								]
# print (df_filtered_1)
# print (df_filtered_2)
# print (df_filtered_3)

# axs.plot(df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")].time, df[(df.clientID=='iot_paride_2') & (df.time=="2022-04-05 10:2")].t_termosifone)
zona_x = 0
zona_y = 0
df_ = df_filtered_1_t
axs[zona_x, zona_y].plot(df_.time2, df_.t_termosifone, label='remoto', linestyle = '--')
ax2 = axs[zona_x, zona_y].twinx()
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
ax2.plot(df_.time2, df_.t_stanza, label='integrato', color = 'red')
ax2.set_ylabel('°C')
ax2.legend()
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
# axs[zona_x, zona_y].plot(df_.time, df_.h_stanza)
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('Sensore Termosifone')
axs[zona_x, zona_y].grid(True)
axs[zona_x, zona_y].legend(loc='upper left')
# axs[zona_x, zona_y].ticker(loc='upper left')

zona_x = 1
zona_y = 0
df_ = df_filtered_2_t
axs[zona_x, zona_y].plot(df_.time2, df_.t_termosifone, label='remoto')
ax2 = axs[zona_x, zona_y].twinx()
# axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
ax2.plot(df_.time2, df_.t_stanza, label='integrato')
ax2.set_ylabel('°C')
# axs[zona_x, zona_y].plot(df_.time, df_.h_stanza)
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('Sensore stanza')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

zona_x = 2
zona_y = 0
df_ = df_filtered_3_t
axs[zona_x, zona_y].plot(df_.time2, df_.t_termosifone, label='remoto')
axs[zona_x, zona_y].plot(df_.time2, df_.t_stanza, label='integrato')
# axs[zona_x, zona_y].plot(df_.time, df_.h_stanza)
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('Sensore condiz.')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

zona_x = 3
zona_y = 0

axs[zona_x, zona_y].set_title(giorno)
axs[zona_x, zona_y].plot(df_filtered_1_t.time, df_filtered_1_t.h_stanza, label='termosifone')
axs[zona_x, zona_y].plot(df_filtered_2_t.time, df_filtered_2_t.h_stanza, label='stanza')
axs[zona_x, zona_y].plot(df_filtered_3_t.time, df_filtered_3_t.h_stanza, label='condizionatore')
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('umidita\' nella stanza')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)



zona_x = 0
zona_y = 1

axs[zona_x, zona_y].plot(df_filtered_1.time, df_filtered_1.count_wifi_c, label='termosifone')
axs[zona_x, zona_y].plot(df_filtered_2.time, df_filtered_2.count_wifi_c, label='stanza')
axs[zona_x, zona_y].plot(df_filtered_3.time, df_filtered_3.count_wifi_c, label='condizionatore')
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('connessioni a wifi')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

zona_x = 1
zona_y = 1

axs[zona_x, zona_y].plot(df_filtered_1.time, df_filtered_1.count_mqtt_c, label='termosifone')
axs[zona_x, zona_y].plot(df_filtered_2.time, df_filtered_2.count_mqtt_c, label='stanza')
axs[zona_x, zona_y].plot(df_filtered_3.time, df_filtered_3.count_mqtt_c, label='condizionatore')
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('connessioni a mqtt')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

zona_x = 2
zona_y = 1

axs[zona_x, zona_y].plot(df_filtered_1_t_prec.time, df_filtered_1_t_prec.count_wifi_c, label='termosifone')
axs[zona_x, zona_y].plot(df_filtered_2_t_prec.time, df_filtered_2_t_prec.count_wifi_c, label='stanza')
axs[zona_x, zona_y].plot(df_filtered_3_t_prec.time, df_filtered_3_t_prec.count_wifi_c, label='condizionatore')
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('conn. a wifi last')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

zona_x = 3
zona_y = 1

axs[zona_x, zona_y].plot(df_filtered_1_t_prec.time, df_filtered_1_t_prec.count_mqtt_c, label='termosifone')
axs[zona_x, zona_y].plot(df_filtered_2_t_prec.time, df_filtered_2_t_prec.count_mqtt_c, label='stanza')
axs[zona_x, zona_y].plot(df_filtered_3_t_prec.time, df_filtered_3_t_prec.count_mqtt_c, label='condizionatore')
axs[zona_x, zona_y].set_xlabel('time')
axs[zona_x, zona_y].set_ylabel('conne. a mqtt last')
axs[zona_x, zona_y].legend()
axs[zona_x, zona_y].grid(True)

# axs.plot(df[df.clientID=='iot_paride_3'].time, df[df.clientID=='iot_paride_3'].t_termosifone)
# df[df.clientID=='iot_paride_1'].plot(x="time", y="t_termosifone", color="r")
# df[df.clientID=='iot_paride_2'].plot(x="time", y="t_termosifone", color="g")
# df[df.clientID=='iot_paride_3'].plot(x="time", y="t_termosifone", color="b")

plt.savefig("test.png");
plt.show()
