

sep = "\t"
# sep = ","

with open('registrazioni.txt') as f:
	lines = f.readlines()
print (len(lines))

array_elements= []
intestazione_array = []
for line in lines:
	elements = line.split(";")
	if len (elements) >= 9:
		if elements[0][0:4].isnumeric(): # salto le righe con eventuali dati spuri
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



f1 = open("registrazioni_new.txt", "w")
f1.write(sep.join(intestazione_array))
f1.write("\n")
for riga in array_elements:
	f1.write(riga)
f1.close()
