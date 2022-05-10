import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nlopt
import math
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues


reader = valReader("IdentificaSatelliti/values.csv")
STARTING_TOL = 1e-6
STARTING_STEP = 1


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


def optimizeCol(col: pd.core.frame.DataFrame,
                algorithm=nlopt.LN_COBYLA, maxtime=0.05) -> tuple:
    step = 1
    period = 1
    results = []
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    x_coordinates = []
    utopicY = 99999
    while period < 1e3:
        data["b"] = period
        print(f"periodo: {period}")
        try:
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            results.append(result)

            if result[0] < utopicY:
                utopicY = result[0]
            if (math.pi*2 / result[1][1] <= 1e4):
                x_coordinates.append(math.pi*2 / result[1][1])
            else:
                step *= 4
            print(f"errore quadratico: {results[-1][0]}")
            print(f"pulsazione: {results[-1][1][1]}")
            print(f"periodo: {math.pi*2 / results[-1][1][1]}")
            if (len(results) > 1 and math.isclose(
                math.pi*2 / results[-1][1][1], math.pi
                    * 2 / results[-2][1][1],
                    abs_tol=1e-1, rel_tol=1e-1)
                    or math.isclose(period, math.pi*2 / results[-1][1][1],
                                    rel_tol=1e-1)):
                step *= 4
            elif (step > STARTING_STEP):
                step = STARTING_STEP
            print(f"step: {step}\n")
            period += step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    utopicX = np.median(x_coordinates)
    plotter(results, utopicX, utopicY)
    return (results, utopicX, utopicY)


def dist(pointA: tuple, pointB: tuple) -> float:
    return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)


def plotter(results, x, y) -> None:
    x_coordinates = []
    y_coordinates = []
    for result in results:
        if math.pi*2 / result[1][1] <= 1e4:
            x_coordinates.append(abs(math.pi*2 / result[1][1]))
            y_coordinates.append(result[0])
    plt.scatter(x_coordinates, y_coordinates)
    plt.scatter([x], [y])
    plt.show()


def utopicLine(results: tuple) -> dict:
    optimal = [0]
    value = 999999
    for result in results[0]:
        currentVal = dist((math.pi*2 / result[1][1], result[0]),
                          (results[1], results[2]))
        if currentVal < value:
            value = currentVal
            optimal = result
    return optimal


if __name__ == '__main__':
    test = pd.DataFrame(generateValues(4, 0.009, 3*math.pi/2, 10))
    dataframe = reader.getRangeValues(0, reader.getNumValues()).iloc[:, 0: 2]
    result = utopicLine(optimizeCol(test, algorithm=nlopt.LN_COBYLA))
    print(f"errore quadratico: {result[0]}")
    print(f"pulsazione: {result[1][1]}")
    print(f"periodo: {math.pi*2 / result[1][1]}")
