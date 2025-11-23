import rasterio
import pandas as pd
from rasterio.sample import sample_gen

# Setup: download tif for pH (0–5cm) manually from soilgrids.org

raster = rasterio.open("phh2o_0-5cm_50m.tif")  # adjust filename
farms = pd.read_csv("farms.csv")               # has 'farm_id', 'lon', 'lat'

coords = [(x, y) for x, y in zip(farms.longitude, farms.latitude)]
vals = [val[0] for val in raster.sample(coords)]

farms["phh2o_0_5cm"] = vals
farms.to_csv("farms_with_ph.csv", index=False)
print("✅ Done! Data saved to farms_with_ph.csv")