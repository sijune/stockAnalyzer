import pandas as pd
import matplotlib.pyplot as plt

s = pd.Series([0,2,3,1,5])
s.index = pd.Index([4,3,2,1,2])
s.index.name = 'haha'
s.name = 'MY_SERIES'
print(s)
print(s.iloc[2])
print(s.describe())

plt.plot(s, 'bs--')
plt.xticks(s.index)
plt.yticks(s.values)
plt.grid(True)
plt.show()