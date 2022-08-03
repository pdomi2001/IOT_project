"# IOT_project" 

Funzione dei file del progetto:

- mqtt_subscriber.py: Questo script resta in ascolto sul server MQTT e scrive le rilevazioni
- converti_dati.py: Converte i dati ricevuti in un formato che sia leggibile da Pandas
- analisi_dati_connessioni.py: Analizza i dati relativi alle connessioni effettuate dai moduli e crea una serie di grafici che indicano le riconnessioni nell'intero periodo.
- analisi_dati_periodo_intero.py: Analizza i dati relativi alle temperature medie giornaliere e l'umidità media giornaliera.
- analisi_dati_termico.py: Analizza i dati relativi ad un dato giorno (nel nostro caso il 14 aprile 2022) e mostra gli andamenti, durante la giornata delle temperature registrate dai sensori interni e dalle sonde dei moduli.
- calcolo_contabilizzazione_calore.py: In base ai dati registrati calcola quante unità di contabilizzazione sono state utilizzatee mostra un grafico con i periodi di contabilizzazione

- progetto_esp.ino: Progetto per Arduino da caricare sulla ESP32
- arduino_secrets.h: File che contiene le informazioni per far connettere alla rete WIFI la ESP32
