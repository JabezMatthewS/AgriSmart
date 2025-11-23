import rasterio
import pandas as pd
import numpy as np

# Soil properties and their .vrt links (0-5cm depth)
soil_layers = {
    "pH": ("https://files.isric.org/soilgrids/latest/data/phh2o/phh2o_0-5cm_mean.vrt", 0.1),
    "sand": ("https://files.isric.org/soilgrids/latest/data/sand/sand_0-5cm_mean.vrt", 1),
    "clay": ("https://files.isric.org/soilgrids/latest/data/clay/clay_0-5cm_mean.vrt", 1),
    "soc": ("https://files.isric.org/soilgrids/latest/data/soc/soc_0-5cm_mean.vrt", 0.01)  # g/kg → %
}

coords = [
    (76.9558, 11.0168),  # Farm 1
    (78.7047, 10.7905),  # Farm 2
    (78.1198,  9.9252)   # Farm 3
]

df = pd.DataFrame(coords, columns=["lon", "lat"])

for name, (url, scale) in soil_layers.items():
    with rasterio.open(url) as src:
        values = [val[0] for val in src.sample(coords)]
        values = np.where(np.array(values) == -32768, np.nan, values)  # replace nodata
        df[name] = values * scale  # apply scaling

print(df)
