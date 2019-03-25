#%%
import petrolpy
import pandas as pd

well = petrolpy.Well('HOGUE', 35087221020000)
print(well)
#%%
data = pd.read_csv("https://raw.githubusercontent.com/mwentzWW/petrolpy/master/Module/Test_Data/test_data_DRI%20Producing%20Entity%20Monthly%20Production.CSV")
#%%
well_data = data.groupby(['API/UWI']).get_group(well.api)
well.import_monthly_production(well_data["Monthly Oil"], well_data["Monthly Gas"])
print(well.d_oil)
print(well.d_gas)