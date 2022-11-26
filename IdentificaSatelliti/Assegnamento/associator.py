import pandas as pd
from .permutation import dataframePerm, leafPerm, shuffleValues
from numpy import median
from .associatorRange import amplOptCol
from .valuesReader import valReader
from .solCollector import ErrorStandards
"""
Overview
-------------------
Fornisce un insieme di metodi statici per l'associazione di valori in base
al risultato dell'interpolazione.
"""

STARTING_TOL = 1e-6
STARTING_STEP = 1
LEAF_STOPPING_CRITERIA = ErrorStandards.LV6.value
NODE_STOPPING_CRITERIA = ErrorStandards.LV4.value
reader = valReader("IdentificaSatelliti/values.csv")
LEAF_SIZE = valReader.leafSize(reader.getNumValues())
THRESHOLD = ErrorStandards.LV8.value
WHEN_SHUFFLE = reader.getNumSat() + 2


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
        return leafOptimal(values)
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
        for i in range(0, temp.shape[1], 2):
            colValue = amplOptCol(temp.iloc[:, i:i+2])[0]
            if (colValue < NODE_STOPPING_CRITERIA):
                optimalDataframe = pd.concat(
                    [optimalDataframe, temp.iloc[:, i:i+2]],
                    axis=1)
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
        permValues = []
        for i in range(0, perm.shape[1], 2):
            colValue = amplOptCol(perm.iloc[:, i:i+2])[0]
            permValues.append(colValue)
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
                gen = leafPerm(perm)
                break
            elif colValue < optimalcol[2]:
                optimalcol = [perm, perm.iloc[:, i:i+2], colValue]
        if median(permValues) > THRESHOLD:
            shuffle_i += 1
        if shuffle_i >= n_shuffle and perm.shape[1] > 4:
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
