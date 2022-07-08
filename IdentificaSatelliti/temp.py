import math

e = [math.sin(0.0125*i) for i in range(10)]
w = [0.08, .500, 1., 50.0, 1500, 10000, 50000]
for puls in w:
    ef = [math.sin(puls*i) for i in range(10)]
    for el in ef:
        print(f"{el}")
    subtracted = []
    for item1, item2 in zip(e, ef):
        item = item1 - item2
        subtracted.append(item)

    mean_error = 0
    for err in subtracted:
        mean_error += err**2
    print(f"errore pari a: {mean_error/10}\n")
