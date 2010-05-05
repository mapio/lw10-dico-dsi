import xml.dom.minidom

from collections import namedtuple

Point = namedtuple( 'Point', 'lat lon' )
Namespace = namedtuple( 'Namespace', 'uri prefix' )

NAMESPACES = {
	'kml': Namespace( 'http://www.opengis.net/kml/2.2', '' ),
	'foaf': Namespace( 'http://xmlns.com/foaf/0.1/', 'foaf' ),
	'dc': Namespace( 'http://dublincore.org/documents/dcmi-namespace/', 'dc' ),
	'xml': Namespace( 'http://www.w3.org/XML/1998/namespace', 'xml' ), 
}

class Kml( object ):

	def __init__( self, path = None ):
		if path:
			f = open( path, 'r' )
			self.doc = xml.dom.minidom.parse( f )
			f.close()
			self.placemarks = {}
			for placemark in self.doc.getElementsByTagNameNS( NAMESPACES[ 'kml' ].uri, 'Placemark' ):
				id = placemark.getAttributeNS( NAMESPACES[ 'xml' ].uri, 'id' )
				self.placemarks[ int( id.split( ':' )[ 1 ] ) ] = placemark
			self.len = len( self.placemarks )
		else:
			self.doc = xml.dom.minidom.Document()
			root = self.doc.createElementNS( NAMESPACES[ 'kml' ].uri, 'kml' )
			root.setAttribute( 'xmlns', NAMESPACES[ 'kml' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'foaf' ].prefix, NAMESPACES[ 'foaf' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'dc' ].prefix, NAMESPACES[ 'dc' ].uri )
			root.setAttribute( 'xmlns:' + NAMESPACES[ 'xml' ].prefix, NAMESPACES[ 'xml' ].uri )
			self.doc.appendChild( root )
			self.placemarks = {}
			self.len = 0
	
	def __repr__( self ):
		return self.doc.toprettyxml( encoding = 'utf-8' )

	def __getitem__( self, id ):
		if not 0 <= id < self.len : raise IndexError
		return self.placemarks[ id ]

	def __len__( self ):
		return self.len

	def append( self, placemark ):
		id = 'img:{0:03d}'.format( self.len )
		placemark.setAttributeNS( NAMESPACES[ 'xml' ].uri, '{0}:{1}'.format( NAMESPACES[ 'xml' ].prefix, 'id' ), id )
		self.doc.documentElement.appendChild( placemark )
		self.len += 1

	def __element( self, tagName, namespace = 'kml', text = None, child = None ):
		element = self.doc.createElementNS( NAMESPACES[ namespace ].uri, '{0}:{1}'.format( NAMESPACES[ namespace ].prefix, tagName ) if NAMESPACES[ namespace ].prefix else tagName )
		if text: element.appendChild( self.doc.createTextNode( text ) )
		if child: element.appendChild( child )
		return element

	def write( self, path ):
		f = open( path, 'w' )
		self.doc.writexml( f, encoding = 'utf-8' )
		f.close()
	
	def placemark( self, point ):
		placemark = self.__element( 'Placemark' )
		placemark.appendChild( self.__element( 'Point', child = self.__element( 'coordinates', text = '{0},{1}'.format( point.lat, point.lon ) ) ) )
		return placemark
	
	def creator( self, creator ):
		return self.__element( 'creator', namespace = 'dc', text = creator )

	def name( self, name ):
		return self.__element( 'name', text = name )
	
	def description( self, description ):
		return self.__element( 'description', text = description )

if __name__ == '__main__':
	import sys
	
	if len( sys.argv ) == 2:
		data = Kml( sys.argv[ 1 ] )
		print len( data )
		data[ 0 ].appendChild( data.creator( "Massimo Santini" ) )
		data[ 1 ].appendChild( data.name( "Una foto" ) )
		for x in data: print x.toprettyxml()
	else:
		data = Kml()
		data.append( data.placemark( Point( 1, 2 ) ) )
		data.append( data.placemark( Point( 3, 4 ) ) )
		print data
		data.write( 'test.xml' )