import numpy as np
import matplotlib.pyplot as plt

fig, ax = plt.subplots()
# reading from files
with open("settings.txt", "r") as s_stream:
    time_delta, discr_level = [float(i) for i in s_stream.read().split()]
s_stream.close()

d_stream = open("data.txt", "r")
res = []
for line in d_stream:
    res.append(float(line))
d_stream.close()
# calculate output
data = np.array(res)
data = data * discr_level
time = np.arange(0, len(data) * time_delta, time_delta)
# plotting lone and simplified dots
plt.plot(time, data, label="Зависимость V(t)", ds="steps")
ax.scatter(time[::40], data[::40], label="Точечное представление", color='black', marker='d')
# settings for grid
ax.minorticks_on()
ax.grid(which='major',
        color='k',
        linewidth=0.3)

ax.grid(which='minor',
        color='k',
        linestyle=':',
        linewidth=0.2)
# labels and title
ax.legend(title="Данные о графике:")
ax.set_xlabel('$t, сек.$')
ax.set_ylabel('$U, В.$')
plt.title("Зарядка и разрядка RC-цепи")
# load time
max_n = np.argmax(data)
ax.annotate("Время заряда: {0:.2} сек.".format(time_delta * max_n), xy=(time[max_n], data[max_n]))
# disload time
ax.annotate("Время разряда: {0:.2} сек.".format(time_delta * (len(time) - max_n)), xy=(time[max_n], data[max_n]),
            xytext=(5, 0))
# final save and showing
plt.savefig("V_t.svg", format='svg')
plt.show()
