from itertools import tee
import pandas as pd
import numpy as np
from random import shuffle
from .valuesReader import valReader


def heapPermute(L: np.ndarray, length: int) -> np.ndarray:
    """
    Overview
    -------------------
    Implementazione dell'algoritmo di Heap per il calcolo di tutte
    le permutazioni di un insieme di elementi. Genera un permutazione
    effettuado ad ogni iterazione un solo scambio di posizione tra elementi.
    (generatore)

    Params
    -------------------
    L (ndarray) - array di elementi da permutare.
    length (int) - numero di elementi di L da permutare.

    Returns
    -------------------
    ndarray - permutazione di L

    """
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


def dataframePerm(dataframe: pd.core.frame.DataFrame,
                  numSat: int) -> pd.core.frame.DataFrame:
    """
    Overview
    -------------------
    Genera una permutazione del dataframe dato rispetto alle colonne.
    (generatore)

    Params
    -------------------
    dataframe (DataFrame) - DataFrame da permutare.
    numSat (int) - numero di colonne (x, y) all'interno del dataframe.

    Returns
    -------------------
    DataFrame - permutazione rispetto alle colonne di dataframe

    """
    rows = toIndex(dataframe.columns.to_list())
    for el in heapPermute(np.array(rows), numSat):
        index = indexTranslator(el)
        yield dataframe.reindex(columns=index)


def leafPerm(values: pd.core.frame.DataFrame):
    """
    Overview
    -------------------
    Compone un generatore che permuta gli elementi di ogni riga di values.

    Params
    -------------------
    values (DataFrame) - dataframe da permutare.

    Returns
    -------------------
    generator - generatore che permuta gli elementi di ogni riga di values.

    """
    if values.shape[0] == 1:
        return dataframePerm(values, values.shape[1] // 2)
    else:
        return rowPermGen(values.iloc[0:1, :],
                          leafPerm(values.iloc[1:, :]))


def rowPermGen(currentRow: pd.core.frame.DataFrame, gen):
    """
    Overview
    -------------------
    Generatore che combina il generatore passato per parametro
    con il generatore sulle permutazioni rispetto alle colonne di currentRow.

    Params
    -------------------
    currentRow (DataFrame) - Riga corrente da permutare rispetto alle colonne.
    gen (generator) - generatore di righe permutate rispetto alle colonne.

    Returns
    -------------------
    DataFrame - Unione delle permutazioni di currentRow con le permutazioni
                generate da gen.

    """
    gen, baseGen = tee(gen)
    currentRowGen = dataframePerm(currentRow, currentRow.shape[1] // 2)
    for perm in currentRowGen:
        for insidePerm in baseGen:
            yield stackDataframes(perm, insidePerm)
        gen, baseGen = tee(gen)


def indexTranslator(index: list) -> list:
    """
    Overview
    -------------------
    Traduce una lista di indici da 0 a n, in indici (x0, y0 a xn, yn)

    Params
    -------------------
    index (list) - lista di indici da 0 a n

    Returns
    -------------------
    list - una lista di indici (x0, y0 a xn, yn)

    """
    colindex = []
    for i in index:
        colindex.append(valReader.translateSat(i)[0])
        colindex.append(valReader.translateSat(i)[1])
    return colindex


def toIndex(columns: list) -> list:
    """
    Overview
    -------------------
    Traduce una lista di indici da 0 a n, in indici (x0, y0 a xn, yn)

    Params
    -------------------
    index (list) - lista di indici da 0 a n

    Returns
    -------------------
    list - una lista di indici (x0, y0 a xn, yn)

    """
    index = []
    i = 0
    while i < len(columns):
        index.append(int(columns[i][1]))
        i += 2
    return index


def stackDataframes(*dataframes):
    """
    Overview
    -------------------
    Unisce due o più dataframe rispetto alle colonne.
    I DataFrame passati per parametro devono avere lo stesso numero di colonne.

    Params
    -------------------
    *dataframes (DataFrame) - dataframe da unire.

    Returns
    -------------------
    DataFrame - unione rispetto alle colonne dei dataframe passati
                per parametro.

    """
    columns = dataframes[0].columns
    for df in dataframes:
        df.columns = columns
    return pd.concat(dataframes)


def shuffleValues(values: pd.core.frame.DataFrame) -> pd.core.frame.DataFrame:
    rows = toIndex(values.columns.to_list())
    result = []
    for i in range(values.shape[0]):
        shuffle(rows)
        result.append(
            values.iloc[i:i+1, :].reindex(columns=indexTranslator(rows)))
    return stackDataframes(*result)


if __name__ == '__main__':
    reader = valReader("IdentificaSatelliti/values.csv")
    dataframe = reader.getRangeValues(0, reader.getNumValues())
    print(shuffleValues(dataframe))
