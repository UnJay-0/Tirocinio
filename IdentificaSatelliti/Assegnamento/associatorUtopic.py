import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import nlopt
import math
import time
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
    errore = 50
    results = []
    result = ()
    oldResult = ()
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    x_coordinates = []
    while errore > 0:
        data["b"] = errore
        # print(f"periodo: {period}")
        try:
            oldResult = result
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            # print(f"errore quadratico: {result[0]}")
            # print(f"pulsazione: {result[1][1]}")
            # print(f"periodo: {math.pi*2 / result[1][1]}")
            results.append(result)

            if (len(results) > 1 and (math.isclose(
                math.pi*2 / result[1][1], math.pi
                    * 2 / oldResult[1][1], rel_tol=1e-1))):
                step *= 2
            elif (step > STARTING_STEP):
                step = STARTING_STEP
            # print(f"step: {step}\n")
            errore -= step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    print(f"numero risultati: {len(results)}")
    utopicX = np.mean(x_coordinates)
    return (results, utopicX, 0)


def dist(pointA: tuple, pointB: tuple) -> float:
    return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)


def plotter(results, x, y) -> None:
    x_coordinates = []
    y_coordinates = []
    for result in results:
        if math.pi*2 / result[1][1] <= 1e5:
            x_coordinates.append(abs(math.pi*2 / result[1][1]))
            y_coordinates.append(result[0])
    plt.scatter(x_coordinates, y_coordinates)
    # plt.scatter([x], [y])


def utopic(results: tuple) -> dict:
    optimal = [0]
    value = 999999
    for result in results[0]:
        currentVal = dist((math.pi*2 / result[1][1], result[0]),
                          (results[1], 0))
        if currentVal < value:
            value = currentVal
            optimal = result
    return optimal


def num_sol(period: float, results: list) -> int:
    counter = 0
    for result in results:
        if (math.pi*2 / result[1][1] > period - 50
                and math.pi*2 / result[1][1] < period + 50):
            counter += 1
    return counter


def compute(puls: float, algorithm: int) -> None:
    print(f"PULSAZIONE: {puls}")
    test = pd.DataFrame(generateValues(1, puls, 0, 30))
    start = time.time()

    results = optimizeCol(test, algorithm=algorithm)
    result = utopic((results[0], math.pi*2/puls, 0))

    end = time.time()
    # plt.scatter([math.pi*2 / result[1][1]], [0], c='red')  # soluzione "giusta"
    result = utopic(results)
    print(
        f"numero di sol nell'intorno: {num_sol(math.pi*2 / puls, results[0])}")
    print(f"numero di soluioni {len(result)}")
    # plt.scatter([math.pi*2 / result[1][1]], [0], c='blue')  # soluzione scelta
    # plt.scatter([results[1]], [results[2]], c='purple')  # punto utopia
    # plt.scatter([math.pi*2/puls], [0], c='green')  # punto sinusoide
    # plotter(results[0], results[1], 0)
    # plt.xlabel('Periodo [s]')
    # plt.ylabel('Errore[m^2]')
    # plt.show()
    print(f"errore quadratico: {result[0]}")
    print(f"pulsazione: {result[1][1]}")
    print(f"periodo: {math.pi*2 / result[1][1]}")

    total_time = end - start
    print(f"computational time: {str(total_time)}\n")


if __name__ == '__main__':
    inits = [0.0025, 0.0017, 0.0015]
    solvers = [nlopt.LN_COBYLA,  nlopt.LN_BOBYQA,
               nlopt.LN_PRAXIS, nlopt.LN_NEWUOA, nlopt.LN_SBPLX]
    for solver in solvers:
        for init in inits:
            col = pd.DataFrame(generateValues(1, 0.0013, 0, 10))
            data = writeValues(col)
            data["b"] = 1e-5
            data["init"] = init
            result = interpolation(data, ftol_rel=1e-6, xtol_rel=1e-6,
                                   maxtime=0.05, algorithm=solver)
            val = 0
            for err in result[1][3:]:
                val += err**2
            val = val / len(result[1][3:])
            string = ''
            string += f"\nPULSAZIONE: {init} {solver}\n" + \
                f"errore quadratico: {val}\n" + \
                f"pulsazione: {result[1][1]}\n" + \
                f"periodo: {math.pi*2 / result[1][1]}\n"
            print(string)
            # with open('output_vincolo.txt', "a") as out:
            #     out.write(string)
    # puls = [0.8, 0.0125, 0.005, 0.0013, 0.0010]
    # for el in puls:
    #     compute(el, nlopt.LN_COBYLA)
