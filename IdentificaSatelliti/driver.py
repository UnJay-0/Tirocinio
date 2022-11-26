import time
import math
# import pandas as pd
from .Assegnamento.valuesReader import valReader
from .Assegnamento.associator import obtainOptimal
from .Assegnamento.associatorRange import amplOptCol, setRange
from .Assegnamento.valuesWriter import generateValuesError, writeDataValues

N_OBSERVATIONS = 10


def compare(result, sinousoids) -> tuple:
    """
    Overview
    -------------------
    Compara due dataframe contenenti punti relativi a sinusoidi idenficando
    il numero di punti in comune per ogni sinusoide

    Params
    -------------------
    result (pd.dataframe) -> dataframe contenente i risultati ottenuti da una
                            ottimizzazione.
    sinousoids (pd.dataframe) -> dataframe contenente i punti generati dalle
                                sinusoidi del problema.

    Returns
    -------------------
    list - contenente il numero di punti uguali per ogni sinusoide di partenza
           rispotto al risultato ottenuto.

    """
    err = []
    for i in range(len(sinousoids) - 1):
        err.append([0] * (len(sinousoids) - 1))
    for i in range(sinousoids[0]):
        for n in range(len(sinousoids)-1):
            for k in range(len(sinousoids)-1):
                index = valReader.translateSat(k)[1]
                if math.isclose(sinousoids[n+1]["y0"][i],
                                result.iloc[i][index],
                                rel_tol=1e-10, abs_tol=1e-10):
                    err[n][k] += 1
    percents = []
    for ls in err:
        max = 0
        for val in ls:
            if val > max:
                max = val
        percents.append((max/N_OBSERVATIONS) * 100)
    print(f"\nmedia percentuali: {sum(percents)/len(percents)}")
    return err


def getFloatValue(printStr: str) -> float:
    """
    Overview
    -------------------
    Funzione che chiede e gestisce la validazione di un input di tipo float

    Params
    -------------------
    printStr (str) -> stringa da stampare in output.

    Returns
    -------------------
    float -> valore ricevuto in input

    """
    while(True):
        try:
            value = float(input(printStr))
            return value
        except ValueError:
            print("Inserire valori numerici, se decimali con il punto\n")


def getIntValue(printStr: str) -> int:
    """
    Overview
    -------------------
    Funzione che chiede e gestisce la validazione di un input di tipo int

    Params
    -------------------
    printStr (str) -> stringa da stampare in output.

    Returns
    -------------------
    int -> valore ricevuto in input

    """
    while(True):
        try:
            value = int(input(printStr))
            return value
        except ValueError:
            print("Inserire valori numerici interi\n")


if __name__ == '__main__':
    print("SPECIFICAZIONE DEL PROBLEMA\n")
    print("Inserire intervallo dei periodi delle sinusoidi sovrapposte")
    range1 = getFloatValue("Limite inferiore (s): ")
    range2 = getFloatValue("Limite superiore (s): ")
    setRange(range1, range2)
    N_OBSERVATIONS = getIntValue("Numero di osservazioni: ")
    nSin = getIntValue("Numero di sinusoidi: ")
    sinParameters = []
    for i in range(1, nSin+1):
        print(f"Parametri della {i}-esima sinusoide")
        ampiezza = getFloatValue("Ampiezza: ")
        pulsazione = getFloatValue("Pulsazione (rad/s): ")
        fase = getFloatValue("Fase (rad): ")
        sinParameters.append((ampiezza, pulsazione, fase))
    errore = getFloatValue("Errore (%) sulle osservazioni: ")
    setRange(range1, range2)
    sinousoids = {}
    sinousoids[0] = N_OBSERVATIONS
    for i in range(nSin):
        sinousoids[i + 1] = generateValuesError(sinParameters[i][0],
                                                sinParameters[i][1],
                                                sinParameters[i][2],
                                                sinousoids[0], errore)

    writeDataValues(sinousoids)

    start = time.time()

    reader = valReader("IdentificaSatelliti/values.csv")
    dataframe = reader.getRangeValues(0, reader.getNumValues())
    result = obtainOptimal(dataframe)

    end = time.time()

    # writeMeanTimes()

    res = []
    for i in range(0, result.shape[1], 2):
        res.append(amplOptCol(result.iloc[:, i:i+2]))

    print("\n\n\n\n\nSINUSOIDI INDIVIDUATE: \n")
    for el in res:
        print(f"errore quadratico: {el[0]}")
        print(f"ampiezza: {el[1][0]}")
        print(f"pulsazione: {el[1][1]}")
        print(f"fase: {el[1][2]}")
        print(f"periodo: {math.pi*2 / el[1][1]}\n")

    total_time = end - start
    print(f"in tempo: {str(total_time)}")
    # print(result)
    # for i in range(1, len(sinousoids)):
    #     print(pd.DataFrame(sinousoids[i]))
    #
    # print(compare(result, sinousoids))
