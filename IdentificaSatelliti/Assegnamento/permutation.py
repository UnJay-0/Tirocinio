from itertools import tee
import pandas as pd
import numpy as np
from .valuesReader import valReader


def heapPermute(L: np.ndarray, length: int) -> np.ndarray:
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


def dataframePerm(dataframe: pd.core.frame.DataFrame, numSat):
    rows = [n for n in range(numSat)]
    for el in heapPermute(np.array(rows), numSat):
        index = indexTranslator(el)
        yield dataframe.reindex(columns=index)


def leafPerm(values: pd.core.frame.DataFrame, i=0):
    if values.shape[0] == 1:
        return dataframePerm(values.iloc[i:i+1, :], values.shape[1] // 2)
    else:
        return rowPermGen(values.iloc[i:i+1, :],
                          leafPerm(values.iloc[i+1:, :], i+1))


def rowPermGen(currentRow: pd.core.frame.DataFrame, gen):
    gen, baseGen = tee(gen)
    currentRowGen = dataframePerm(currentRow, currentRow.shape[1] // 2)
    for perm in currentRowGen:
        for insidePerm in baseGen:
            yield stackDataframes(perm, insidePerm)
        gen, baseGen = tee(gen)


def indexTranslator(index: list) -> list:
    colindex = []
    for i in index:
        colindex.append(valReader.translateSat(i)[0])
        colindex.append(valReader.translateSat(i)[1])
    return colindex


def stackDataframes(*dataframes):
    columns = dataframes[0].columns
    for df in dataframes:
        df.columns = columns
    return pd.concat(dataframes)
