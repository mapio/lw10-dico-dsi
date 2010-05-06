function initialize() {
	var map = new google.maps.Map( document.getElementById( 'map_canvas' ), {
		zoom: 13,
		center: new google.maps.LatLng( 45.477822, 9.169501 ),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	} );
	var metadata = loadMetadata();
	points = metadata.getElementsByTagName('Point');
	for ( var i = 0; i < points.length ; i++ ) addMarker( points[ i ], map );
}

function loadMetadata() {
	xhttp = new XMLHttpRequest();
	xhttp.open( 'GET', '/img/metadata', false );
	xhttp.send( '' );
	return xhttp.responseXML;
}

function addMarker( point, map ) {
	lat_lon = point.firstChild.firstChild.nodeValue.split( ',' );
	title = point.parentNode.getElementsByTagName( 'name' )[ 0 ].firstChild.nodeValue;
	description = point.parentNode.getElementsByTagName( 'description' )[ 0 ].firstChild.nodeValue;
	src = "/img/" + parseInt( point.parentNode.attributes.getNamedItem('xml:id').value.split( ':' )[ 1 ] );
	var marker = new google.maps.Marker( {
		position: new google.maps.LatLng( parseFloat( lat_lon[ 0 ] ), parseFloat( lat_lon[ 1 ] ) ), 
		map: map, 
		title: title
	} );
	var infowindow = new google.maps.InfoWindow( {
	    content: "<div><h3>" + title + "</h3><p>" + description + "</p><img src='" + src + "' height=100 width=100/></div>"
	} );
	google.maps.event.addListener( marker, 'click', function() {
		infowindow.open( map, marker );
	} );	
}
