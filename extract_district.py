import geopandas as gpd

districts = gpd.read_file("gadm41_IND_2.shp")
tn_districts = districts[districts["NAME_1"] == "Tamil Nadu"]

tn_districts.to_file("TN_districts.shp")
