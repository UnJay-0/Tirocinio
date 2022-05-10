import pandas as pd
import math
import nlopt
from .permutation import dataframePerm, leafPerm, shuffleValues
from numpy import median
from ..Interpolazione.client import interpolation
from .valuesReader import valReader
from .valuesWriter import generateValues
"""
Overview
-------------------
Fornisce un insieme di metodi statici per l'associazione di valori in base
al risultato dell'interpolazione.
"""

STARTING_TOL = 1e-6
STARTING_STEP = 0.1
MAX_NON_UPGRADE = 10
LEAF_STOPPING_CRITERIA = 1e-1
NODE_STOPPING_CRITERIA = 0.1
reader = valReader("IdentificaSatelliti/values.csv")
LEAF_SIZE = valReader.leafSize(reader.getNumValues())
THRESHOLD = 3
WHEN_SHUFFLE = reader.getNumSat()


def obtainOptimal(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Overview
    ------------
    Associa i punti dati in maniera tale che i punti situati nella stessa
    colonna interpolino in maniera ottima una sinusoide. Devono essere presenti
    almeno due o più colonne (x, y) nel dataframe passato per parametro.

    Params
    ------------
        values (Dataframe): dataframe contenente le n osservazioni effettuate e
                            k punti per osservazione.

    Returns
    ------------
    DataFrame - Restituisce un dataframe dove i punti situati nella stessa
                colonna interpolano in maniera ottima una sinusoide.

    """
    if values.shape[0] <= LEAF_SIZE:
        print(f"foglia:\n {values}")
        return leafOptimal(values)
    print(f"nodo 1:\n {values.iloc[0:values.shape[0] // 2, ]}")
    print(f"nodo 2:\n {values.iloc[values.shape[0] // 2:, ]}")
    return nodeOptimal(
            obtainOptimal(values.iloc[0:values.shape[0] // 2, :]),
            obtainOptimal(values.iloc[values.shape[0] // 2:, :]))


def nodeOptimal(values1: pd.core.frame.DataFrame,
                values2: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Overview
    -------------------
    Associa le colonne di values2 alle colonne di values1 in maniera tale che
    interpolino in maniera ottima una sinusoide. il numero di colonne di
    values1 deve essere pari al numero di colonne di values2.

    Params
    -------------------
    values1 (DataFrame) - primo dataframe di n osservazioni
                          e k colonne di punti.
    values2 (DataFrame) - secondo dataframe di m osservazioni
                          e k colonne di punti.

    Returns
    -------------------
     Dataframe - unione di values1 e values2 in maniera tale che le colonne
                 interpolino in maniera ottima una sinusoide

    """
    optimalDataframe = pd.DataFrame()
    optimalcol = [0, 0, 99999]
    gen = dataframePerm(values2, values2.shape[1] // 2)
    while True:
        try:
            perm = next(gen)
        except StopIteration:
            optimalDataframe = pd.concat(
                [optimalDataframe, optimalcol[1]], axis=1)
            values1.drop(labels=optimalcol[1], axis=1, inplace=True)
            perm = optimalcol[0]
            perm.drop(labels=optimalcol[1], axis=1, inplace=True)
            gen = dataframePerm(perm, perm.shape[1] // 2)
            optimalcol = [0, 0, 99999]
            if perm.shape[1] == 2:
                optimalDataframe = pd.concat(
                    [optimalDataframe, pd.concat([values1, perm])], axis=1)
                return optimalDataframe
        perm.columns = values1.columns
        temp = pd.concat([values1, perm])
        i = 0
        while i < temp.shape[1]:
            print(f"permutazione nodo ordinaria\n{temp}")
            print(f" colonna \n{temp.iloc[:, i:i+2]}")
            colValue = optimizeCol(temp.iloc[:, i:i+2])
            print(f"valore: {colValue}")
            if (colValue < NODE_STOPPING_CRITERIA):
                optimalDataframe = pd.concat(
                    [optimalDataframe, temp.iloc[:, i:i+2]],
                    axis=1)
                print(f"in costruzione\n{optimalDataframe}")
                values1.drop(values1.iloc[:, i:i+2], axis=1, inplace=True)
                perm.drop(perm.iloc[:, i:i+2], axis=1, inplace=True)
                gen = dataframePerm(perm, perm.shape[1] // 2)
                optimalcol = [0, 0, 99999]
                if perm.shape[1] == 2:
                    optimalDataframe = pd.concat(
                        [optimalDataframe, pd.concat([values1, perm])], axis=1)
                    return optimalDataframe
                break
            if colValue < optimalcol[2]:
                optimalcol = [perm, temp.iloc[:, i:i+2], colValue]
            i += 2
    return optimalDataframe


def leafOptimal(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    """
    Overview
    -------------------
    Associa i punti di values in maniera tale che interpolino in maniera
    ottima una sinusoide.

    Params
    -------------------
    values (Dataframe) - dataframe di n osservazioni e k colonne di punti.

    Returns
    -------------------
    DataFrame - Restituisce un dataframe dove i punti situati nella stessa
                colonna interpolano in maniera ottima una sinusoide.

    """
    optimalDataframe = pd.DataFrame()
    if values.shape[0] == 1:
        return values
    gen = leafPerm(values)
    optimalcol = [0, 0, 99999]
    n_shuffle = WHEN_SHUFFLE
    shuffle_i = 0
    while True:
        try:
            perm = next(gen)
        except StopIteration:
            optimalDataframe = pd.concat(
                [optimalDataframe, optimalcol[1]], axis=1)
            perm = optimalcol[0].drop(optimalcol[1], axis=1, inplace=False)
            gen = leafPerm(perm)
            n_shuffle = perm.shape[1]
            shuffle_i = 0
            optimalcol = [0, 0, 99999]
            if(perm.shape[1] == 2):
                optimalDataframe = pd.concat(
                    [optimalDataframe, perm], axis=1)
                return optimalDataframe
        print(f"permutazione ordinaria\n {perm}")
        i = 0
        permValues = []
        while i < perm.shape[1]:
            colValue = optimizeCol(perm.iloc[:, i:i+2])
            permValues.append(colValue)
            print(f"valore: {colValue}")
            if (colValue < LEAF_STOPPING_CRITERIA):
                optimalDataframe = pd.concat(
                    [optimalDataframe, perm.iloc[:, i:i+2]], axis=1)
                perm.drop(perm.iloc[:, i:i+2], axis=1, inplace=True)
                n_shuffle = perm.shape[1]
                shuffle_i = 0
                optimalcol = [0, 0, 99999]
                if(perm.shape[1] == 2):
                    optimalDataframe = pd.concat(
                        [optimalDataframe, perm], axis=1)
                    return optimalDataframe
                print(f"in costruzione\n{optimalDataframe}")
                gen = leafPerm(perm)
                break
            elif colValue < optimalcol[2]:
                optimalcol = [perm, perm.iloc[:, i:i+2], colValue]
            i += 2
        print(f"mediana: {median(permValues)}")
        if median(permValues) > THRESHOLD:
            shuffle_i += 1
        print(f"shuffle i: {shuffle_i}")
        if shuffle_i >= n_shuffle and perm.shape[1] > 4:
            print("shuffle")
            gen = leafPerm(shuffleValues(perm))
            shuffle_i = 0

    return optimalDataframe


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
                algorithm=nlopt.LN_COBYLA, maxtime=0.05) -> list:
    """
    Overview
    -------------------
    Calcola la sinusoide che interpola i punti passati per parametro.
    La sinusoide calcolata è la sinusoide che interpola i punti con minimo
    errore e massimo periodo.

    Params
    -------------------
    col (DataFrame) - Colonna (x, y) con i punti da interpolare
    algorithm (int) - intero identificativo di un algoritmo specificato
                      all'interno del modulo nlopt.
    maxtime (float) - tempo massimo di elaborazione [s].

    Returns
    -------------------
    float - L'errore complessivo della sinusoide rispetto ai punti.

    """
    step = 1
    period = 1
    results = []
    data = writeValues(col)
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    while period < 100:
        data["b"] = period
        print(f"periodo: {period}")
        try:
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
            if not math.isclose(math.pi*2 / result[1][1],
                                period + 10, rel_tol=1e-1):
                results.append(result)
                print(f"errore quadratico: {results[-1][0]}")
                print(f"pulsazione: {results[-1][1][1]}")
                print(f"periodo: {math.pi*2 / results[-1][1][1]}")
                if (len(results) > 1 and math.isclose(
                    math.pi*2 / results[-1][1][1], math.pi
                        * 2 / results[-2][1][1],
                        abs_tol=1e-1, rel_tol=1e-1)):
                    step *= 2
                elif (step > STARTING_STEP):
                    step = STARTING_STEP
            print(f"step: {step}\n")
            period += step
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
    return utopicLine(results)


def dist(pointA: tuple, pointB: tuple) -> float:
    return math.sqrt((pointA[0] - pointB[0])**2 + (pointA[1] - pointB[1])**2)


def utopicLine(results: tuple):
    optimal = [0]
    value = 999999
    for result in results:
        if result[0] < value:
            value = result[0]
            optimal = result
    print(f"errore quadratico: {optimal[0]}")
    print(f"pulsazione: {optimal[1][1]}")
    print(f"periodo: {math.pi*2 / optimal[1][1]}")
    return optimal[0]


if __name__ == '__main__':
    test = pd.DataFrame(generateValues(1, 10, 0, 10))
    print(optimizeCol(test))
