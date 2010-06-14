# Copyright (C) 2010 Massimo Santini
# 
# This file is part of lw09-dico-dsi.
#
# lw09-dico-dsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# lw09-dico-dsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with lw09-dico-dsi.  If not, see <http://www.gnu.org/licenses/>.

from cgi import FieldStorage, escape
from logging import getLogger
from mimetypes import guess_type
from re import sub
from wsgiref.util import request_uri as wsgi_request_uri

LOGGER = getLogger( "server.server" )

import kml
import resources
import templates

request_method = None
request_uri = None
request_uri_parts = None
post_data = None
stop = False

__start_response = None

def handle_addapp():
	if request_method == 'POST':
		try:
			javascript = [ _.value for _ in post_data[ 'javascript' ] ]
		except ( TypeError, KeyError ): # not iterable, at most one value
			try:
				javascript = post_data[ 'javascript' ].value
			except KeyError: # no value present
				javascript = []
		templates.addioapp( 
			app = post_data[ 'key' ].value, 
			title = post_data[ 'title' ].value.decode( 'utf8' ),
			javascript = javascript
		)
		return html( 'appscfg', appscfg = resources.load_appscfg() )
	else:
		return html( 'addapp' )
		
def handle_edit():
	try:
		name = request_uri_parts.pop( 0 )
		code = resources.load_code( name )
	except IndexError:
		return http( 400, 'No application to edit (uri {0})'.format( request_uri ) )
	except KeyError:
		return http( 400, 'No code present for application "{0}"'.format( name ) )
	if not request_uri_parts:
		return html( 'edit' )
	action = request_uri_parts.pop( 0 )
	if action == 'load':
		return http( 200, code, content_type = 'text/javascript; charset=utf-8' )
	elif action == 'save' and request_method == 'POST':
		resources.save_code( name, post_data[ 'code' ].value )
		return http( 200 )

def handle_halt():
	halt()
	return http( 200, 'Server halted.' )

def handle_home():
	apps = []
	for k in templates.USER_APPS:
		apps.append( '<li>{0}: <a href="/edit/{1}">edit</a>, <a href="/run/{1}">run</a></li>'.format( templates.ALL[ k ].title, k ) )
	return html( 'home', apps = '\n'.join( apps ) )
	
def handle_img():
	req = request_uri_parts[ 0 ]
	if req == 'metadata':
		return http( 200, kml.string(), 'application/vnd.google-earth.kml+xml' )
	else:
		return http( 200, resources.load_image( int( req ) ), 'image/jpeg' )

def handle_run():
	rup = request_uri_parts
	try:
		app = rup.pop( 0 )
	except IndexError:
		return http( 400, 'No application specified to run (uri {0})'.format( request_uri ) )
	try:
		return html( app )
	except KeyError:
		return http( 400, 'No configuration present for application "{0}"'.format( app ) )

def handle_shell():
	return html( 'shell' )

def handle_static():
	name = '/'.join( request_uri_parts )
	try:
		data = resources.load_static( name )
	except:
		return http( 404, 'Not present in static/: ' + name )
	mime_type = guess_type( name.rsplit( '/', 1 )[ -1 ] )[ 0 ]
	if not mime_type: mime_type = 'application/octet-stream'
	return http( 200, data, mime_type )

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
		return http( 400, 'Tag application error (this should never happen).' )

def application( environ, start_response ):
	global request_method, request_uri, request_uri_parts, post_data, __start_response 
	request_method = environ[ 'REQUEST_METHOD' ]
	request_uri = sub( r'([^:])/+', r'\1/', sub( r'(\?|#).*$', '', wsgi_request_uri( environ ) ) ) # we remove the query and anchor part
	request_uri_parts = request_uri.rstrip( '/' ).split( '/' )[ 3 : ]
	post_data = FieldStorage( fp = environ[ 'wsgi.input' ], environ = environ, keep_blank_values = 1 ) if request_method == 'POST' else None
	__start_response = start_response
	try:
		application = request_uri_parts.pop( 0 )
	except IndexError:
		#return http( 400, 'No application specified (uri {0})'.format( request_uri ) )
		return handle_home()
	try:
		handle = globals()[ 'handle_' + application ]
	except KeyError:
		return http( 400, 'No handler defined for "{0}" (uri {1})'.format( application, request_uri ) )
	else:
		return handle()

def halt():
	global stop
	LOGGER.info( 'Clean halt in progress...' )
	if not stop:
		stop = True
		kml.dump()
		resources.dump()

def http( status = 200, data = '', content_type = 'text/plain; charset=utf-8' ):
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
	__start_response( '{0} {1}'.format( status, HTTP_CODES[ status ] ), [ ( 'Content-type', content_type ) ] )
	if isinstance( data, str ): data = [ data ]
	return data

def html( name, **kwargs ):
	return http( 200, templates.html( name, **kwargs ), 'text/html' )
