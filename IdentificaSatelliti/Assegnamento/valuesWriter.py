import csv
import math
from random import shuffle, choice
from .valuesReader import valReader


def generateValues(a, w, f, num) -> dict:
    """
    Overview
    -------------------
    Calcola i valori di una sinusoide dati i suoi parametri

    Params
    -------------------
    a (float) -> Ampiezza.
    w (float) -> Pulsazione.
    f (float) -> Fase.

    Returns
    -------------------
    Restituisce un dict contenente (x, y) della sinusoide specificata.

    """
    dataValues = {}
    t = [n for n in range(num)]
    y = []
    for i in t:
        y.append(a * math.sin(w * i + f))
    dataValues['x0'] = t
    dataValues['y0'] = y
    return dataValues


def generateValuesError(a, w, f, num, maxErr) -> dict:
    """
    Overview
    -------------------
    Calcola i valori di una sinusoide dati i suoi parametri

    Params
    -------------------
    a (float) -> Ampiezza.
    w (float) -> Pulsazione.
    f (float) -> Fase.
    maxErr (float) -> Errore massimo nelle osservazioni.

    Returns
    -------------------
    Restituisce un dict contenente (x, y) della sinusoide specificata.

    """
    dataValues = {}
    t = [n for n in range(num)]
    y = []
    for i in t:
        if maxErr != 0:
            err = a * math.sin(w * i + f) * choice(range(0, maxErr))/100
        else:
            err = 0
        if choice([0, 1]) == 1:
            err = 0 - err
        y.append(a * math.sin(w * i + f) + err)
    dataValues['x0'] = t
    dataValues['y0'] = y
    return dataValues


def writeDataValues(sinousoids: dict) -> None:
    """
    Overview
    -------------------
    Scrive su un file (values.csv) i valori delle sinusoidi ricevuti in input.

    Params
    -------------------
    sinousoids (dict) -> sinusoidi.

    """
    header = []
    for n in range(0, len(sinousoids) - 1):
        index = valReader.translateSat(n)
        header.append(index[0])
        header.append(index[1])
    data = []
    index = [i for i in range(1, len(sinousoids))]
    for n in range(sinousoids[0]):
        row = []
        for i in index:
            row.append(sinousoids[i]["x0"][n])
            row.append(sinousoids[i]["y0"][n])
        shuffle(index)
        data.append(row)
    with open("IdentificaSatelliti/values.csv", "w", encoding="UTF8") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data)
