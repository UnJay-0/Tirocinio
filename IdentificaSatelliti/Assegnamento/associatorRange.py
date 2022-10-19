import pandas as pd
import matplotlib.pyplot as plt
import nlopt
import math
import time
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues, generateValuesError
from .solCollector import SolCollector, ErrorStandards


reader = valReader("IdentificaSatelliti/values.csv")
STARTING_TOL = 1e-6
STARTING_STEP = 1
testing = []
solver = "knitro"


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


def amplOptCol(col: pd.core.frame.DataFrame, algorithm=solver):
    data = writeValues(col)
    data["minMax"] = True
    ranges = [1000, 2000, 3000, 4000, 5000]
    # ranges = [12, 24]
    multiplier = 0
    currentRange = [0, 0]
    sol = SolCollector()
    for r in ranges:
        currentRange = [r - 1000 + 0.1, r]
        # currentRange = [r - 12 + 0.1, r]
        data["minMax"] = True
        data["fixedA"] = None
        data["multiplier"] = multiplier
        setDataAmpl(currentRange, data)
        result = interpolation(data, algorithm=algorithm)
        sol.insert(result)
        testing.append(result)
        while (currentRange[1] - currentRange[0]) > 50:
            # print("\nMINIMO")
            # print(f"\nintervallo: [{currentRange[0]}, {currentRange[1]}]")
            # print(f"errore quadratico: {result[0]}")
            # print(f"ampiezza: {result[1][0]}")
            # print(f"pulsazione: {result[1][1]}")
            # print(f"periodo: {math.pi*2 / result[1][1]}\n")

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
                                 rel_tol=1e-1, abs_tol=1e-1))):
                break

            # test intervallo inferiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((currentRange[0], solPeriod), data)
            data["init"] = 2*math.pi / solPeriod
            resultInf = interpolation(data, algorithm=algorithm)
            sol.insert(resultInf)
            testing.append(resultInf)

            # print("INFERIORE")
            # print(f"\nintervallo: [{currentRange[0]}, {solPeriod}]")
            # print(f"errore quadratico: {resultInf[0]}")
            # print(f"ampiezza: {resultInf[1][0]}")
            # print(f"pulsazione: {resultInf[1][1]}")
            # print(f"periodo: {math.pi*2 / resultInf[1][1]}\n")

            # test intervallo superiore
            data["minMax"] = True
            data["fixedA"] = None
            setDataAmpl((solPeriod, currentRange[1]), data)
            data["init"] = 2*math.pi / solPeriod
            resultSup = interpolation(data, algorithm=algorithm)
            sol.insert(resultSup)
            testing.append(resultSup)

            # print("SUPERIORE")
            # print(f"\nintervallo: [{solPeriod}, {currentRange[1]}]")
            # print(f"errore quadratico: {resultSup[0]}")
            # print(f"ampiezza: {resultSup[1][0]}")
            # print(f"pulsazione: {resultSup[1][1]}")
            # print(f"periodo: {math.pi*2 / resultSup[1][1]}\n")

            if resultInf[0] < resultSup[0]:
                currentRange = (currentRange[0], solPeriod - solPeriod * 1e-1)
            else:
                currentRange = (solPeriod + solPeriod * 1e-1, currentRange[1])
        multiplier += 1
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


def plotter(results, lv) -> None:
    x_coordinates = []
    y_coordinates = []
    for result in results:
        if ErrorStandards.rangeOf(result[0]) == lv and not(result[0] == 0.0):
            x1 = abs(math.pi*2 / result[1][1])
            y1 = result[0]
            dominance = False
            print(
                f"\nerrore quadratico: {result[0]}\nperiodo: {math.pi*2 / result[1][1]}\nampiezza: {result[1][0]}\n\n")
            for result2 in results:
                if ErrorStandards.rangeOf(result2[0]) == lv and not(result2[0] == 0.0):
                    if (x1 < abs(math.pi*2 / result2[1][1])
                            and y1 < result2[0]):
                        dominance = True
                        print(
                            f"ESCLUSO CON \nerrore quadratico: {result2[0]}\nperiodo: {math.pi*2 / result2[1][1]}\n")
                        break
            if not(dominance):
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
    plt.ylabel('Errore [m^2]')
    plt.scatter(x_coordinates, y_coordinates)
    plt.show()


def num_intorno(puls) -> int:
    count = 0
    for sol in testing:
        period = 2*math.pi / sol[1][1]
        solPeriod = 2*math.pi / puls
        if period >= solPeriod - 100 and period <= solPeriod+100:
            count += 1
    return count


def compute(puls: float, algorithm: int) -> None:
    punti = 10
    test = pd.DataFrame(generateValuesError(1, puls, 0, punti, 5))
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
    #     out.write(string)

    plotter(testing, ErrorStandards.rangeOf(result[0]))
    print(string)
    plotter2(testing)


if __name__ == '__main__':
    puls = [0.8,  0.0125, 0.005024, 0.0013]
    # puls = [1, 0.8, 0.348, 0.28]  # 6.28, 7.8, 18, 22
    for el in puls:
        compute(el, 0)
