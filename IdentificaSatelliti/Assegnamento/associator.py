import pandas as pd
import math
import nlopt
from .permutation import dataframePerm, leafPerm, shuffleValues
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
LEAF_STOPPING_CRITERIA = 1e-2
NODE_STOPPING_CRITERIA = 0.1
reader = valReader("IdentificaSatelliti/values.csv")
LEAF_SIZE = valReader.leafSize(reader.getNumValues())
ROW = 3
WHEN_SHUFFLE = math.factorial(reader.getNumSat()) ** ROW


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
            print(f"primo dataframe: {values1}")
            print(f"secondo dataframe: {perm}")
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
        shuffle_i += 1
        try:
            perm = next(gen)
        except StopIteration:
            optimalDataframe = pd.concat(
                [optimalDataframe, optimalcol[1]], axis=1)
            perm = optimalcol[0].drop(optimalcol[1], axis=1, inplace=False)
            gen = leafPerm(perm)
            n_shuffle = math.factorial(perm.shape[1]) ** ROW
            shuffle_i = 0
            optimalcol = [0, 0, 99999]
            if(perm.shape[1] == 2):
                optimalDataframe = pd.concat(
                    [optimalDataframe, perm], axis=1)
                return optimalDataframe
        print(f"permutazione ordinaria\n {perm}")
        i = 0
        while i < perm.shape[1]:
            colValue = optimizeCol(perm.iloc[:, i:i+2])
            print(f"valore: {colValue}")
            if (colValue < LEAF_STOPPING_CRITERIA):
                optimalDataframe = pd.concat(
                    [optimalDataframe, perm.iloc[:, i:i+2]], axis=1)
                perm.drop(perm.iloc[:, i:i+2], axis=1, inplace=True)
                n_shuffle = math.factorial(perm.shape[1]) ** ROW
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
            elif shuffle_i == n_shuffle and perm.shape[1] > 4:
                print("shuffle")
                gen = leafPerm(shuffleValues(perm))
                shuffle_i = 0
            i += 2

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
                algorithm=nlopt.LN_COBYLA, maxtime=0.04) -> float:
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
    step = STARTING_STEP
    optimalValue = 99999
    data = writeValues(col)
    i = 0
    ftol = STARTING_TOL
    xtol = STARTING_TOL
    while(not(math.isclose(optimalValue, 0, abs_tol=1e-6, rel_tol=1e-6))
          and i < MAX_NON_UPGRADE):
        try:
            result = interpolation(data, ftol_rel=ftol, xtol_rel=xtol,
                                   maxtime=maxtime, algorithm=algorithm)
        except nlopt.RoundoffLimited:
            ftol = ftol * 10
            xtol = xtol * 10
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
            else:
                return optimalValue
    return optimalValue
    return optimalValue
