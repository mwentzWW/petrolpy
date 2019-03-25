from petrolpy import calc_oil_drainage_area
from petrolpy import drainage_radius
import matplotlib.pyplot as plt
import numpy as np

print("""\

  _____     _             _             
 |  __ \   | |           | |            
 | |__) |__| |_ _ __ ___ | |_ __  _   _ 
 |  ___/ _ \ __| '__/ _ \| | '_ \| | | |
 | |  |  __/ |_| | | (_) | | |_) | |_| |
 |_|   \___|\__|_|  \___/|_| .__/ \__, |
                           | |     __/ |
                           |_|    |___/ 


""")

oil_produced = float(input('Enter the cumulative production in MBO: '))
low_porosity = float(input('Enter the lower porosity limit: '))
high_porosity = float(input('Enter the higher porosity limit: '))
low_saturation = float(input('Enter the low water saturation limit: '))
high_saturation = float(input('Enter the high water saturation limit: '))
low_height = float(input('Enter the low reservoir height limit: '))
high_height = float(input('Enter the high reservoir height limit: '))
res_depth = float(input('Enter the reservoir depth estimate: '))

res_pressure = 0.433 * res_depth
avg_porosity = (low_porosity + high_porosity) / 2
avg_saturation = (low_saturation + high_saturation) / 2
avg_height = (low_height + high_height) / 2

areas = []
porosityS = []
saturationS = []
recoveriesS = []
boS = []

# all low, all average, all high cases
areas.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                    avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

areas.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=low_height, porosity=low_porosity,
                                    avg_water_saturation=high_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

areas.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=high_height, porosity=high_porosity,
                                    avg_water_saturation=low_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

# porosity sensitivity
porosityS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=low_porosity,
                                        avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

porosityS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                        avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

porosityS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=high_porosity,
                                        avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

for a in porosityS:
    areas.append(a)

# saturation sensitivity
saturationS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=low_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

saturationS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

saturationS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=high_saturation, oil_vol_factor=1.2,
                                          recoveryfactor=0.10))

for a in saturationS:
    areas.append(a)

# Recovery Factor sensitivity
recoveriesS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.05))

recoveriesS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

recoveriesS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                          avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.15))

for a in recoveriesS:
    areas.append(a)

# Oil formation volume factor sensitivity

boS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                  avg_water_saturation=avg_saturation, oil_vol_factor=1.1, recoveryfactor=0.10))

boS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                  avg_water_saturation=avg_saturation, oil_vol_factor=1.2, recoveryfactor=0.10))

boS.append(calc_oil_drainage_area(oil_produced=oil_produced, res_height=avg_height, porosity=avg_porosity,
                                  avg_water_saturation=avg_saturation, oil_vol_factor=1.3, recoveryfactor=0.10))

print("\n--------------------Calculation Results--------------------")

print("\nThe low Bo estimate is: {} RBBL/STB --> {} acres".format(1.1, round(boS[0])))
print("The mid Bo estimate is: {} RBBL/STB --> {} acres".format(1.2, round(boS[1])))
print("The high Bo estimate is: {} RBBL/STB --> {} acres\n".format(1.3, round(boS[2])))

for a in boS:
    areas.append(a)

# Remove duplicates in areas list
all_cases = list(set(areas))
cases_rounded = []

for a in all_cases:
    rounded = round(a)
    cases_rounded.append(rounded)

print(sorted(cases_rounded))

average = round(sum(cases_rounded) / len(cases_rounded))
medianarea = round(np.median(cases_rounded))
minarea = min(cases_rounded)
maxarea = max(cases_rounded)

print("\nThe minimum drainage area is: {} acres".format(minarea))
print("The average drainage area is: {} acres".format(average))
print("The median drainage area is: {} acres".format(medianarea))
print("The maximum drainage area is: {} acres".format(maxarea))

minradius = drainage_radius(minarea)
medianradius = drainage_radius(medianarea)
maxradius = drainage_radius(maxarea)

print("\nThe minimum drainage radius is: {} miles".format(minradius))
print("The median drainage radius is: {} miles".format(medianradius))
print("The maximum drainage radius is: {} miles\n".format(maxradius))

plt.hist(cases_rounded, alpha=0.5, label='All cases drainage area (Acres)')
plt.hist(saturationS, alpha=0.5, label='Oil Saturation Sensitivity drainage area (Acres)')
plt.legend(loc='upper right')
plt.show()

# Halt immediate window closure
input("--------------------Hit Enter to close the program--------------------")
