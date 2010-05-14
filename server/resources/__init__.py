from io import BytesIO
from os import path
from string import Template
from sys import argv
from zipfile import ZipFile

import kml

__data = dict()
with open( argv[ 0 ], 'rb' ) as f:
	zf = ZipFile( f, 'r' )
	for zi in zf.infolist():
		if zi.file_size and zi.filename.startswith( 'resources/' ) and '/' in zi.filename:
			__data[ zi.filename[ len( 'resources/' ) : ] ] = zf.read( zi )
	zf.close()
if path.exists( 'data.zip' ): 
	with open( 'data.zip', 'rb' ) as f:
		zf = ZipFile( f, 'r' )
		for zi in zf.infolist():
			if zi.file_size:
				__data[ zi.filename[ len( 'resources/' ) : ] ] = zf.read( zi )
		zf.close()

def load_template( name ):
	return Template( __data[ 'templates/{0}.html'.format( name ) ] )
	
def load_image( n ):
	return __data[ 'img/{0:03d}.jpg'.format( n ) ]
	
def save_image( n, image ):
	__data[ 'img/{0:03d}.jpg'.format( n ) ] = image
	
def load_metadata():
	try:
		return __data[ 'img/metadata.kml' ]
	except KeyError:
		return None
	
def save_metadata():
	__data[ 'img/metadata.kml' ] = kml.to_string()
	
def load_code( name ):
	pass
	
def save_code( name, code ):
	pass

def dump():
	save_metadata()
	with open( 'data.zip', 'wb' ) as f:
		zf = ZipFile( f, 'w' )
		for arcname, bytes in __data.iteritems():
			prefix_is = arcname.startswith
			if prefix_is( 'code/' ) or prefix_is( 'img/'): zf.writestr( arcname, bytes )
		zf.close()
