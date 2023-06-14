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
