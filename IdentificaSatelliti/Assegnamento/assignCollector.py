

class AssignCollector():

    def __init__(self):
        self.assignments = []

    def add(self, assign: tuple) -> None:
        self.assignments.append(assign)

    def getBestAssign(self) -> tuple:
        AssignCollector.mergeSort(self.assignments)
        return self.assignments[0]

    def iterate(self):
        for el in self.assignments:
            yield el[0]

    def isEmpty(self):
        return len(self.assignments) == 0

    def mergeSort(arr):
        if len(arr) > 1:

            mid = len(arr)//2

            L = arr[:mid]

            R = arr[mid:]

            AssignCollector.mergeSort(L)

            AssignCollector.mergeSort(R)

            i = j = k = 0

            while i < len(L) and j < len(R):
                if L[i][1] > R[j][1]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1
