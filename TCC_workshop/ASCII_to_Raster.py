import rasterio
import pandas as pd
import glob
import os
base = '/Data/Base_Data/Climate/Other/Permafrost/AK_CAN_2km/'
scenarios = ['2013_AK_Can_2km_5model_a1b','2013_AK_Can_2km_5model_a2']
for scenario in scenarios :
    path = os.path.join(base,scenario)

    out = '/workspace/Shared/Users/jschroder/Yukon-Flats_workshop/Permafrost/Source'

    if not os.path.exists(os.path.join(out , scenario)):
        os.makedirs(os.path.join(out , scenario))

    folders = glob.glob(os.path.join(path, '*out*'))
    _ls = [glob.glob(os.path.join( f, '*.txt')) for f in folders]
    ls = [item for sublist in _ls for item in sublist]

    
    for asc in ls : 
            
        rst = rasterio.open(asc)
        arr = rst.read()
        meta = rst.meta

        meta.update( crs={'init':"epsg:3338"},driver='GTiff')
        filename = os.path.basename(asc)
        with rasterio.open(os.path.join(out , scenario , filename.replace('txt','tif')), "w", **meta) as dest:
            dest.write(arr)
