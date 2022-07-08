import pandas as pd
from numpy import median
from .associatorRange import optimizeCol
from .valuesReader import valReader
from .permutation import dataframePerm, leafPerm
from .solCollector import ErrorStandards
from .assignCollector import AssignCollector
from .associator import leafOptimal


reader = valReader("IdentificaSatelliti/values.csv")
LEAF_SIZE = valReader.leafSize(reader.getNumValues())


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
    assignments = AssignCollector()
    assignments.add((leafOptimal(values.iloc[0: LEAF_SIZE, :]), 0))
    for oss in range(LEAF_SIZE, reader.getNumValues()):
        ossCorrente = values.iloc[[oss]]
        print(f"riga:\n{ossCorrente}")
        if assignments.isEmpty():
            assignments.add((ossCorrente, 0))
        else:
            assignmentsTemp = AssignCollector()
            for el in assignments.iterate():
                print(f"assegnamento:\n {el}\n")
                for perm in leafPerm(ossCorrente):
                    perm.columns = el.columns
                    assign = pd.concat([el, perm])
                    print(f"concatenazione:\n {assign}")
                    colValues = []
                    for i in range(0, assign.shape[1], 2):
                        colValue = optimizeCol(assign.iloc[:, i:i+2])
                        colValues.append(ErrorStandards.rangeOf(colValue))
                    assignmentsTemp.add((assign, median(colValues)))
                    print(f"valore: {median(colValues)}")
            assignments = assignmentsTemp
    return assignments.getBestAssign()


def generateStartAssign(values: pd.core.frame.DataFrame) -> AssignCollector:
    assignments = AssignCollector()
    leaf = values.iloc[0: LEAF_SIZE, :]
    print(f"foglia: \n{leaf}\n")
    for el in leafPerm(leaf):
        print(f"permutazione: \n{el}")
        colValues = []
        for i in range(0, leaf.shape[1], 2):
            print(f"colonna: \n{el.iloc[:, i:i+2]}")
            colValue = optimizeCol(el.iloc[:, i:i+2])
            print(f"valore colonna : {colValue}\n")
            colValues.append(ErrorStandards.rangeOf(colValue))
        assignments.add((el, median(colValues)))
        print(f"valore: {median(colValues)}\n")
    return assignments
