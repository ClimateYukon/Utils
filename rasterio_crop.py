def crop(tif_file,out) :
    with rasterio.open(tif_file) as src:
        Nodata = src.meta['nodata']
        out_image, out_transform = rasterio.tools.mask.mask( src, features , nodata = Nodata , crop=True )
        out_meta = src.meta.copy()

    out_meta.update({"driver": "GTiff",
                     "height": out_image.shape[1],
                     "width": out_image.shape[2],
                     "transform": out_transform,
                      "crs" : 'EPSG:3857',
                     "compress" : 'lzw'})

    with rasterio.open(out, "w", **out_meta) as dest:
        dest.write(out_image)

if __name__ == '__main__':
    import os , glob
    import fiona
    import rasterio
    import rasterio.tools.mask

    shp = '/Data/Base_Data/GIS/GIS_Data/Vector/Boundaries/Alaska_Albers_ESRI.shp'

    base = '/atlas_scratch/jschroder/NED_1_AK/result/NED1_DEM.img'

    out = base.replace('DEM','cropping_DEM')
    with fiona.open(shp, "r") as shapefile:
        features = [feature["geometry"] for feature in shapefile]

    crop(base,out)
