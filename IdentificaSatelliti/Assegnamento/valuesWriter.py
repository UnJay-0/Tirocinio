import csv
import math
from random import shuffle
from .valuesReader import valReader


def generateValues(a, w, f, num) -> dict:
    dataValues = {}
    t = [n for n in range(num)]
    y = []
    for i in t:
        y.append(a * math.sin(w * i + f))
    dataValues['x0'] = t
    dataValues['y0'] = y
    return dataValues


def writeDataValues(sinousoids: dict) -> None:
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
