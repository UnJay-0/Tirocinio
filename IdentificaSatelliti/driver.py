import time
import math
import random
import pandas as pd
from .Assegnamento.valuesReader import valReader
from .Assegnamento.associator import obtainOptimal, writeMeanTimes
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
    percents = []
    for ls in err:
        max = 0
        for val in ls:
            if val > max:
                max = val
        percents.append((max/N_OBSERVATIONS) * 100)
    print(f"\nmedia percentuali: {sum(percents)/len(percents)}")
    return err


if __name__ == '__main__':
    sinousoids = {}
    x = random.choices(range(1, 5000), k=4)
    sinousoids[0] = N_OBSERVATIONS
    sinousoids[1] = generateValues(random.randint(1, 10),
                                   math.pi*2/x[0], 0, sinousoids[0])
    sinousoids[2] = generateValues(random.randint(1, 10),
                                   math.pi*2/x[1], math.pi, sinousoids[0])
    sinousoids[3] = generateValues(random.randint(1, 10),
                                   math.pi*2/x[2], math.pi/2, sinousoids[0])
    sinousoids[4] = generateValues(random.randint(1, 10),
                                   math.pi*2/x[3], 3*math.pi/2, sinousoids[0])
    # sinousoids[1] = generateValues(1, 0.314, 0, sinousoids[0])
    # sinousoids[2] = generateValues(10, 0.0027, math.pi, sinousoids[0])
    # sinousoids[3] = generateValues(4, 0.00139, math.pi/2, sinousoids[0])
    # sinousoids[4] = generateValues(7, 0.125, 3*math.pi/2, sinousoids[0])
    writeDataValues(sinousoids)

    start = time.time()

    reader = valReader("IdentificaSatelliti/values.csv")
    dataframe = reader.getRangeValues(0, reader.getNumValues())
    result = obtainOptimal(dataframe)

    end = time.time()

    writeMeanTimes()

    print(result)
    for i in range(1, len(sinousoids)):
        print(pd.DataFrame(sinousoids[i]))

    print(compare(result, sinousoids))
    # for i in range(0, result.shape[1], 2):
    #     res = optimizeCol(result.iloc[:, i:i+2], maxtime=1)
    #     print(f"errore quadratico: {res[0]}")
    #     print(f"ampiezza: {res[1][0]}")
    #     print(f"pulsazione: {res[1][1]}")
    #     print(f"fase: {res[1][2]}")
    #     print(f"periodo: {math.pi*2 / res[1][1]}\n")

    # Subtract Start Time from The End Time
    total_time = end - start
    print(f"computational time: {str(total_time)}")
