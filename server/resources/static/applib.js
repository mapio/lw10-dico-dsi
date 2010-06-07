/**
    Copyright (C) 2010 Massimo Santini

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
**/

var map = null; // after _init_map this will be the Google map object
var Point = null; // after _init_map this will be google.maps.LatLng

/**
	Inits the Google map object (and Point function) after makeing the 
	fieldsef of id 'mapfs' (that contains the map div) visible.
*/
function _init_map( lat, lng ) {
	if ( map ) return;
	if ( lat === undefined ) {
		lat = 45.477822;
		lng = 9.169501;
	}
	var mapfs = document.getElementById( 'mapfs' );
	if ( mapfs ) mapfs.style.display = 'block';
	map = new google.maps.Map( document.getElementById( 'map' ), {
		zoom: 13,
		center: new google.maps.LatLng( lat, lng ),
		mapTypeId: google.maps.MapTypeId.ROADMAP
	} );
	Point = google.maps.LatLng;
}

/**
	If the google object is defined, it initializes the map and then calls the user init function.
*/
function _init() {
	if ( typeof google != 'undefined' ) _init_map();
	init()
}

/**
	Called by 'onclick' by the button in the input fieldset, collects inputs and passes them
	to the user main function.
*/
function _main() {
	var input = Array();
	var inputs = document.getElementsByTagName( 'input' );
	for ( i = 0; i < inputs.length; i++ ) {
	    input[ i ] = inputs[ i ].value;
	    if ( inputs[ i ].getAttribute( 'class' ) == 'int' ) input[ i ] = parseInt(input[i]);
	    if ( inputs[ i ].getAttribute( 'class' ) == 'float' ) input[ i ] = parseFloat(input[i]);
	}
	var output = document.getElementById( 'output' );
	output.value = '';
	// if map is defined we should re-init it!
	main( input );
}

/**
	Adds to the element of id 'input' a 'p' element containing n 'label' elements each one 
	containing an 'input' element of type k (stored as a string in the class attribute);
	if the optional parameter labels is defined it will be used to label input controls, more precisely
	if it is an array, then labels[ i ] (if defined) will be added as the text of the 'label' element
	enclosing i-th input; if n is 1 labels can be either an array of size one, or a string.
*/
function _input( n, k, labels ) {
	var input = document.getElementById( 'input' );	
	if ( n === 1 && typeof labels === 'string' ) labels = [ labels ];
	var para = document.createElement( 'p' )
	for ( i = 0; i < n; i++ ) {
		var ctrl = document.createElement( 'input' );
		ctrl.setAttribute( 'type', 'text' );
		ctrl.setAttribute( 'class', k );
		var lab = document.createElement( 'label' );
		if ( labels !== undefined && labels[ i ] !== undefined )
			lab.appendChild( document.createTextNode( labels[ i ] + ': ' ) );
		lab.appendChild( ctrl );
		if ( i != n - 1 ) lab.appendChild( document.createTextNode( ', ' ) );
		para.appendChild( lab );
	}
	input.appendChild( para );
}

function input_ints( n, labels ) {
	_input( n, 'int', labels );
}

function input_strings( n, labels ) {
	_input( n, 'string', labels );
}

function input_floats( n, labels ) {
	_input( n, 'float', labels );
}

function output( str, label ) {
    var output = document.getElementById( 'output' );
    output.value += (label === undefined ? '' : label) + str + '\n';
}

function marker( point, title, description, src ) {
	if ( ! map ) return;
	var marker = new google.maps.Marker( { position: point, map: map, title: title } );
	if ( description !== undefined ) {
		var content = "<h3>" + title + "</h3><p>" + description + "</p>";
		if ( src !== undefined )
			content += "<img src='" + src + "' height=100 width=100/>";
		var infowindow = new google.maps.InfoWindow( { content: "<div>" + content + "</div>" } );
		google.maps.event.addListener( marker, 'click', function() {
			infowindow.open( map, marker );
		} );
	}
}

function loadMetadata() {
	xhttp = new XMLHttpRequest();
	xhttp.open( 'GET', '/img/metadata', false );
	xhttp.send( '' );
	return xhttp.responseXML;
}
