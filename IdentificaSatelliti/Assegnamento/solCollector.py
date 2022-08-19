import math
from enum import Enum, unique


@unique
class ErrorStandards(Enum):
    LV1 = 1e-4
    LV2 = 1e-2
    LV3 = 1e-1
    LV4 = 1
    LV5 = 3
    LV6 = 5
    LV7 = 7
    LV8 = 10
    # LV1 = 1e-9
    # LV2 = 1e-7
    # LV3 = 1e-5
    # LV4 = 1e-3
    # LV5 = 1e-1
    # LV6 = 1
    # LV7 = 3
    # LV8 = 5

    def rangeOf(error: float):
        if error < ErrorStandards.LV1.value:
            return 1
        if error < ErrorStandards.LV2.value:
            return 2
        if error < ErrorStandards.LV3.value:
            return 3
        if error < ErrorStandards.LV4.value:
            return 4
        if error < ErrorStandards.LV5.value:
            return 5
        if error < ErrorStandards.LV6.value:
            return 6
        if error < ErrorStandards.LV7.value:
            return 7
        if error < ErrorStandards.LV8.value:
            return 8
        else:
            return 9


class SolCollector():

    def __init__(self):
        self.range = 10
        self.sol = {}

    def insert(self, sol: tuple) -> None:
        if ErrorStandards.rangeOf(sol[0]) < self.range:
            self.sol = sol
            self.range = ErrorStandards.rangeOf(sol[0])
        elif ErrorStandards.rangeOf(sol[0]) == self.range:
            if self.range == 9:
                if sol[0] < self.sol[0]:
                    self.sol = sol
            elif (math.pi * 2 / sol[1][1]) > (math.pi * 2 / self.sol[1][1]):
                self.sol = sol

    def getSol(self):
        return self.sol
