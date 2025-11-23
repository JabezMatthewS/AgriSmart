import rasterio

file = "PH_TN_0cm.tif"

with rasterio.open(file) as src:
    print("Driver:", src.driver)
    print("Shape:", src.width, "x", src.height)
    print("Bands:", src.count)
    print("CRS:", src.crs)
    print("Transform:", src.transform)
    print("Nodata value:", src.nodata)
    print("Metadata:", src.tags())
