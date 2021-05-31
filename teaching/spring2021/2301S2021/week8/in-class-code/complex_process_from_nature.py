from random import random
from collections import defaultdict

def getOutcome():

    if random() < .3:
        part = "PartA"
    else:
        part = "PartB"

    if part == "PartA":
        if random() < .3:
            breakDown = "_Breaks"
        else:
            breakDown = "_NotBreaks"
    if part == "PartB":
        if random() < .9:
            breakDown = "_Breaks"
        else:
            breakDown = "_NotBreaks"

    return part + breakDown

if __name__ == "__main__":

    N = 1000

    total = []
    for i in range(1000):
        total.append(getOutcome())

    partCounter = defaultdict(int)
    breaksCounter = defaultdict(int)
    totalCounter = defaultdict(int)
    for t in total:
        part, breaks = t.split('_')
        partCounter[part] += 1
        breaksCounter[breaks] += 1
        totalCounter[t] += 1

    pA = partCounter["PartA"]/N
    pB = breaksCounter["Breaks"]/N
    print(partCounter["PartA"]/N)
    print(breaksCounter["Breaks"]/N)
    print(pA * pB)
    print(totalCounter["PartA_Breaks"]/N)
    print(totalCounter)