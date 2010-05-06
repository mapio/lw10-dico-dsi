function initialize() {
	var map = new google.maps.Map( document.getElementById( 'map_canvas' ), {
		zoom: 13,
		center: new google.maps.LatLng( 45.477822, 9.169501 ),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	} );
}
/*
function loadMetadata() {
	xhttp = new XMLHttpRequest();
	xhttp.open( 'GET', '/img/metadata', false );
	xhttp.send( '' );
	xml = xhttp.responseXML;

	points = xml.getElementsByTagName('Point');
	for (var i = 0; i < points.length ; i++) {
		id = points[ i ].parentNode.attributes.getNamedItem('xml:id').value;
		ll = points[ i ].firstChild.firstChild.nodeValue.split( ',' );
		lat = parseFloat( ll[ 0 ] )
		lon = parseFloat( ll[ 1 ] )
		alert( lat );
	}
}
*/