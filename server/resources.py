from io import BytesIO
from os import path
from sys import argv
from zipfile import ZipFile

class Resources( object ):
	
	def __init__( self, basename ):
		self.basename = basename
		if path.exists( basename ):
			_data = dict()
			with open( filename, 'rb' ) as f:
				zf = ZipFile( f, 'r' )
				for zi in zf.infolist():
					_data[ zi.filename ] = zf.read( zi )
		self.data = _data

	def load_template( self, name ):
		pass
		
	def load_image( self, n ):
		return self.data[ 'img/{0:03d}.jpg'.format( n ) ]
		
	def save_image( self, n, image ):
		self.data[ 'img/{0:03d}.jpg'.format( n ) ] = image
		
	def load_metadata( self ):
		return self.data[ 'img/metadata.kml' ]
		
	def save_metadata( self, metadata ):
		self.data[ 'img/metadata.kml' ] = metadata
		
	def load_code( self, name ):
		pass
		
	def save_code( self, name, code ):
		pass
	
	def dump( self ):
		with open( filename, 'wb' ) as f:
			zf = ZipFile( f, 'w' )
			for arcname, bytes in data.iteritems():
				zf.writestr( arcname, bytes )
