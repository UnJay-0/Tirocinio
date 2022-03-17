'''
I prodotti sono 3. Le materie prime sono 5.

Tabella 1: composizione dei prodotti
(unità di materia per ogni unità di prodotto)

              Prodotto
Materia     P1   P2   P3
   M1       20   15   30
   M2       12   18   40
   M3       25   21   30
   M4       30   38   18
   M5       25   12   33


Tabella 2: Parametri per il calcolo dei prezzi

Prodotto    Alfa   Beta   Gamma
   P1        50     50     0.8
   P2        48     55     0.2
   P3        65     45     0.5


Tabella 3: Disponibilità di materie (numero di unità per periodo)

Materia  Quantità
   M1      1600
   M2      1800
   M3      2200
   M4      3800
   M5      1300

'''

N_PRODOTTI = 3
N_MATERIE = 5

COMP_PROD = [[20, 15, 30],
             [12, 18, 40],
             [25, 21, 30],
             [30, 38, 18],
             [25, 12, 33]]
ALFA = [50, 48, 65]
BETA = [50, 55, 45]
GAMMA = [0.8, 0.2, 0.5]

DISP = [1600, 1800, 2200, 3800, 1300]
