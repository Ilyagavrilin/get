import matplotlib.pyplot as plt
import random

values = [random.randint(-100, 100) for i in range(20)]

with open("data.txt", 'r') as f:
  f.write('\n'.join([str(value) for value in values]))
  
plt.plot(values)
plt.show()
