import pandas as pd
import math
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .solCollector import SolCollector


reader = valReader("IdentificaSatelliti/values.csv")
STARTING_TOL = 1e-6
STARTING_STEP = 1
solver = "knitro"
rangeValues = []


def setRange(val1: float, val2: float):
    """
    Overview
    -------------------
    Imposta gli intervalli nella quale effettuare la ricerca della soluzione

    Params
    -------------------
    val1 (float) - limite inferiore
    val2 (float) - limite superiore

    """
    n = 0
    if (val2 - val1) / 5 >= 500:
        n = 5
    elif (val2 - val1) / 5 >= 200:
        n = 3
    else:
        n = 2
    interval = (val2 - val1) / n
    limit = val1 + interval
    for i in range(n - 1):
        rangeValues.append(limit)
        limit += val1 + interval
    rangeValues.append(val2)


def writeValues(values: pd.core.frame.DataFrame) -> dict:
    """
    Overview
    -------------------
    Compone un dizionario contenente le informazioni della sola colonna (x, y)
    di values.

    Params
    -------------------
    values (Dataframe) - dataframe contenente una sola colonna (x, y)
                         e k osservazioni.

    Returns
    -------------------
    dict - dizionario contenente tutte le informazioni utili per il calcolo
           della sinusoide di interpolazione.
    """
    dataValues = {"numeroPunti": values.index.size,
                  "y": [], "t": [], "b": STARTING_STEP}
    colLabels = values.columns.tolist()
    for label in colLabels:
        if label.find("x") != -1:
            dataValues["t"] = values[label].tolist()
        else:
            dataValues["y"] = values[label].tolist()
    return dataValues


def amplOptCol(col: pd.core.frame.DataFrame, algorithm=solver):
    """
    Overview
    -------------------
    Individuazione della soluzione tramite il modello Ampl

    Params
    -------------------
    values (Dataframe) - dataframe contenente una sola colonna (x, y)
                         e k osservazioni.

    Returns
    -------------------
    Tupla contenente i valori della soluzione individuata
    """

    data = writeValues(col)
    data["minMax"] = True
    multiplier = 0
    currentRange = [0, 0]
    interval = (rangeValues[1] - rangeValues[0])
    minValue = (interval * 5) / 100
    sol = SolCollector()
    for r in rangeValues:
        currentRange = [r - interval + 0.1, r]
        data["minMax"] = True
        data["fixedA"] = None
        data["multiplier"] = multiplier
        setDataAmpl(currentRange, data)
        result = interpolation(data, algorithm=algorithm)
        sol.insert(result)
        while (currentRange[1] - currentRange[0]) > minValue:

            data["minMax"] = False
            data["fixedA"] = result[1][0]
            result = interpolation(data, algorithm=algorithm)
            solPeriod = 2*math.pi / result[1][1]

            if (math.isclose(solPeriod, currentRange[0],
                             rel_tol=1e-1, abs_tol=1e-1)):
                setDataAmpl(
                    ((currentRange[1]+currentRange[0])/2, currentRange[1]),
                    data)
                data["minMax"] = False
                data["fixedA"] = result[1][0]
                result = interpolation(data, algorithm=algorithm)
                solPeriod = 2*math.pi / result[1][1]
            elif (math.isclose(solPeriod, currentRange[1],
                               rel_tol=1e-1, abs_tol=1e-1)):
                setDataAmpl(
                    (currentRange[0], (currentRange[1]+currentRange[0])/2),
                    data)
                data["minMax"] = False
                data["fixedA"] = result[1][0]
                result = interpolation(data, algorithm=algorithm)
                solPeriod = 2*math.pi / result[1][1]
            if ((math.isclose(solPeriod, currentRange[0],
                              rel_tol=1e-1, abs_tol=1e-1))
                or (math.isclose(solPeriod, currentRange[1],
                                 rel_tol=1e-1, abs_tol=1e-1))
                or (math.isclose(solPeriod,
                                 (currentRange[1]+currentRange[0])/2,
                                 rel_tol=1e-1, abs_tol=1e-1))):
                break

            # test intervallo inferiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((currentRange[0], solPeriod), data)
            data["init"] = 2*math.pi / solPeriod
            resultInf = interpolation(data, algorithm=algorithm)
            sol.insert(resultInf)

            # test intervallo superiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((solPeriod, currentRange[1]), data)
            data["init"] = 2*math.pi / solPeriod
            resultSup = interpolation(data, algorithm=algorithm)
            sol.insert(resultSup)

            if resultInf[0] < resultSup[0]:
                currentRange = (currentRange[0], solPeriod - solPeriod * 1e-1)
            else:
                currentRange = (solPeriod + solPeriod * 1e-1, currentRange[1])
        multiplier += 1
    return sol.getSol()


def setDataAmpl(currentRange, data):
    """
    Overview
    -------------------
    Compone un dizionario contenente le informazioni per il modello Ampl

    Params
    -------------------
    currentRange (tuple) -> intervallo di periodo corrente
    data (dict) -> dizionario che conterrà tutte le informazioni utili per
                    il calcolo della sinusoide di interpolazione.
    """
    data["init"] = 2*math.pi / (sum(currentRange) / 2)
    data["minMax"] = True
    data["minW"] = 2*math.pi / currentRange[1]
    data["maxW"] = 2*math.pi / currentRange[0]


# def dist(pointA: tuple, pointB: tuple) -> float:
#     return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)
#
#
# def utopic(results: tuple) -> dict:
#     optimal = [0]
#     value = 999999
#     for result in results:
#         currentVal = dist((math.pi*2 / result[1][1], result[0]),
#                           (5000, 0))
#         if currentVal < value:
#             value = currentVal
#             optimal = result
#     return optimal
