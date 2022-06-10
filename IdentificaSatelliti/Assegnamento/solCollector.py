import math


class SolCollector():
    def __init__(self):
        self.range = 10
        self.sol = {}

    def insert(self, sol: tuple) -> None:
        if SolCollector.rangeOf(sol[0]) < self.range:
            self.sol = sol
            self.range = SolCollector.rangeOf(sol[0])
        elif SolCollector.rangeOf(sol[0]) == self.range:
            if self.range == 9:
                if sol[0] < self.sol[0]:
                    self.sol = sol
            elif math.pi * 2 / sol[1][1] > math.pi * 2 / self.sol[1][1]:
                self.sol = sol

    def getSol(self):
        return self.sol

    def rangeOf(error: float):
        if error < 1e-5:
            return 1
        if error < 1e-2:
            return 2
        if error < 1e-1:
            return 3
        if error < 1:
            return 4
        if error < 3:
            return 5
        if error < 5:
            return 6
        if error < 7:
            return 7
        if error < 10:
            return 8
        else:
            return 9
