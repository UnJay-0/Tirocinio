import pandas as pd
import math
import time
import nlopt
import numpy as np
from itertools import permutations as perm
from itertools import product as prod
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
"""
Overview
-------------------
Fornisce un insieme di metodi statici per l'associazione di valori in base
al risultato dell'interpolazione.
"""

STARTING_TOL = 1e-6
STARTING_STEP = 0.1
MAX_NON_UPGRADE = 10
reader = valReader(
    "IdentificaSatelliti/values.csv")


def obtainOptimal(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    pass


def indexTranslator(index: list) -> list:
    coord = []
    for perms in index:
        colindex = []
        for i in perms:
            colindex.append(valReader.translateSat(i)[0])
            colindex.append(valReader.translateSat(i)[1])
        coord.append(colindex)
    return coord


def dataframePermutations(numSat: int) -> list:
    colPerms = perm(i for i in range(numSat))
    return indexTranslator(colPerms)


def leafPermutations(dataframe: np.ndarray, i=0) -> np.ndarray:
    if i == len(dataframe) - 1:
        return np.array([el
                         for el in dataframePermutations(dataframe.shape[1])])
    result = []
    for val in prod(dataframePermutations(dataframe.shape[1]),
                    leafPermutations(dataframe, i + 1)):
        # for el in dataframePermutations(dataframe.shape[1]):
        #    for els in leafPermutations(dataframe, i + 1):
        result.append(np.vstack((val[0], val[1])))
    return np.array(result)


def heapPermute(L, length):
    if length == 1:
        yield L
    else:
        length -= 1
        for i in range(length):
            for L in heapPermute(L, length):
                yield L
            if length % 2:
                L[i], L[length] = L[length], L[i]
            else:
                L[0], L[length] = L[length], L[0]
            for L in heapPermute(L, length):
                yield L


def writeValues(values: pd.core.frame.DataFrame) -> dict:
    dataValues = {"numeroPunti": int(values.index.size/2),
                  "y": [], "t": [], "b": STARTING_STEP}
    colLabels = values.columns.tolist()
    for label in colLabels:
        if label.find("x") != -1:
            dataValues["t"] = values[label]
        else:
            dataValues["y"] = values[label]
    return dataValues


def optimizeCol(col: pd.core.frame.DataFrame, algorithm=25, maxtime=0.05) -> float:
    step = STARTING_STEP
    optimalValue = 99999
    data = writeValues(col)
    i = 0
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    while(not(math.isclose(optimalValue, 0, abs_tol=1e-6, rel_tol=1e-6))
          and i < MAX_NON_UPGRADE):
        result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                               maxtime=maxtime, algorithm=algorithm)
        if result[0] < optimalValue:
            optimalValue = result[0]
        else:
            i += 1
        data["b"] += step
        if result[3] == 6:
            if not math.isclose(ftol, 1e-1):
                ftol = ftol * 10
                xtol = xtol * 10
            elif not math.isclose(step, 0.01):
                step = 0.01
                data["b"] = 0.01
        print(f"opt: {optimalValue}\nb: {data['b']}")
    return optimalValue


def generateValues(a, w, f) -> dict:
    dataValues = {}
    t = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    y = []
    for i in t:
        y.append(a * math.sin(w * i + f))
    dataValues['x0'] = t
    dataValues['y0'] = y
    return dataValues


if __name__ == '__main__':
    start = time.time()

    # Grab Currrent Time After Running the Code
    # dataValues = generateValues(4, 2, math.pi)

    # dataframe = pd.DataFrame(dataValues)
    # print(f"opt val: {optimizeCol(dataframe, algorithm=nlopt.LN_BOBYQA)}")

    read = valReader("IdentificaSatelliti/values.csv")

    dataframe = read.getRangeValues(0, read.getNumValues())
    rows = [n for n in range(10)]
    index = []
    for i in range(1):
        index.append(rows)
    for el in heapPermute(rows, len(rows)):
        print(indexTranslator(el))

    end = time.time()

    # Subtract Start Time from The End Time
    total_time = end - start
    print(f"computational time: {str(total_time)}")
