

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

            # Finding the mid of the array
            mid = len(arr)//2

            # Dividing the array elements
            L = arr[:mid]

            # into 2 halves
            R = arr[mid:]

            # Sorting the first half
            AssignCollector.mergeSort(L)

            # Sorting the second half
            AssignCollector.mergeSort(R)

            i = j = k = 0

            # Copy data to temp arrays L[] and R[]
            while i < len(L) and j < len(R):
                if L[i][1] > R[j][1]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            # Checking if any element was left
            while i < len(L):
                arr[k] = L[i]
                i += 1
                k += 1

            while j < len(R):
                arr[k] = R[j]
                j += 1
                k += 1


if __name__ == '__main__':
    test = AssignCollector()
    for i in range(10):
        test.add((0, i))
    print(test.getBestAssign())
