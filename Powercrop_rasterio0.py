def crop(tif_file) :
	with rasterio.open(tif_file) as src:
		Nodata = src.metap['nodata']
	    out_image, out_transform = rasterio.tools.mask.mask( src, features , nodata = Nodata , crop=True )
	    out_meta = src.meta.copy()

	out_meta.update({"driver": "GTiff",
	                 "height": out_image.shape[1],
	                 "width": out_image.shape[2],
	                 "transform": out_transform,
	                 "compress" : 'lzw'})

	year = tif_file.split('/')[-2]
	out = tif_file.replace('apbennett','jschroder').replace('/'+ year , '')

	with rasterio.open(out, "w", **out_meta) as dest:
	    dest.write(out_image)

if __name__ == '__main__':
	import os , glob
	import fiona
	import rasterio
	import rasterio.tools.mask
	from pathos import multiprocessing as mp
	shp = '/Data/Base_Data/GIS/GIS_Data/Vector/Boundaries/Alaska_Albers_ESRI.shp'

	a = ['mpi_echam5.sresa1b' , 'cccma_cgcm3_1.sresa1b' , 'mpi_echam5.sresa2','cccma_cgcm3_1.sresa2','mpi_echam5.sresb1' , 'cccma_cgcm3_1.sresb1' ]

	base = '/atlas_scratch/apbennett/IEM/FinalCalib'
	base = os.path.join(base,a[0])
	outpath = base.replace('apbennett','jschroder')
	with fiona.open(shp, "r") as shapefile:
		features = [feature["geometry"] for feature in shapefile]

	if not os.path.exists(os.path.join(outpath,'Maps')): os.makedirs(os.path.join(outpath,'Maps'))

	lsa = [i for j in range(1900,2101) for i in glob.glob( os.path.join(base , 'Maps' , str(j) , '*.tif')) ]
	lsa.sort()
	pool = mp.Pool( 32 )
	pool.map(crop,lsa)
	pool.close()
