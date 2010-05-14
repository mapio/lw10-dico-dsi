# Copyright (C) 2010 Massimo Santini
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from cgi import FieldStorage, escape
from mimetypes import guess_type
from os import path, access, R_OK
from shutil import copyfileobj
from string import Template
from sys import exit
from wsgiref.util import request_uri

import kml
import resources

class Handler( object ):

	def __init__( self, context ):
		self.context = context

class ImgHandler( Handler ):

	def __call__( self ):
		_context = self.context
		req = _context.request_uri_parts[ 0 ]
		return _context.response( 200, resources.load_image( int( req ) ), guess_type( '0.jpg' )[ 0 ] )
		#return self.context.static( path.join( 'img', 'metadata.kml' if img == 'metadata' else '{0:03d}.jpg'.format( int( img ) ) ) )

class MapHandler( Handler ):

	def __call__( self ):
		rup = self.context.request_uri_parts
		try:
			app = rup.pop( 0 )
		except IndexError:
			return self.context.response( 400, 'No application specified in "map" (uri {0})'.format( request_uri( self.context.environ ) ) )
		if not rup and not request_uri( self.context.environ ).endswith( '/' ):
			return self.context.response( 400, 'Missing trailing / for "{0}" (uri {1})'.format( app, request_uri( self.context.environ ) ) )
		res = rup if rup else [ app + '.html' ]
		return self.context.static( path.join( 'map', app, *res ) )

class TagHandler( Handler ):

	def __init__( self, context ):
		super( TagHandler, self ).__init__( context )
		self.templates = dict( ( _, resources.load_template( _ ) ) for _ in 'base upload metadata confirm dump'.split() )

	def __call__( self ):
		def _response( title, body_template, **kwargs ):
			html = self.templates[ 'base' ].substitute( title = title, body = self.templates[ body_template ].substitute( **kwargs ) )
			return self.context.response( 200, html, 'text/html' )
		if not self.context.request_uri_parts: stage = 'upload'
		else: stage = self.context.request_uri_parts.pop( 0 )
		if stage == 'upload':
			return _response( 'Upload', 'upload' )
		elif stage  == 'add':
			if not self.context.post_data[ 'file_field' ].filename: return _response( 'Upload', 'upload' )
			data = self.context.post_data[ 'file_field' ].file.read()
			num = len( kml.placemarks )
			resources.save_image( num, data )
			point = kml.extract_lat_lon( data )
			kml.append( kml.placemark( point ) )
			return _response( 'Aggiungi metadati', 'metadata', num = num, lat = point.lat, lon = point.lon )
		elif stage == 'metadata':
			data = self.context.post_data
			placemark = kml.placemarks[ int( self.context.request_uri_parts[ 0 ] ) ]
			placemark.appendChild( kml.name( data[ 'name' ].value ) )
			placemark.appendChild( kml.creator( data[ 'creator' ].value ) )
			placemark.appendChild( kml.description( data[ 'description' ].value ) )
			return _response( 'Conferma', 'confirm', placemark = escape( placemark.toprettyxml() ) )
		elif stage == 'dump':
			resources.save_metadata()
			return _response( 'Salvataggio', 'dump' )
		elif stage == 'halt':
			self.context.stop = True
			return self.context.response( 200, 'Server halted.' )
		else:
			return self.context.response( 400, 'Tag application error (this should never happen).' )

class EditHandler( Handler ):
	def __call__( self ):
		try:
			file = self.context.request_uri_parts.pop( 0 )
		except IndexError:
			return self.response( 400, 'No application to edit (uri {0})'.format( request_uri( self.context.environ ) ) )
		if not self.context.request_uri_parts:
			return self.context.static( path.join( 'static', 'edit.html' ) )
		action = self.context.request_uri_parts.pop( 0 )
		if action == 'load':
			fp = open( path.join( 'map', file, file + '.js' ), 'r' )
			code = fp.read()
			fp.close()
			return self.context.response( 200, code )
		elif action == 'save':
			fp = open( path.join( 'map', file, file + '.js' ), 'w' )
			fp.write( self.context.post_data[ 'code' ].value )
			return self.context.response( 200 )

class Context( object ):

	def __init__( self ):
		self.stop = False
		self.handlers = {
			'img': ImgHandler( self ),
			'tag': TagHandler( self ),
			'map': MapHandler( self ),
			'edit': EditHandler( self ),
		}

	def __call__( self, environ, start_response ):
		self.environ = environ
		self.start_response = start_response
		self.request_method = self.environ[ 'REQUEST_METHOD' ]
		self.request_uri_parts = request_uri( environ ).rstrip( '/' ).split( '/' )[ 3 : ]
		self.__post_data = None
		try:
			application = self.request_uri_parts.pop( 0 )
		except IndexError:
			return self.response( 400, 'No application specified (uri {0})'.format( request_uri( environ ) ) )
		if application == 'static':
			return self.static( path.join( 'static', *self.request_uri_parts ) )
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
			301: 'MOVED PERMANENTLY',
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
		if not self.__post_data:
			self.__post_data = FieldStorage( fp = self.environ[ 'wsgi.input' ], environ = self.environ, keep_blank_values = 1 )
		return self.__post_data
