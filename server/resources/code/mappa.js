function init() {
	var metadata = loadMetadata();
	var points = metadata.getElementsByTagName('Point');
	for ( var i = 0; i < points.length ; i++ ) disegna( points[ i ] );
}

function disegna( point ) {
	var lat_lng = point.firstChild.firstChild.nodeValue.split( ',' );
	var title = point.parentNode.getElementsByTagName( 'name' )[ 0 ].firstChild.nodeValue;
	var description = point.parentNode.getElementsByTagName( 'description' )[ 0 ].firstChild.nodeValue;
	var src = '/img/' + parseInt( point.parentNode.attributes.getNamedItem( 'xml:id' ).value.split( '_' )[ 1 ] );
	marker( new Point( lat_lng[ 0 ], lat_lng[ 1 ] ), title, description, src );
}
