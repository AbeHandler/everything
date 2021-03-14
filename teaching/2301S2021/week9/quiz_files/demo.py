import pandas as pd
import numpy as np
from random import random

heads = 0
total_flips = 0
pct_heads = []

for i in range(50):
    if random() < .5:
        heads += 1
    total_flips += 1
    pct_heads.append(heads/total_flips)

ts = pd.Series(pct_heads)

ts.plot(ylim=[0,1])