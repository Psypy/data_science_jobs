import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

jobs = pd.read_csv("/home/max/PycharmProjects/GlassDoor/venv/jobs.csv")

print(jobs.loc[0,'Job Description'])
