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

from collections import namedtuple
from logging import getLogger
from os.path import exists
from xml.dom.minidom import Document, parse

Point = namedtuple( 'Point', 'lat lon' )
Namespace = namedtuple( 'Namespace', 'uri prefix' )

NAMESPACES = {
	'kml': Namespace( 'http://www.opengis.net/kml/2.2', '' ),
	'foaf': Namespace( 'http://xmlns.com/foaf/0.1/', 'foaf' ),
	'dc': Namespace( 'http://dublincore.org/documents/dcmi-namespace/', 'dc' ),
	'xml': Namespace( 'http://www.w3.org/XML/1998/namespace', 'xml' ), 
}

LOGGER = getLogger( "server.kml" )

class Kml( object ):

	def __init__( self, filename ):
		self.filename = filename
		self.placemarks = {}
		if exists( filename ):
			LOGGER.debug( 'Reading kml from ' + filename )
			f = open( filename, 'r' )
			self.doc = parse( f )
			f.close()
			for placemark in self.doc.getElementsByTagNameNS( NAMESPACES[ 'kml' ].uri, 'Placemark' ):
				id = placemark.getAttributeNS( NAMESPACES[ 'xml' ].uri, 'id' )
				self.placemarks[ int( id.split( ':' )[ 1 ] ) ] = placemark
		else:
			LOGGER.debug( 'Creating empty kml' )
			self.doc = Document()
			root = self.doc.createElementNS( NAMESPACES[ 'kml' ].uri, 'kml' )
			root.setAttribute( 'xmlns', NAMESPACES[ 'kml' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'foaf' ].prefix, NAMESPACES[ 'foaf' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'dc' ].prefix, NAMESPACES[ 'dc' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'xml' ].prefix, NAMESPACES[ 'xml' ].uri )
			self.doc.appendChild( root )
		self.len = len( self.placemarks )
	
	def __repr__( self ):
		return self.doc.toprettyxml( encoding = 'utf-8' )

	def __getitem__( self, id ):
		if not 0 <= id < self.len: raise IndexError
		return self.placemarks[ id ]

	def __len__( self ):
		return self.len

	def append( self, placemark ):
		id = 'img:{0:03d}'.format( self.len )
		placemark.setAttributeNS( NAMESPACES[ 'xml' ].uri, '{0}:{1}'.format( NAMESPACES[ 'xml' ].prefix, 'id' ), id )
		self.doc.documentElement.appendChild( placemark )
		self.placemarks[ self.len ] = placemark
		self.len += 1
		return id

	def element( self, tagName, namespace = 'kml', child = None ):
		element = self.doc.createElementNS( 
			NAMESPACES[ namespace ].uri, 
			'{0}:{1}'.format( NAMESPACES[ namespace ].prefix, tagName ) if NAMESPACES[ namespace ].prefix else tagName 
		)
		if child: 
			if isinstance( child, str ): element.appendChild( self.doc.createTextNode( child ) )
			else: element.appendChild( child )
		return element

	def write( self ):
		f = open( self.filename, 'w' )
		self.doc.writexml( f, encoding = 'utf-8' )
		f.close()
		LOGGER.debug( 'Written kml to ' + self.filename )

	def placemark( self, point ):
		return self.element( 'Placemark', 
			child = self.element( 'Point', 
				child = self.element( 'coordinates', child = '{0},{1}'.format( point.lat, point.lon ) ) 
			) 
		)

	def creator( self, creator ):
		return self.element( 'creator', 'dc', creator )

	def name( self, name ):
		return self.element( 'name', child = name )

	def description( self, description ):
		return self.element( 'description', child = description )
