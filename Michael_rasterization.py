class SubDomains( object ):
	'''
	a class that reads in and prepares a dataset to be used in masking
	'''
	def __init__( self, fiona_shape, rasterio_raster, id_field, **kwargs ):
		'''
		initializer for the SubDomains object
		The real magic here is that it will use a generator to loop through the 
		unique ID's in the sub_domains raster map generated.
		'''
		import numpy as np
		self.sub_domains = self.rasterize_subdomains( fiona_shape, rasterio_raster, id_field, **kwargs )
		self.domains_generator = self._domains_generator() # this may be confusing remove if needed.
		self.sub_domains_path = self._domains_name( fiona_shape, rasterio_raster )
		self.template_raster_path = rasterio_raster.name
	@staticmethod
	def rasterize_subdomains( fiona_shape, rasterio_raster, id_field ):
		'''
		rasterize a subdomains shapefile to the extent and resolution of 
		a template raster file. The two must be in the same reference system 
		or there will be potential issues. 
		returns:
			numpy.ndarray with the shape of the input raster and the shapefile
			polygons burned in with the values of the id_field of the shapefile
		gotchas:
			currently the only supported data type is uint8 and all float values will be
			coerced to integer for this purpose.  Another issue is that if there is a value
			greater than 255, there could be some error-type issues.  This is something that 
			the user needs to know for the time-being and will be fixed in subsequent versions
			of rasterio.  Then I can add the needed changes here.
		'''
		from rasterio.features import rasterize
		import six
		import numpy as np

		test_shape_field = [ f['properties'][id_field] for f in fiona_shape ][0]
		if fiona_shape:
			if not isinstance( test_shape_field , six.string_types ):
				out = rasterize( ( ( f['geometry'], int(f['properties'][id_field]) ) for f in fiona_shape ),
						out_shape=rasterio_raster.shape,
						transform=rasterio_raster.transform,
						fill=0 )
			elif isinstance( test_shape_field, six.string_types ):
				BaseException ( 'Check the type of the id_field, it can only work with uint8 or vals between 0-255' )
			else:
				BaseException ( 'Check the inputs' )
		elif fiona_shape is None:
			out = rasterio_raster.read_band( 1 )
		else:
			BaseException( 'Check the inputs' )
		return out
	def _domains_name( self, fiona_shape, rasterio_raster, **kwargs ):
		'''
		return a domains shapefile name or None
		'''
		if fiona_shape:
			out_name = fiona_shape.name
		elif fiona_shape is None:
			out_name = rasterio_raster.name
		return out_name
	def _domains_generator( self, **kwargs ):
		'''
		this is a simple generator creator to save on RAM and also so it can be easily regenerated
		for subsequent time steps as it plows through the data.
		NOTE:
			due to pickling issues with both pickle and dill, I had to convert this to a list comprehension
			instead of a generator because generators cannot be pickled using either approach.
		'''
		return [( str( i ), np.ma.masked_where( self.sub_domains != i, self.sub_domains )) for i in np.unique( self.sub_domains ) if i != 0 ]



# to use the above class for your purposes:
shp_fn = '' # path to the shapefile
id_field = '' # name of field to use for rasterizing the shapefile
rst_fn = '' # path to the raster to use as as template for rasterization
shp = fiona.open( shp_fn )
rst = rasterio.open( rst_fn )
sub_domains = SubDomains( shp, rst, id_field )

new_rasterized_arr = sub_domains.sub_domains

# do whatever you want here 
