

sep = "\t"
# sep = ","

with open('registrazioni.txt') as f:
	lines = f.readlines()


array_elements= []
array_elements2 = []
intestazione_array = []
for line in lines:
	elements = line.split(";")
	if len (elements) >= 9:
		if len(array_elements) == 0:
			intestazione_array.append("time")
		array_singolo_elemento = []
		for elemento in elements:
			dati = elemento.split("=")
			if len(array_elements) == 0:
				if len(dati) > 1:
					intestazione_array.append(dati[0])
			if len(dati) == 1:
				array_singolo_elemento.append(dati[-1][:19].replace("-","").replace(".","").replace(":","").replace(" ",""))
			else:
				array_singolo_elemento.append(dati[-1])
		# 
		if not "nan" in array_singolo_elemento:
			array_elements.append(sep.join(array_singolo_elemento))
			array_elements2.append(array_singolo_elemento)



f1 = open("registrazioni_new.txt", "w")
f1.write(sep.join(intestazione_array))
f1.write("\n")
for riga in array_elements:
	f1.write(riga)
f1.close()

# genero il codice sql
f1 = open("registrazioni_new.sql", "w")
# f1.write(sep.join(intestazione_array))
f1.write("\n")
for riga in array_elements2:
	f1.write('INSERT INTO sensori (time, sender_ip, clientID, h_stanza, t_stanza, t_termosifone, count, count_wifi_c, count_mqtt_c)\n')
	f1.write("VALUES (")
	first = True
	for elemento in riga:
		if not first:
			f1.write(', ')
		else:
			first = False
		f1.write('"')
		f1.write(elemento.replace("\n",""))
		f1.write('"')
	f1.write(");")
	f1.write("\n")
f1.close()


