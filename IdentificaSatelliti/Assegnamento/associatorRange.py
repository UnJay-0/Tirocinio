import pandas as pd
import nlopt
import math
import time
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues
from .solCollector import SolCollector


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
    result = ()
    oldResult = ()
    sol = SolCollector()
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    while period < 5e3:
        data["b"] = period
        # print(f"periodo: {period}")
        try:
            oldResult = result
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            # print(f"errore quadratico: {result[0]}")
            # print(f"pulsazione: {result[1][1]}")
            # print(f"periodo: {math.pi*2 / result[1][1]}")
            sol.insert(result)
            if (oldResult != () and math.isclose(
                math.pi*2 / result[1][1], math.pi
                    * 2 / oldResult[1][1], rel_tol=1e-1)
                    or math.isclose(period, math.pi*2 / result[1][1],
                                    rel_tol=1e-2)
                    or SolCollector.rangeOf(result[0]) >= 6):
                step *= 2
            elif (step > STARTING_STEP):
                step = STARTING_STEP
            # print(f"step: {step}\n")
            period += step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    return sol.getSol()


if __name__ == '__main__':
    test = pd.DataFrame(generateValues(1, 0.005, 0, 30))
    dataframe = reader.getRangeValues(0, reader.getNumValues()).iloc[:, 0: 2]
    start = time.time()
    result = optimizeCol(test, algorithm=nlopt.LN_COBYLA)
    end = time.time()
    print(f"errore quadratico: {result[0]}")
    print(f"pulsazione: {result[1][1]}")
    print(f"periodo: {math.pi*2 / result[1][1]}")

    total_time = end - start
    print(f"computational time: {str(total_time)}")
