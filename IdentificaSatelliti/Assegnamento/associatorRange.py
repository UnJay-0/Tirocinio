import pandas as pd
import matplotlib.pyplot as plt
import nlopt
import math
import time
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues
from .solCollector import SolCollector, ErrorStandards


reader = valReader("IdentificaSatelliti/values.csv")
STARTING_TOL = 1e-6
STARTING_STEP = 1
testing = []


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
    result = ()
    oldResult = ()
    sol = SolCollector()
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    k = 5
    while period < 5e3:
        data["b"] = period
        data["init"] = 2 * math.pi / \
            (data["b"] + ((5e3 - data["b"]) / 2))  # (data[b])
        print(f"periodo: {period}")
        try:
            oldResult = result
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            print(f"periodo iniziale: {(data['b'] + ((5e3 - data['b']) / 2))}")
            print(f"errore quadratico: {result[0]}")
            print(f"pulsazione: {result[1][1]}")
            print(f"periodo: {math.pi*2 / result[1][1]}")
            sol.insert(result)
            testing.append(result)
            if (oldResult != () and math.isclose(
                math.pi*2 / result[1][1], math.pi
                    * 2 / oldResult[1][1], rel_tol=1e-1)  # ):
                # or math.isclose(period, math.pi*2 / result[1][1],
                #                 rel_tol=1e-2)
                    or ErrorStandards.rangeOf(result[0]) >= 5):
                step *= k
            elif (step > STARTING_STEP):
                step = step / k
            if (step < STARTING_STEP):
                step = STARTING_STEP
            print(f"step: {step}\n")
            period += step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    return sol.getSol()


def plotter(results, lv) -> None:
    x_coordinates = []
    y_coordinates = []
    for result in results:
        if ErrorStandards.rangeOf(result[0]) == lv:
            x_coordinates.append(abs(math.pi*2 / result[1][1]))
            y_coordinates.append(result[0])
    plt.xlabel('Periodo [s]')
    plt.ylabel('Errore')
    plt.scatter(x_coordinates, y_coordinates)
    plt.show()


def plotter2(results) -> None:
    x_coordinates = []
    y_coordinates = []
    for result in results:
        x_coordinates.append(abs(math.pi*2 / result[1][1]))
        y_coordinates.append(result[0])
    plt.xlabel('Periodo [s]')
    plt.ylabel('Errore')
    plt.scatter(x_coordinates, y_coordinates)
    plt.show()


def compute(puls: float, algorithm: int) -> None:
    punti = 30
    test = pd.DataFrame(generateValues(1, puls, 0, punti))
    start = time.time()
    result = optimizeCol(test, algorithm=algorithm)
    end = time.time()
    total_time = end - start
    string = ''
    string += f"\nPULSAZIONE: {puls} {punti}\n" + \
        f"errore quadratico: {result[0]}\n" + \
        f"pulsazione: {result[1][1]}\n" + \
        f"periodo: {math.pi*2 / result[1][1]}\n" + \
        f"computational time: {str(total_time)}\n"
    # with open('output3.txt', "a") as out:
    #    out.write(string)
    print(string)

    # plotter(testing, ErrorStandards.rangeOf(result[0]))
    plotter2(testing)


if __name__ == '__main__':
    puls = [0.8, 0.0125, 0.005, 0.0013, 0.0010]
    for el in puls:
        compute(el, nlopt.LN_COBYLA)
