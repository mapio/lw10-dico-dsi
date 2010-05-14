from io import BytesIO
from os import path
from string import Template
from sys import argv
from xml.dom.minidom import parseString
from zipfile import ZipFile

class Resources( object ):
	
	def __init__( self ):
		if path.exists( basename ):
			_data = dict()
			with open( basename, 'rb' ) as f:
				zf = ZipFile( f, 'r' )
				for zi in zf.infolist():
					_data[ zi.filename ] = zf.read( zi )
		self.data = _data

	def load_template( self, name ):
		return Template( self.data[ 'templates/{0}.html'.format( name ) ] )
		
	def load_image( self, n ):
		return self.data[ 'img/{0:03d}.jpg'.format( n ) ]
		
	def save_image( self, n, image ):
		self.data[ 'img/{0:03d}.jpg'.format( n ) ] = image
		
	def load_metadata( self ):
		try:
			return parseString( self.data[ 'img/metadata.kml' ] )
 		except KeyError:
			return None
		
	def save_metadata( self, xml ):
		self.data[ 'img/metadata.kml' ] = xml.toxml( 'utf-8' )
		
	def load_code( self, name ):
		pass
		
	def save_code( self, name, code ):
		pass
	
	def dump( self ):
		with open( self.basename, 'wb' ) as f:
			zf = ZipFile( f, 'w' )
			for arcname, bytes in self.data.iteritems():
				zf.writestr( arcname, bytes )
			zf.close()
