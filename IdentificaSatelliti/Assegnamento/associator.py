import pandas as pd
import math
import time
import nlopt
from .permutation import dataframePerm, leafPerm
import numpy as np
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
LEAF_SIZE = 3
reader = valReader(
    "IdentificaSatelliti/values.csv")


def obtainOptimal(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    if values.shape[0] < LEAF_SIZE:
        return leafOptimal(values)
    return nodeOptimal(
            obtainOptimal(values.iloc[0:values.shape[0] // 2, ]),
            obtainOptimal(values.iloc[values.shape[0] // 2:, ]))


def nodeOptimal(values1: pd.core.frame.DataFrame,
                values2: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    optimalPerm = (0, 99999)
    for perm in dataframePerm(values2, reader.getNumSat()):
        perm.columns = values1.columns
        temp = pd.concat([values1, perm])
        optimalValues = []
        print(temp)
        i = 0
        while i < reader.getNumSat() * 2:
            print(temp.iloc[:, i:i+2])
            optimalValues.append(optimizeCol(temp.iloc[:, i:i+2]))
            i += 2
        median = np.median(optimalValues)
        if (optimalPerm[1] > median):
            optimalPerm = (temp, median)
    return optimalPerm[0]


def leafOptimal(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    optimalPerm = (0, 99999)
    for perm in leafPerm(values):
        optimalValues = []
        for i in range(reader.getNumSat()):
            print(perm)
            optimalValues.append(optimizeCol(perm.iloc[:, i:i+2]))
        median = np.median(optimalValues)
        if (optimalPerm[1] > median):
            optimalPerm = (perm, median)
    return optimalPerm[0]


def writeValues(values: pd.core.frame.DataFrame) -> dict:
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
                algorithm=nlopt.LN_COBYLA, maxtime=0.05) -> float:
    step = STARTING_STEP
    optimalValue = 99999
    data = writeValues(col)
    print(data)
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
    return optimalValue


def generateValues(a, w, f) -> dict:
    dataValues = {}
    t = [0, 1, 2, 3, 4]
    y = []
    for i in t:
        y.append(a * math.sin(w * i + f))
    dataValues['x0'] = t
    dataValues['y0'] = y
    return dataValues


if __name__ == '__main__':
    start = time.time()
    # Grab Currrent Time After Running the Code
    dataValues = generateValues(4, 2, math.pi)

    dataframe = pd.DataFrame(dataValues)
    # print(f"opt val: {optimizeCol(dataframe, algorithm=nlopt.LN_BOBYQA)}")

    # dataframe = reader.getRangeValues(0, reader.getNumValues())
    # print(nodeOptimal(dataframe.iloc[0:dataframe.shape[0] // 2, ],
    #                   dataframe.iloc[dataframe.shape[0] // 2:, ]))
    test = obtainOptimal(dataframe)
    print(test)
    end = time.time()

    # Subtract Start Time from The End Time
    total_time = end - start
    print(f"computational time: {str(total_time)}")
