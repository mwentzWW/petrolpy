from petrolpy import calc_oil_drainage_area

area = calc_oil_drainage_area(oil_produced=72.5, res_height=20, porosity=0.25, avg_water_saturation=0.25, oil_vol_factor=1.2, recoveryfactor=0.10)
print(area)