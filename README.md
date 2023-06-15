# OBD Simulator

Programma python che simula dati OBD accessibili all'esterno tramite BLE e tramite websocket.

# Requisiti

Installare le seguenti librerie python:
- [Bless](https://pypi.org/project/bless/)
- [Websockets](https://pypi.org/project/websockets/)

## Linux
```bash
pip3 install bless
pip3 install websockets
```

# Esecuzione

Trovare l'indirizzo ip della propria macchina, (`ip address show` su Linux) e inserilo al posto di quello specificato di default ("192.168.1.50") e passato come argomento alla thread del web socket; se la porta 8765 è già in uno, cambiare anche il valore della porta. Infine eseguire con:
```bash
cd <directory dove si trova il file main.py>
python3 main.py
```

# OBDSimulator

Lo script si esegue sul Raspberry.
Al fine di leggere i dati dal veicolo, usiamo l'emulatore (https://github.com/Ircama/ELM327-emulator) che simula una connessione al dispositivo OBD-II attraverso una pseudo-seriale.

Lo script resta in attesa di connessione Bluetooth. Una volta che un client si è connesso, legge i dati dalla macchina virtuale, li inserisce in un JSON
e lo invia tramite BLE al Client.

# OBDClient

Script in Python per testare la ricezione dei dati macchina.
Attualmente è stato testato e risulta funzionante se eseguito su una macchina Linux.

Lo script si collega con un socket bluetooth al raspberry e legge i dati. Successivamente li stampa sul terminale.
