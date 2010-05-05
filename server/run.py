# -*- coding: utf8 -*-

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

def handle_img( start_response, num ):
	filename = path.join( 'img', '{0:03d}.jpg'.format( num ) )
	if not path.exists( filename ) or not path.isfile( filename ):
		return http_response( start_response, 404, data = "File does not exist: " + filename )
	if not access( filename, R_OK ):
		return http_response( start_response, 401, data = "You do not have permission to access this file: " + filename )
	return http_response( start_response, 200, content_type = 'image/jpeg', data = open( filename, 'rb' ) )

upload = """
<form method="post" enctype="multipart/form-data">
<input type="hidden" name="stage" value="upload">
<input type="file" name="file_field">
<input type="submit" value="Upload" name="submit_field">
</form>
"""

add_metadata = Template( """
<img height="400" width="400" src="/img/$num">
<img src="http://maps.google.com/maps/api/staticmap?center=$lat,$lon&zoom=15&size=400x400&sensor=false&markers=color:blue|$lat,$lon">
<form method="post" enctype="multipart/form-data">
<input type="hidden" name="stage" value="metadata">
<input type="hidden" name="num" value="$num">
<label for="metadata_field">Metadata: </label> <input type="text" name="metadata_field">
<input type="submit" value="Annota" name="submit_field">
</form>
""" )

confirm ="""
<p>Immagine aggiunta.
"""

def handle_app( start_response, environ ):
	if environ[ 'REQUEST_METHOD' ] == 'POST':
		fs = FieldStorage( fp = environ[ 'wsgi.input' ], environ = environ, keep_blank_values = 1 )
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
			return html_response( start_response, "Aggiungi metadati", add_metadata.substitute( num = len( data ) - 1, lat = point.lat, lon = point.lon ) )
		elif stage == 'metadata':
			return html_response( start_response, "Conferma", confirm )
	else:
		return html_response( start_response, "Upload", upload )
	return http_response( start_response, 400 )

def application( environ, start_response ):
	path = request_uri( environ ).split( '/' )[ 3 : ]
	if path[ 0 ] == 'img':
		return handle_img( start_response, int( path[ 1 ] ) )
	elif path[ 0 ] == 'app':
		return handle_app( start_response, environ )
	else:
		return http_response( start_response, 400, data = ', '.join( path ) )

if __name__ == '__main__':
	server = make_server( 'localhost', 8000, application )
	open_new( "http://localhost:8000/app" )
	server.serve_forever()