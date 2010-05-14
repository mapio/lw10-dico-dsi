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
from wsgiref.util import request_uri as wsgi_request_uri

import kml
import resources
import templates

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

stop = False
request_method = None
request_uri = None
request_uri_parts = None
post_data = None
__start_response = None

def handle_img():
	req = request_uri_parts[ 0 ]
	if req == 'metadata':
		return response( 200, kml.string(), 'application/vnd.google-earth.kml+xml' )
	else:
		return response( 200, resources.load_image( int( req ) ), 'image/jpeg' )

def handle_map():
	rup = request_uri_parts
	try:
		app = rup.pop( 0 )
	except IndexError:
		return response( 400, 'No application specified in "map" (uri {0})'.format( request_uri ) )
	if not rup and not request_uri.endswith( '/' ):
		return response( 400, 'Missing trailing / for "{0}" (uri {1})'.format( app, request_uri ) )
	res = rup if rup else [ app + '.html' ]
	return static( '/'.join( [ app ] + res ) )

def handle_tag():
	if not request_uri_parts: stage = 'upload'
	else: stage = request_uri_parts.pop( 0 )
	if stage == 'upload':
		return html( 'upload' )
	elif stage  == 'add':
		if not post_data[ 'file_field' ].filename: return html( 'upload' )
		data = post_data[ 'file_field' ].file.read()
		num = len( kml.placemarks )
		resources.save_image( num, data )
		point = kml.extract_lat_lon( data )
		kml.append( kml.placemark( point ) )
		return html( 'metadata', num = num, lat = point.lat, lon = point.lon )
	elif stage == 'metadata':
		data = post_data
		placemark = kml.placemarks[ int( request_uri_parts[ 0 ] ) ]
		placemark.appendChild( kml.name( data[ 'name' ].value ) )
		placemark.appendChild( kml.creator( data[ 'creator' ].value ) )
		placemark.appendChild( kml.description( data[ 'description' ].value ) )
		return html( 'confirm', placemark = escape( placemark.toprettyxml() ) )
	else:
		return response( 400, 'Tag application error (this should never happen).' )

def handle_edit():
	try:
		name = request_uri_parts.pop( 0 )
	except IndexError:
		return response( 400, 'No application to edit (uri {0})'.format( request_uri ) )
	if not request_uri_parts:
		return html( 'edit' )
	action = request_uri_parts.pop( 0 )
	if action == 'load':
		return response( 200, resources.load_code( name ) )
	elif action == 'save' and request_method == 'POST':
		resources.save_code( name, post_data[ 'code' ].value )
		return response( 200 )

def application( environ, start_response ):
	global __start_response, request_method, request_uri_parts, post_data, request_uri, stop
	__start_response = start_response
	request_method = environ[ 'REQUEST_METHOD' ]
	request_uri = wsgi_request_uri( environ )
	request_uri_parts = request_uri.rstrip( '/' ).split( '/' )[ 3 : ]
	post_data = FieldStorage( fp = environ[ 'wsgi.input' ], environ = environ, keep_blank_values = 1 ) if request_method == 'POST' else None
	try:
		application = request_uri_parts.pop( 0 )
	except IndexError:
		return response( 400, 'No application specified (uri {0})'.format( request_uri ) )
	if application == 'static':
		return static( '/'.join( request_uri_parts ) )
	if application == 'halt':
		halt()
		return response( 200, 'Server halted.' )
	try:
		handle = globals()[ 'handle_' + application ]
	except KeyError:
		return response( 400, 'No handler defined for "{0}" (uri {1})'.format( application, request_uri ) )
	else:
		return handle()

def halt():
	stop = True
	kml.dump()
	resources.dump()

def response( status = 200, data = '', content_type = 'text/plain; charset=utf-8' ):
	__start_response( '{0} {1}'.format( status, HTTP_CODES[ status ] ), [ ( 'Content-type', content_type ) ] )
	if isinstance( data, str ): data = [ data ]
	return data

def html( name, **kwargs ):
	return response( 200, templates.html( name, **kwargs ), 'text/html' )

def static( name ):
	try:
		data = resources.load_static( name )
	except:
		return response( 404, 'Not present in static/: ' + name )
	mime_type = guess_type( name.rsplit( '/', 1 )[ -1 ] )[ 0 ]
	if not mime_type: mime_type = 'application/octet-stream'
	return response( 200, data, mime_type )

