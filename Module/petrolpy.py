"""
Author: Michael Wentz
Github: github.com/mwentzWW

Scope: Create Petroleum Engineering functions commonly used for python

"""
def porosity_sim(vol_pore= 0, vol_bulk=1.0, vol_matrix=0.7):
    """Returns the simple porosity of volume given the bulk and matrix volume."""
    if vol_pore > 0:
        return float(vol_pore/vol_bulk)
    else:
        return float((vol_bulk-vol_matrix/vol_bulk))

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
    fluid delta t, and the matrix delta t. The fuid is usually mud filtrate (189 micro-sec/ft). 
    Sandstone delta t ~ 55.5 or 51.0, Limestone delta t ~ 47.5, Dolomite delta t ~ 43.5."""
    return (delt_log-delt_matrix)/(delt_fluid-delt_matrix)

def stoiip(area=40, res_height=20, porosity=0.25, avg_water_saturation=0.4, oil_vol_factor=1.30):
    """Returns the estimate for stock tank oil initially in place (STB) given the area (acres), reservoir height (ft),
    porosity (fraction), average water saturation (fraction), and the oil formation volume factor (RB/STB)."""
    return (7758*area*res_height*porosity*(1-avg_water_saturation))/oil_vol_factor

#def giip(area=40, res_height=20, porosity=0.25, avg_water_saturation=0.4, gas_vol_factor=1.30):
    """Returns the estimate for stock tank oil initially in place (STB) given the area (acres), reservoir height (ft),
    porosity (fraction), average water saturation (fraction), and the oil formation volume factor (RB/STB)."""
    #return (7758*area*res_height*porosity*(1-avg_water_saturation))/oil_vol_factor