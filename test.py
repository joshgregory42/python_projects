import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


bin_ranges = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

data = pd.read_csv('grades.csv')

grades = data.loc[2:, 'Final_Score']

plt.hist(grades, bins=bin_ranges, edgecolor='black')
plt.xlabel("Grade")
plt.ylabel("Count")
plt.show()
