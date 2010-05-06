from cgi import FieldStorage
from os import path, access, R_OK
from shutil import copyfileobj
from string import Template
from webbrowser import open_new
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

from exif import process_file
from kml import Kml, Point

def extract_lat_lon( filename ):
	def rat2float( vals ):
		return [ float( _.num ) / float( _.den ) for _ in vals ]
	fp = open( filename, 'rb' )
	tags = process_file( fp )
	fp.close()
	try:
		lat_ref = tags[ 'GPS GPSLatitudeRef' ].values
		lat_rat = rat2float( tags[ 'GPS GPSLatitude' ].values )
		lon_ref = tags[ 'GPS GPSLongitudeRef' ].values
		lon_rat = rat2float( tags[ 'GPS GPSLongitude' ].values )
	except KeyError:
		return None
	return Point(
		( lat_rat[ 0 ] + lat_rat[ 1 ] / 60 + lat_rat[ 2 ] / 3600 ) * ( 1 if lat_ref == "N" else -1 ),
		( lon_rat[ 0 ] + lon_rat[ 1 ] / 60 + lon_rat[ 2 ] / 3600 ) * ( -1 if lon_ref == "W" else 1 )
	)

def get_template( name ):
	f = open( path.join( 'app', name + '.html' ), 'r' )
	return Template( f.read() )
	f.close()

class Handler( object ):

	def application( self, environ, start_response ):
		self.environ = environ
		self.start_response = start_response
		self.path = request_uri( environ ).split( '/' )[ 3 : ]
		self.templates = dict( ( _, get_template( _ ) ) for _ in 'base upload metadata confirm'.split() )
		dispatch = {
			'img': self.handle_img,
			'app': self.handle_app
		}
		try:
			return dispatch[ self.path[ 0 ] ]()
		except KeyError:
			return self.http_response( 400, data = ', '.join( self.path ) )

	def http_response( self, status = 200, content_type = 'text/plain; charset=utf-8', data = '' ):
		HTTP_CODES = {
			200: 'OK',
			400: 'BAD REQUEST',
			401: 'UNAUTHORIZED',
			403: 'FORBIDDEN',
			404: 'NOT FOUND',
			405: 'METHOD NOT ALLOWED',
			500: 'INTERNAL SERVER ERROR',
		}
		self.start_response( '{0} {1}'.format( status, HTTP_CODES[ status ] ), [ ( 'Content-type', content_type ) ] )
		if isinstance( data, str ): data = [ data ]
		return data

	def html_response( self, title, body_template, **kwargs ):
		data = self.templates[ 'base' ].substitute( title = title, body = self.templates[ body_template ].substitute( **kwargs ) )
		return self.http_response( 200, 'text/html', data )

	def handle_img( self ):
		num = int( self.path[ 1 ] )
		filename = path.join( 'img', '{0:03d}.jpg'.format( num ) )
		if not path.exists( filename ) or not path.isfile( filename ):
			return http_response( start_response, 404, data = "File does not exist: " + filename )
		if not access( filename, R_OK ):
			return http_response( start_response, 401, data = "You do not have permission to access this file: " + filename )
		return self.http_response( 200, 'image/jpeg', open( filename, 'rb' ) )

	def handle_app( self ):
		if self.environ[ 'REQUEST_METHOD' ] == 'POST':
			fs = FieldStorage( fp = self.environ[ 'wsgi.input' ], environ = self.environ, keep_blank_values = 1 )
			stage = fs[ 'stage' ].value
			if stage  == 'upload':
				data = Kml( 'data.xml' )
				form_file = fs[ 'file_field' ]
				dest_filename = path.join( 'img', '{0:03d}.jpg'.format( len( data ) ) )
				dest = open( dest_filename, 'wb' )
				copyfileobj( form_file.file, dest )
				dest.close()
				point = extract_lat_lon( dest_filename )
				data.append( data.placemark( point ) )
				data.write()
				if not point: point = Point( 0, 0 )
				return self.html_response( 'Aggiungi metadati', 'metadata', num = len( data ) - 1, lat = point.lat, lon = point.lon )
			elif stage == 'metadata':
				return self.html_response( 'Conferma', 'confirm' )
		else:
			return self.html_response( 'Upload', 'upload' )
		return self.http_response( 400 )

if __name__ == '__main__':
	handler = Handler()	
	server = make_server( 'localhost', 8000, handler.application )	
	open_new( 'http://localhost:8000/app' )
	server.serve_forever()
