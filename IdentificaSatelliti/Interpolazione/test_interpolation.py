import math
import json
from .interpolator import Interpolator
from .cobylaCreator import CobylaCreator


def testInterpolation(test: Interpolator):
    data = {"y": [], "t": [], "numeroPunti": 5}
    dataFile = {}
    config = {}
    for i in range(5):
        data["t"].append(i)
        data["y"].append(math.sin(i))
    with open("dataFile.json", "w") as dataFile:
        json.dump(data, dataFile, indent=4)

    with open("dataFile.json", "r") as dataModel:
        dataFile = json.load(dataModel)

    with open("config.json", "r") as configModel:
        config = json.load(configModel)

    cobyla = test.createModel(dataFile, config)
    print(cobyla.optimize())


if __name__ == '__main__':
    testInterpolation(CobylaCreator())
