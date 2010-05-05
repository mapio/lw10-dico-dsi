# -*- coding: utf8 -*-

from cgi import FieldStorage
from os import path, access, R_OK
from shutil import copyfileobj
from string import Template
from webbrowser import open_new
from wsgiref.simple_server import make_server
from wsgiref.util import request_uri

def http_response( start_response, status = 200, content_type = 'text/plain; charset=utf-8', data = '' ):
	HTTP_CODES = {
		200: 'OK',
		400: 'BAD REQUEST',
		401: 'UNAUTHORIZED',
		403: 'FORBIDDEN',
		404: 'NOT FOUND',
		405: 'METHOD NOT ALLOWED',
		500: 'INTERNAL SERVER ERROR',
	}
	start_response( '{0} {1}'.format( status, HTTP_CODES[ status ] ), [ ( 'Content-type', content_type ) ] )
	if isinstance( data, str ): data = [ data ]
	return data

def html_response( start_response, title, body ):
	base_page = Template( """
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
	<title>$title</title>
</head>
<body>
$body
</body>
</html>
""" )
	return http_response( start_response, 200, content_type = 'text/html', data = base_page.substitute( title = title, body = body ) )

def handle_img( start_response, basename ):
	filename = path.join( 'img', basename + '.jpg' )
	if not path.exists( filename ) or not path.isfile( filename ):
		return http_response( start_response, 404, data = "File does not exist: " + filename )
	if not access( filename, R_OK ):
		return http_response( start_response, 401, data = "You do not have permission to access this file: " + filename )
	return http_response( start_response, 200, content_type = 'image/jpeg', data = open( filename, 'rb' ) )

upload_body = """
<form method="post" enctype="multipart/form-data">
<input type="hidden" name="stage" value="upload">
<input type="file" name="file_field">
<input type="submit" value="Upload" name="submit_field">
</form>
"""

add_metadata = Template( """
<img height="400" width="400" src="/img/$name">
<img src="http://maps.google.com/maps/api/staticmap?center=40.714728,-73.998672&zoom=12&size=400x400&sensor=false">
<form method="post" enctype="multipart/form-data">
<input type="hidden" name="stage" value="metadata">
<input type="hidden" name="name" value="$name">
<label for="metadata_field">Metadata: </label> <input type="text" name="metadata_field">
<input type="submit" value="Annota" name="submit_field">
</form>
""" )

confirm ="""
"""

def handle_app( start_response, environ ):
	if environ[ 'REQUEST_METHOD' ] == 'POST':
		fs = FieldStorage( fp = environ[ 'wsgi.input' ], environ = environ, keep_blank_values = 1 )
		if fs[ 'stage' ].value == 'upload':
			form_file = fs[ 'file_field' ]
			dest = open( path.join( 'img', '001' + '.jpg' ), 'wb' )
			copyfileobj( form_file.file, dest )
			dest.close()
			return html_response( start_response, "Add metadata", add_metadata.substitute( name = "001" ) )
	else:
		return html_response( start_response, "Upload", upload_body )
	return http_response( start_response, 400 )

def application( environ, start_response ):
	path = request_uri( environ ).split( '/' )[ 3 : ]
	if path[ 0 ] == 'img':
		return handle_img( start_response, path[ 1 ] )
	elif path[ 0 ] == 'app':
		return handle_app( start_response, environ )
	else:
		return http_response( start_response, 400, data = ', '.join( path ) )

if __name__ == '__main__':
	server = make_server( 'localhost', 8000, application )
	open_new( "http://localhost:8000/app" )
	server.serve_forever()