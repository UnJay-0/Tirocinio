import math
from enum import Enum, unique


@unique
class ErrorStandards(Enum):
    LV1 = 1e-13
    LV2 = 1e-12
    LV3 = 1e-11
    LV4 = 1e-10
    LV5 = 1e-9
    LV6 = 1e-7
    LV7 = 1e-5
    LV8 = 1e-3
    LV9 = 1e-1
    LV10 = 1

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
        if error < ErrorStandards.LV9.value:
            return 9
        if error < ErrorStandards.LV10.value:
            return 10
        else:
            return 11


class SolCollector():

    def __init__(self):
        self.range = 12
        self.sol = {}

    def insert(self, sol: tuple) -> None:
        if sol[0] == 0.0:
            return
        if self.sol == {}:
            self.sol = sol
        if ErrorStandards.rangeOf(sol[0]) < self.range:
            self.sol = sol
            self.range = ErrorStandards.rangeOf(sol[0])
        elif ErrorStandards.rangeOf(sol[0]) == self.range:
            if self.range == 12:
                if sol[0] < self.sol[0]:
                    self.sol = sol
            elif (math.pi * 2 / sol[1][1]) > (math.pi * 2 / self.sol[1][1]):
                self.sol = sol

    def getSol(self):
        return self.sol

    def __str__(self):
        string = f"errore quadratico: {self.sol[0]}\n" + \
            f"pulsazione: {self.sol[1][1]}\n" + \
            f"ampiezza: {self.sol[1][0]}\n" + \
            f"fase: {self.sol[1][2]}\n" + \
            f"periodo: {math.pi*2 / self.sol[1][1]}\n"
        return string
