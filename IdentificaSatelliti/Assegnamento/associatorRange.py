import pandas as pd
# import matplotlib.pyplot as plt
import nlopt
import math
import time
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues
from .solCollector import SolCollector, ErrorStandards
from .initValueGen import InitValueGen


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
    result = ()
    result = amplOptCol(col)
    return result


def amplOptCol(col: pd.core.frame.DataFrame, algorithm="snopt"):
    data = writeValues(col)
    data["minMax"] = True
    ranges = [1000, 2000, 3000, 4000, 5000]
    currentRange = [0, 0]
    sol = SolCollector()
    for r in ranges:
        currentRange = [r - 1000 + 0.1, r]
        while (currentRange[1] - currentRange[0]) > 10:
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl(currentRange, data)
            result = interpolation(data, algorithm=algorithm)
            sol.insert(result)
            print("\nMINIMO")
            print(f"\nintervallo: [{currentRange[0]}, {currentRange[1]}]")
            print(f"errore quadratico: {result[0]}")
            print(f"ampiezza: {result[1][0]}")
            print(f"pulsazione: {result[1][1]}")
            print(f"periodo: {math.pi*2 / result[1][1]}\n")

            data["minMax"] = False
            data["fixedA"] = result[1][0]
            result = interpolation(data, algorithm=algorithm)
            sol.insert(result)
            print("\nMASSIMO")
            print(f"\nintervallo: [{currentRange[0]}, {currentRange[1]}]")
            print(f"errore quadratico: {result[0]}")
            print(f"ampiezza: {result[1][0]}")
            print(f"pulsazione: {result[1][1]}")
            print(f"periodo: {math.pi*2 / result[1][1]}\n")
            solPeriod = 2*math.pi / result[1][1]

            if (int(solPeriod) == int(currentRange[0])
                    or int(solPeriod) == int(currentRange[1])):
                break

            # test intervallo inferiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((currentRange[0], solPeriod), data)
            resultInf = interpolation(data, algorithm=algorithm)
            sol.insert(resultInf)

            print("INFERIORE")
            print(f"\nintervallo: [{currentRange[0]}, {solPeriod}]")
            print(f"errore quadratico: {resultInf[0]}")
            print(f"ampiezza: {resultInf[1][0]}")
            print(f"pulsazione: {resultInf[1][1]}")
            print(f"periodo: {math.pi*2 / resultInf[1][1]}\n")

            # test intervallo superiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((solPeriod, currentRange[1]), data)
            resultSup = interpolation(data, algorithm=algorithm)
            sol.insert(resultInf)

            print("SUPERIORE")
            print(f"\nintervallo: [{solPeriod}, {currentRange[1]}]")
            print(f"errore quadratico: {resultSup[0]}")
            print(f"ampiezza: {resultSup[1][0]}")
            print(f"pulsazione: {resultSup[1][1]}")
            print(f"periodo: {math.pi*2 / resultSup[1][1]}\n")

            if resultInf[0] < resultSup[0]:
                currentRange = (currentRange[0], solPeriod - solPeriod * 1e-1)
            else:
                currentRange = (solPeriod + solPeriod * 1e-1, currentRange[1])

    return sol.getSol()


def setDataAmpl(currentRange, data):
    data["init"] = 2*math.pi / (sum(currentRange) / 2)
    data["minMax"] = True
    data["minW"] = 2*math.pi / currentRange[1]
    data["maxW"] = 2*math.pi / currentRange[0]


def modifyPeriod(solPeriod: float, limitPeriod: float, minOrMax: bool) -> float:
    if int(solPeriod) == int(limitPeriod):
        if minOrMax == "min":
            return solPeriod + (solPeriod * 1e-1)
        else:
            return solPeriod - (solPeriod * 1e-1)
    else:
        return solPeriod


