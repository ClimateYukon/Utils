import rasterio, os, glob, fiona
import pandas as pd
import numpy as np
import rasterio.tools.mask

#quick and dirty way to convert LOGS to LOFS and crop to Yukon Flats for a ASAP plot request

pth_AKCAN = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/LOFS_AK-CAN/'
pth_YK ='/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/LOFS_YK-FLATS/'
shp = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/shp/Yukon_flats.shp'
lgs = "/Data/Base_Data/Climate/AK_CAN_2km_v2/derived_grids/decadal_monthlies/5ModelAvg/"
scenarios = ["rcp45","rcp60","rcp85"]

with fiona.open(shp, "r") as shapefile:
    features = [feature["geometry"] for feature in shapefile]

    for scen in scenarios : 
        if not os.path.exists(os.path.join(pth_AKCAN,scen)):
            os.makedirs(os.path.join(pth_AKCAN,scen))
        if not os.path.exists(os.path.join(pth_YK,scen)):
            os.makedirs(os.path.join(pth_YK,scen))
            
        path = os.path.join(lgs,scen,"logs")
        files = glob.glob(os.path.join(path,"*.tif"))
        
        for i in files : 
            print("working on {}".format(i))
            _rst = rasterio.open(i)
            meta = _rst.meta.copy()
            _arr = _rst.read()
            ind = np.where( _arr != -9999 )
            _arr[ ind ] = 365 - _arr[ ind ]
            filename = os.path.basename(i.replace('logs','lofs'))
            
            with rasterio.open(os.path.join(pth_AKCAN,scen,filename),'w',**meta) as dst :
                dst.write(_arr)
                
                #at this point destinatin become source
                src = dst
                 
                out_image, out_transform = rasterio.tools.mask.mask(src, features,
                                                                    crop=True)
                
                meta.update({"driver": "GTiff",
                         "height": out_image.shape[1],
                         "width": out_image.shape[2],
                         "transform": out_transform})
                         
                with rasterio.open(os.path.join(pth_YK,scen,filename), "w", **meta) as dest:
                    dest.write(out_image)
                

            
