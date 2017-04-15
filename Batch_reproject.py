import os
import glob

#folder containing rasters to reproject
source = '/workspace/Shared/Users/afloyd8/NWT/CRU_rasters'
l = glob.glob(os.path.join(source, '*.tif'))

for i in l :
	#store reprojected file in the folder name warped
	dst = os.path.join(source,'warped')

	if not os.path.exists( dst ):
		os.mkdir( dst )

	file = os.path.join(dst,os.path.basename(i))

	#change projection s = source t = target
	os.system('gdalwarp -s_srs EPSG:4326 -t_srs EPSG:3580 -wo NUM_THREADS=ALL_CPUS -of GTiff %s %s' % ( i , file  ))