def stepOptCol(col: pd.core.frame.DataFrame,
               algorithm=nlopt.LN_COBYLA, maxtime=.05):
    step = 1
    period = 1
    result = ()
    oldResult = ()
    sol = SolCollector()
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    k = 10
    while period < 5000:
        data["b"] = period
        data["init"] = math.pi*2 / period  # per fissare punto di init
        # print(f"periodo: {period}")
        try:
            oldResult = result
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            # print(f"periodo iniziale: {initValue.currentVal}")
            # print(f"errore quadratico: {result[0]}")
            # print(f"pulsazione: {result[1][1]}")
            # print(f"periodo: {math.pi*2 / result[1][1]}\n")
            sol.insert(result)
            # break  # per fissare punto di init
            if (oldResult != () and math.isclose(
                math.pi*2 / result[1][1], math.pi
                    * 2 / oldResult[1][1], rel_tol=1e-1)  # ):
                or math.isclose(period, math.pi*2 / result[1][1],
                                rel_tol=1e-1)
                    or ErrorStandards.rangeOf(result[0]) >= 5):
                step *= k
            elif (step > STARTING_STEP):
                step = step / k
            if (step < STARTING_STEP):
                step = STARTING_STEP
            # print(f"step: {step}\n")
            period += step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    return sol.getSol()


def initOptCol(col: pd.core.frame.DataFrame,
               algorithm=nlopt.LN_COBYLA, maxtime=.05):
    result = ()
    sol = SolCollector()
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    initValue = InitValueGen(4000)
    while initValue.getRange() > 20:
        data["b"] = initValue.getBound()
        data["init"] = 2*math.pi / initValue.currentVal
        try:
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            # print(f"periodo iniziale: {initValue.currentVal}")
            # print(f"errore quadratico: {result[0]}")
            # print(f"pulsazione: {result[1][1]}")
            # print(f"periodo: {math.pi*2 / result[1][1]}\n")
            sol.insert(result)
            # testing.append(result)
            try:
                initValue.genInitVal(math.pi*2 / result[1][1])
            except Exception:
                upperLower = initValue.testUpperLower()
                data["init"] = 2*math.pi / upperLower[0]
                upperResult = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                            maxtime=maxtime,
                                            algorithm=algorithm)
                data["init"] = 2*math.pi / upperLower[1]
                lowerResult = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                            maxtime=maxtime,
                                            algorithm=algorithm)
                sol.insert(upperResult)
                sol.insert(lowerResult)
                if upperResult[0] < lowerResult[0]:
                    try:
                        initValue.genInitVal(math.pi*2 / upperResult[1][1])
                    except Exception:
                        initValue.oldVal = initValue.currentVal
                        initValue.currentVal = math.pi*2 / upperResult[1][1]

                else:
                    try:
                        initValue.genInitVal(math.pi*2 / lowerResult[1][1])
                    except Exception:
                        initValue.oldVal = initValue.currentVal
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    return sol.getSol()


# def plotter(results, lv) -> None:
#     x_coordinates = []
#     y_coordinates = []
#     for result in results:
#         if ErrorStandards.rangeOf(result[0]) == lv:
#             x_coordinates.append(abs(math.pi*2 / result[1][1]))
#             y_coordinates.append(result[0])
#     plt.xlabel('Periodo [s]')
#     plt.ylabel('Errore')
#     plt.scatter(x_coordinates, y_coordinates)
#     plt.show()
#
#
# def plotter2(results) -> None:
#     x_coordinates = []
#     y_coordinates = []
#     for result in results:
#         x_coordinates.append(abs(math.pi*2 / result[1][1]))
#         y_coordinates.append(result[0])
#     plt.xlabel('Periodo [s]')
#     plt.ylabel('Errore [m^2]')
#     plt.scatter(x_coordinates, y_coordinates)
#     plt.show()


def compute(puls: float, algorithm: int) -> None:
    punti = 10
    test = pd.DataFrame(generateValues(6, puls, 0, punti))
    start = time.time()
    result = optimizeCol(test, algorithm=algorithm)
    end = time.time()
    total_time = end - start
    string = ''
    string += f"\nPULSAZIONE: {puls} {punti}\n" + \
        f"errore quadratico: {result[0]}\n" + \
        f"pulsazione: {result[1][1]}\n" + \
        f"ampiezza: {result[1][0]}\n" + \
        f"fase: {result[1][2]}\n" + \
        f"periodo: {math.pi*2 / result[1][1]}\n" + \
        f"computational time: {str(total_time)}\n"
    # with open('output3.txt', "a") as out:
    #    out.write(string)
    print(string)

    # plotter(testing, ErrorStandards.rangeOf(result[0]))
    # plotter2(testing)


if __name__ == '__main__':
    puls = [1]
    for el in puls:
        compute(el, nlopt.LN_COBYLA)
