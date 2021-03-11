from random import random 

p = {"Sunny": .24, "Cloudy": .7, "Rainy": .06}

with open("weather.txt", "w") as of:
    for i in range(1000):
        prob = random()
        if prob < p["Sunny"]:
            of.write("Sunny\n")
        elif prob > 1 -  p["Rainy"]:
            of.write("Rainy\n")
        else:
            of.write("Cloudy\n")