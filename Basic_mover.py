import os
import glob

source = '/home/UA/jschroder/Pictures/resize2/'

#We want all the files which looks like that '/home/UA/jschroder/Pictures/resize2/*.tif so :
l = glob.glob( os.path.join(source , '*.tif') )

#Loop through l, list of files
for i in l :
	#grab the basename (Aliy_Zirkle-HD-2497.jpg), split by '-' and takes the first one : [0]
	name  = os.path.splitext( os.path.basename( i ) )[0].split( '-' )[0]

	#create the new path by joining that /home/UA/jschroder/Pictures/resize2/ and Aliy_Zirkle
	path = os.path.join(source,name)

	#if it doens'nt exist, create it
	if not os.path.exists( path ):
		os.mkdir( path )

	#and move the file, rename here is used for moving as you rename it from /home/UA/jschroder/Pictures/resize2/Aliy_Zirkle-HD-2497.jpg to
	#/home/UA/jschroder/Pictures/resize2/Aliy_Zirkle/Aliy_Zirkle-HD-2497.jpg	
	os.rename(i , os.path.join(source,name,os.path.basename( i )))
