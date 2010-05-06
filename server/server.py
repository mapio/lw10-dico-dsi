from cgi import FieldStorage, escape
from mimetypes import guess_type
from os import path, access, R_OK
from shutil import copyfileobj
from string import Template
from sys import exit
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

class Handler( object ):

	def __init__( self, context ):
		self.context = context

class ImgHandler( Handler ):

	def __call__( self ):
		num = int( self.context.request_uri_parts[ 0 ] )
		filename = path.join( 'img', '{0:03d}.jpg'.format( num ) )
		return self.context.static( filename )
		
class MapHandler( Handler ):

	def __call__( self ):
		rup = self.context.request_uri_parts
		app = rup.pop( 0 )
		res = rup if rup else [ app + '.html' ]
		filename = path.join( 'map', app, *res )
		print filename
		return self.context.static( filename )

class TagHandler( Handler ):

	def __init__( self, context ):
		super( TagHandler, self ).__init__( context )
		def _get( name ):
			f = open( path.join( 'tag', name + '.html' ), 'r' )
			return Template( f.read() )
			f.close()
		self.templates = dict( ( _, _get( _ ) ) for _ in 'base upload metadata confirm dump'.split() )

	def __call__( self ):
		def _html( title, body_template, **kwargs ):
			return self.templates[ 'base' ].substitute( title = title, body = self.templates[ body_template ].substitute( **kwargs ) )
		stage = self.context.request_uri_parts[ 0 ]
		kml = self.context.kml
		if stage == 'upload':
			return self.context.response( 200, _html( 'Upload', 'upload' ), 'text/html' )
		elif stage  == 'metadata':
			dest = path.join( 'img', '{0:03d}.jpg'.format( len( kml ) ) )
			self.context.post_file( 'file_field', dest )
			point = extract_lat_lon( dest )
			kml.append( kml.placemark( point ) )
			if not point: point = Point( 0, 0 )
			return self.context.response( 200, _html( 'Aggiungi metadati', 'metadata', num = len( kml ) - 1, lat = point.lat, lon = point.lon ), 'text/html' )
		elif stage == 'confirm':
			data = self.context.post_data
			placemark = kml[ int( data[ 'num' ].value ) ]
			placemark.appendChild( kml.name( data[ 'name' ].value ) )
			placemark.appendChild( kml.creator( data[ 'creator' ].value ) )
			placemark.appendChild( kml.description( data[ 'description' ].value ) )
			return self.context.response( 200, _html( 'Conferma', 'confirm', placemark = escape( placemark.toprettyxml() ) ), 'text/html' )
		elif stage == 'dump':
			kml.write()
			return self.context.response( 200, _html( 'Salvataggio', 'dump' ), 'text/html' )
		elif stage == 'halt':
			self.context.stop = True
			return self.context.response( 200, '' )
		else:
			return self.context.response( 400, 'Tag application error' )

class Context( object ):

	def __init__( self, kml ):
		self.handlers = {
			'img': ImgHandler( self ),
			'tag': TagHandler( self ),
			'map': MapHandler( self )
		}
		self.kml = kml
		self.stop = False

	def __call__( self, environ, start_response ):
		self.environ = environ
		self.start_response = start_response
		self.request_method = self.environ[ 'REQUEST_METHOD' ]
		self.request_uri_parts = request_uri( environ ).rstrip( '/' ).split( '/' )[ 3 : ]
		application = self.request_uri_parts.pop( 0 )
		try:
			handle = self.handlers[ application ]
		except KeyError:
			return self.response( 400, 'No handler defined for "{0}" (uri {1})'.format( application, request_uri( environ ) ) )
		else:
			return handle()

	def response( self, status = 200, data = '', content_type = 'text/plain; charset=utf-8' ):
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

	def post_file( self, field_name, dest_filename ):
		dest = open( dest_filename, 'wb' )
		copyfileobj( self.post_data[ field_name ].file, dest )
		dest.close()

	def static( self, filename ):
		if not path.exists( filename ) or not path.isfile( filename ):
			return self.response( 404, 'File does not exist: ' + filename )
		if not access( filename, R_OK ):
			return self.response( 401, 'You do not have permission to access this file: ' + filename )
		mime_type = guess_type( filename )[ 0 ]
		if not mime_type: mime_type = 'application/octet-stream'
		f = open( filename, 'r' if mime_type.startswith( 'text/' ) else 'rb' )
		data = f.read()
		f.close()
		return self.response( 200, data, mime_type )

	@property
	def post_data( self ):
		return FieldStorage( fp = self.environ[ 'wsgi.input' ], environ = self.environ, keep_blank_values = 1 )
