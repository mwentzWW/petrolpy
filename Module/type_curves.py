import petrolpy
import matplotlib
import matplotlib.pyplot as plt

type_curve = petrolpy.hyperbolic_type_curve(b_factor=.832, initial_prod=590, di_factor=0.009, time=365)

axes = plt.subplot()

axes.plot(type_curve)
axes.grid(True)
axes.set_xlabel('Time (Days)')
axes.set_ylabel('Oil Rate (BOPD)')
axes.set_title('Oil Type Curve')
plt.yscale('log')
plt.ylim(ymin=10, ymax=10000)

plt.show()