import time
import math
import pandas as pd
from .Assegnamento.valuesReader import valReader
from .Assegnamento.associator import obtainOptimal
from .Assegnamento.valuesWriter import generateValues, writeDataValues

N_OBSERVATIONS = 10


def compare(result, sinousoids) -> tuple:
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
    return err


if __name__ == '__main__':
    sinousoids = {}
    sinousoids[0] = N_OBSERVATIONS
    sinousoids[1] = generateValues(1, 1, 0, sinousoids[0])
    sinousoids[2] = generateValues(10, 4, math.pi, sinousoids[0])
    sinousoids[3] = generateValues(4, 0.5, math.pi/2, sinousoids[0])
    # sinousoids[4] = generateValues(7, 1, 3*math.pi/2, sinousoids[0])
    writeDataValues(sinousoids)

    start = time.time()
    # Grab Currrent Time After Running the Code
    reader = valReader("IdentificaSatelliti/values.csv")
    dataframe = reader.getRangeValues(0, reader.getNumValues())
    result = obtainOptimal(dataframe)

    end = time.time()

    print(result)
    for i in range(1, len(sinousoids)):
        print(pd.DataFrame(sinousoids[i]))

    print(compare(result, sinousoids))

    # Subtract Start Time from The End Time
    total_time = end - start
    print(f"computational time: {str(total_time)}")
