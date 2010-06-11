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

from collections import namedtuple
from io import BytesIO
from logging import getLogger
from xml.dom.minidom import Document

from exif import process_file

Point = namedtuple( 'Point', 'lat lon' )
Namespace = namedtuple( 'Namespace', 'uri prefix' )

NAMESPACES = {
	'kml': Namespace( 'http://www.opengis.net/kml/2.2', '' ),
	'foaf': Namespace( 'http://xmlns.com/foaf/0.1/', 'foaf' ),
	'dc': Namespace( 'http://dublincore.org/documents/dcmi-namespace/', 'dc' ),
	'xml': Namespace( 'http://www.w3.org/XML/1998/namespace', 'xml' ), 
}

LOGGER = getLogger( "server.kml" )

import resources

doc = resources.load_metadata()
if doc:
	xml_placemarks = doc.getElementsByTagNameNS( NAMESPACES[ 'kml' ].uri, 'Placemark' )
	placemarks = [ None ] * len( xml_placemarks )
	for placemark in xml_placemarks:
		id = placemark.getAttributeNS( NAMESPACES[ 'xml' ].uri, 'id' )
		placemarks[ int( id.split( '_' )[ 1 ] ) ] = placemark
else:
	doc = Document()
	root = doc.createElementNS( NAMESPACES[ 'kml' ].uri, 'kml' )
	root.setAttribute( 'xmlns', NAMESPACES[ 'kml' ].uri )
	root.setAttribute( 'xmlns:' + NAMESPACES[ 'foaf' ].prefix, NAMESPACES[ 'foaf' ].uri )
	root.setAttribute( 'xmlns:' + NAMESPACES[ 'dc' ].prefix, NAMESPACES[ 'dc' ].uri )
	root.setAttribute( 'xmlns:' + NAMESPACES[ 'xml' ].prefix, NAMESPACES[ 'xml' ].uri )
	doc.appendChild( root )
	placemarks = []

def dump():
	resources.save_metadata( string() )

def string():
	return doc.toxml( 'utf-8' )
	
def append( placemark ):
	id = 'img_{0:03d}'.format( len( placemarks ) )
	placemark.setAttributeNS( NAMESPACES[ 'xml' ].uri, '{0}:{1}'.format( NAMESPACES[ 'xml' ].prefix, 'id' ), id )
	placemarks.append( placemark )
	doc.documentElement.appendChild( placemark )

def element( tagName, namespace = 'kml', child = None ):
	element = doc.createElementNS( 
		NAMESPACES[ namespace ].uri, 
		'{0}:{1}'.format( NAMESPACES[ namespace ].prefix, tagName ) if NAMESPACES[ namespace ].prefix else tagName 
	)
	if child: 
		if isinstance( child, str ): element.appendChild( doc.createTextNode( child ) )
		else: element.appendChild( child )
	return element

def placemark( point ):
	return element( 'Placemark', 
		child = element( 'Point', 
			child = element( 'coordinates', child = '{0},{1}'.format( point.lat, point.lon ) ) 
		) 
	)

def creator( creator ):
	return element( 'creator', 'dc', creator )

def name( name ):
	return element( 'name', child = name )

def description( description ):
	return element( 'description', child = description )
	
def extract_lat_lon( data ):
	def rat2float( vals ):
		return [ float( _.num ) / float( _.den ) for _ in vals ]
	fp = BytesIO( data )
	tags = process_file( fp )
	fp.close()
	try:
		lat_ref = tags[ 'GPS GPSLatitudeRef' ].values
		lat_rat = rat2float( tags[ 'GPS GPSLatitude' ].values )
		lon_ref = tags[ 'GPS GPSLongitudeRef' ].values
		lon_rat = rat2float( tags[ 'GPS GPSLongitude' ].values )
	except KeyError:
		return Point( 0, 0 ) # TODO: do better!
	return Point(
		( lat_rat[ 0 ] + lat_rat[ 1 ] / 60 + lat_rat[ 2 ] / 3600 ) * ( 1 if lat_ref == "N" else -1 ),
		( lon_rat[ 0 ] + lon_rat[ 1 ] / 60 + lon_rat[ 2 ] / 3600 ) * ( -1 if lon_ref == "W" else 1 )
	)
