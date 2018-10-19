from petrolpy import calc_drainage_area
from petrolpy import calc_gas_vol_factor
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

gas_produced = float(input('Enter the cumulative production in BCF: '))
low_porosity = float(input('Enter the lower porosity limit: '))
high_porosity = float(input('Enter the higher porosity limit: '))
low_saturation = float(input('Enter the low water saturation limit: '))
high_saturation = float(input('Enter the high water saturation limit: '))
low_height = float(input('Enter the low reservoir height limit: '))
high_height = float(input('Enter the high reservoir height limit: '))
res_pressure = float(input('Enter the reservoir pressure estimate: '))

avg_porosity = (low_porosity + high_porosity)/2
avg_saturation = (low_saturation + high_saturation)/2
avg_height = (low_height + high_height)/2 

areas = []
porosityS = []
saturationS = []
recoveriesS = []
bgS = []

# all low, all average, all high cases
areas.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

areas.append(calc_drainage_area(gas_produced=gas_produced, res_height=low_height, porosity=low_porosity, 
avg_water_saturation=high_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

areas.append(calc_drainage_area(gas_produced=gas_produced, res_height=high_height, porosity=high_porosity, 
avg_water_saturation=high_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

# porosity sensitivity
porosityS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=low_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

porosityS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

porosityS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=high_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

for a in porosityS:
    areas.append(a)

# saturation sensitivity
saturationS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=low_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

saturationS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

saturationS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=high_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

for a in saturationS:
    areas.append(a)

# Recovery Factor sensitivity
recoveriesS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.50))

recoveriesS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.65))

recoveriesS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=0.00533, recoveryfactor=0.85))

for a in recoveriesS:
    areas.append(a)

# Gas formation volume factor sensitivity
bg_lowz = calc_gas_vol_factor(z_value=.3,temp=125, pressure=res_pressure)
bg_midz = calc_gas_vol_factor(z_value=.6,temp=125, pressure=res_pressure)
bg_highz = calc_gas_vol_factor(z_value=.8,temp=125, pressure=res_pressure)

print("The low Z factor Bg estimate is: {} rcf/scf".format(bg_lowz))
print("The mid Z factor Bg estimate is: {} rcf/scf".format(bg_midz))
print("The high Z factor Bg estimate is: {} rcf/scf".format(bg_highz))

bgS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=bg_lowz, recoveryfactor=0.85))

bgS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=bg_midz, recoveryfactor=0.85))

bgS.append(calc_drainage_area(gas_produced=gas_produced, res_height=avg_height, porosity=avg_porosity, 
avg_water_saturation=avg_saturation, gas_vol_factor=bg_highz, recoveryfactor=0.85))

for a in bgS:
    areas.append(a)

# Remove duplicates in areas list
all_cases = list(set(areas))
cases_rounded = []

for a in all_cases:
    rounded = round(a)
    cases_rounded.append(rounded)

print(cases_rounded)

average = round(sum(cases_rounded)/len(cases_rounded))

print("The minimum drainage area is: {} acres".format(min(cases_rounded)))
print("The average drainage area is: {} acres".format(average))
print("The maximum drainage area is: {} acres".format(max(cases_rounded)))

plt.hist(cases_rounded, alpha=0.5, label='All cases drainage area (Acres)')
plt.hist(bgS, alpha=0.5, label='Bg Sensitivity drainage area (Acres)')
plt.legend(loc='upper right')
plt.show()

# Halt immediate window closure
input("--------------------Hit Enter to close the program--------------------")