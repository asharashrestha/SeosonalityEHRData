

import matplotlib.pyplot as plt
import numpy as np

a = np.random.rand(20)

b = np.r_[a, np.random.rand(20)*1.6]
c = np.random.rand(20)*2.1
data = [a,b,c]
mins = [d.mean() for d in data]
maxes = [d.mean() for d in data]

plt.figure()
plt.boxplot(data)
# simply plot the data as usual
plt.plot([1,2,3], mins, c="r", lw=2)
plt.plot([1,2,3], maxes, c="g", lw=2)


plt.show()