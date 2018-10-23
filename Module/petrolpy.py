"""
Author: Michael Wentz
Github: github.com/mwentzWW

Scope: Create Petroleum Engineering functions commonly used for python

"""
def porosity_sim(vol_pore=0, vol_bulk=1.0, vol_matrix=0.7):
    """Returns the simple porosity of volume given the bulk and matrix volume,
     or the user can give the pore volume and bulk volume."""
    if vol_pore > 0:
        return float(vol_pore/vol_bulk)
    else:
        return float((vol_bulk-vol_matrix)/vol_bulk)

def fluid_saturation(vol_fluid=50, vol_pore=100):
    """Returns the fluid saturation given the fluid volume and pore volume."""
    return float(vol_fluid/vol_pore)

def porosity_by_densitylog(den_matrix=2.654, den_fluid=1.1, den_bulk=2.0):
    """Returns the porosity given the matrix density, fluid density, and bulk density 
    from a density log. Default values are in g/cc. Quartz density ~ 2.654, 
    Calcite density ~ 2.710, Dolomite density ~ 2.870, fresh water density ~ 1.0, 
    salt water density ~ 1.146 depending on location, oil density < 1.0 ~ 0.850"""
    return (den_matrix-den_bulk)/(den_matrix-den_fluid)

def porosity_by_soniclog(delt_log=144, delt_matrix=55.5, delt_fluid=189):
    """Returns the porosity given the average delta t (micro-sec/ft) of an interval, 
    fluid delta t, and the matrix delta t. The fluid is usually mud filtrate (189 micro-sec/ft). 
    Sandstone delta t ~ 55.5 or 51.0, Limestone delta t ~ 47.5, Dolomite delta t ~ 43.5."""
    return (delt_log-delt_matrix)/(delt_fluid-delt_matrix)

def stoiip(area=40, res_height=20, porosity=0.25, avg_water_saturation=0.4, oil_vol_factor=1.30):
    """Returns the estimate for stock tank oil initially in place (STB) given the area (acres), reservoir height (ft),
    porosity (fraction), average water saturation (fraction), and the oil formation volume factor (RB/STB)."""
    return (7758*area*res_height*porosity*(1-avg_water_saturation))/oil_vol_factor

def giip(area=40, res_height=20, porosity=0.25, avg_water_saturation=0.4, gas_vol_factor=0.00533):
    """Returns the estimate for gas initially in place (SCF) given the area (acres), reservoir height (ft),
    porosity (fraction), average water saturation (fraction), and the gas formation volume factor (RCF/SCF)."""
    return (43560*area*res_height*porosity*(1-avg_water_saturation))/gas_vol_factor

def mcf_to_boe(mcf=0, conversion_factor=6000):
    """Converts mcf to barrels of oil equivalent using the standard 6000 mcf/boe conversion factor."""
    return (mcf/conversion_factor)

def hyperbolic_type_curve(b_factor=0.8,initial_prod=0, di_factor=0.15, time=10):
    """Creates a type curve using Arp's equation for hyperbolic decline. Make sure the units for production and time are the same.
    The input for time is how long you want the type curve to estimate for, for example 1 year or 10 years. The function 
    returns the type curve as a list."""
    production = []
    for x in range(0, time + 1):
        q_time = (initial_prod)/((1 + b_factor*di_factor*x)**(1/b_factor))
        production.append(q_time)
    return production

def exponential_type_curve(initial_prod=0, di_factor=0.15, time=10):
    """Creates a type curve using Arp's equation for exponential decline. Make sure the units for production and time are the same.
    The input for time is how long you want the type curve to estimate for, for example 1 year or 10 years. The function 
    returns the type curve as a list."""
    import math
    production = []
    for x in range(0, time + 1):
        q_time = (initial_prod)*math.exp(-di_factor*x)
        production.append(q_time)
    return production

def calc_gas_vol_factor(z_value=1.0,temp=193, pressure=500):
    """Calculates the gas formation volume factor Bg from the gas compressibility factor z (0.25 up to 1.1), the reservoir temperature (F), 
    and the reservoir pressure (psia). The calculated Bg units are rcf/scf"""
    temp_rankin = temp + 459.67
    bg = 0.0282793*((z_value*temp_rankin)/pressure)
    return bg

def calc_gas_drainage_area(gas_produced=2.5, res_height=20, porosity=0.25, avg_water_saturation=0.25, gas_vol_factor=0.00533, recoveryfactor=0.65):
    """Returns the estimate for drainage area (Acres) given the gas produced (BCF), reservoir height (ft),
    porosity (fraction), average water saturation (fraction), the gas formation volume factor (RCF/SCF), and the recovery factor."""
    return ((gas_produced*10**(9))*gas_vol_factor*recoveryfactor)/(43560*res_height*porosity*(1-avg_water_saturation))