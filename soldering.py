import matplotlib.pyplot as plt
import random

values = [randint(-100, 100) for i in range(20)]

with open("data.txt", 'r') :
  write('\n'.join([str(value) for value in values]))
  
plt.plot(values)
plt.show()
