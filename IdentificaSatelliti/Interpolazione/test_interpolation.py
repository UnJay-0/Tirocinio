import json
import nlopt
import math
from .interpolator import Interpolator
from .slsqpCreator import SlsqpCreator
from .genericDfCreator import GenericDfCreator
from .genericGbCreator import GenericGbCreator
from .cobylaCreator import CobylaCreator


def testInterpolation(test: Interpolator, data, config):
    intModel = test.createModel(data, config)
    result = intModel.optimize()
    printResult(result)


def printResult(result: tuple) -> None:
    print(f"valore f.o.: {result[0]:.6f}")
    print(f"ampiezza: {result[1][0]: .6f}\nw: {result[1][1]: .6f}")
    print(f"fase: {result[1][2]:.6f}")
    err = result[2] / data["numeroPunti"]
    print(f"errore quadratico medio: {err}")


def writeValues(a, w, f) -> None:
    dataValues = {"numeroPunti": 6}
    t = [0, 1, 2, 3, 4, 5]
    y = []
    for i in t:
        y.append(a * math.sin(w * i + f))
    with open("dataFile.json", "w") as data:
        dataValues["t"] = t
        dataValues["y"] = y
        dataValues["b"] = 0.01
        json.dump(dataValues, data, indent=4)


if __name__ == '__main__':
    # writeValues(5, -6, math.pi)
    writeValues(1, 1, 0)

    ln = [nlopt.LN_BOBYQA, nlopt.LN_PRAXIS, nlopt.LN_SBPLX,
          nlopt.LN_NEWUOA, nlopt.LN_NELDERMEAD]
    ld = [nlopt.LD_MMA, nlopt.LD_VAR1, nlopt.LD_VAR2,
          nlopt.LD_CCSAQ, nlopt.LD_LBFGS, nlopt.LD_TNEWTON]

    with open("dataFile.json", "r") as dataModel:
        data = json.load(dataModel)
    with open("config.json", "r") as configModel:
        config = json.load(configModel)

    if (config["algorithm"] == nlopt.LN_COBYLA):
        testInterpolation(CobylaCreator(), data, config)
    elif (config["algorithm"] in ln):
        testInterpolation(GenericDfCreator(), data, config)
    elif (config["algorithm"] == nlopt.LD_SLSQP):
        testInterpolation(SlsqpCreator(), data, config)
    elif (config["algorithm"] in ld):
        testInterpolation(GenericGbCreator(), data, config)
