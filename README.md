# Identificatore di sinusoidi sovrapposte

Individua sinusoidi a partire da serie di valori osservati.

## Descrizione
Il problema nasce dall'individuazione di satelliti indistinguibili a partire unicamente dal loro moto.
Lo scopo e la funzionalità del programma è quello di individuare n sinusoidi sovrapposte a partire da una serie di osservazioni, 
quindi definire ampiezza, pulsazione e fase delle suddette sinusoidi.
Il programma è suddiviso principalmente in due moduli:

* Interpolazione
* Assegnamento

La funzione del primo è la definizione del modello per l'individuazione di una singola sinusoide.
Il secondo ha il compito di controllare i parametri del modello, selezionare la migliore soluzione individuata 
e di individuare gli assegnamenti corretti che identificano le sinusoidi.

## Inizializzazione

### Dipendenze

Per poter eseguire il codice  è necessario: 

* Python 3.9
* Ampl 

La directory di installazione di ampl deve essere nel search path di sistema.
I successivi passaggi sono:

1. Clonare la repository `git clone ...`
2. `cd Tirocinio`
3. Installare le dipendenze Python `python -m pip install -r requirements.txt`


### Eseguire il programma
A partire dalla directory Tirocinio:

* Eseguire il comando `python -m IdentificaSatelliti.driver`

A seguito dell'esecuzione di questo comando sarà richiesto l'inserimento delle caratteristiche del problema, relativo alle sinusoidi sovrapposte, 
che si vuole testare la risoluzione. 

Nello specifico si richiede:
 * L'intervallo di periodi delle sinusoidi sovrapposte.
 * Il numero di osservazioni.
 * Il numero di sinusoidi sovrapposte.
 * Per ogni sinusoide ampiezza, pulsazione e fase per la generazione dei punti.
 * Errore massimo nei punti generati.

Il risultato corrisponderà ad:
 * Errore quadratico medio 
 * Ampiezza, pulsazione e fase e periodo 

Questo per ogni sinusoide, ed infine il tempo di esecuzione.
#### Esempio 
![alt text](https://github.com/UnJay-0/Tirocinio/blob/master/example_1.png)
![alt text](https://github.com/UnJay-0/Tirocinio/blob/master/example_1_solution.png)

## Autori

Jonathan Junior Agyekum 
