class initCalculator():

    def __init__(self, lowerBound=0, upperBound=5000):
        step = upperBound / 4
        self.bounds = []
        for val in range(0, 5000, step):
            self.bounds.append((val, val+step))

    def getInitValues(self) -> list:
        initValues = []
        for ranges in self.bounds:
            initValues.append((ranges[1] - ranges[0]) / 2)
        return initValues

    def editRange(self, values: list):
        minSol = (0, 0)

        for sol in values:
            if sol[1] > minSol[1]:
                minSol = sol[1]
