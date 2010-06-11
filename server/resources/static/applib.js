/*
	Copyright (C) 2010 Massimo Santini, Mattia Monga

	This file is part of lw09-dico-dsi.
	lw09-dico-dsi is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	lw09-dico-dsi is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with lw09-dico-dsi.  If not, see <http://www.gnu.org/licenses/>.
*/

var map = null; // after _init_map this will be instantiated as a google.maps.Map
var Point = null; // after _init_map this will be google.maps.LatLng
var Table = null; // after _init_chart this will be instantiatend as a google.visualization.DataTable

/**
	Inits the Google map object (and Point function) after makeing the 
	fieldsef of id 'mapfs' (that contains the map div) visible.
*/
function _init_map( lat, lng ) {
	if ( map ) return;
	if ( typeof google.maps == 'undefined' ) return;
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

function _init_chart() {
	if ( typeof google.visualization == 'undefined' ) return;
	var chartfs = document.getElementById( 'chartfs' );
	if ( chartfs ) chartfs.style.display = 'block';
	Table = google.visualization.DataTable;
}

/**
	If the google object is defined, it initializes the map and then calls the user init function.
*/
function _init() {
	if ( typeof google != 'undefined' ) {
		_init_map();
		_init_chart();
	}
	init();
}

/**
	Called by 'onclick' by the button in the input fieldset, collects inputs and passes them
	to the user main function.
*/
var oer;
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
	try {
		main( input );
	} catch ( err ) {
		oer = err;
		var txt = "There was an error on this page.\n\n";
		txt += "Error description: " + err;
		error( txt );
	}
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
	for ( var i = 0; i < n; i++ ) {
		var ctrl = document.createElement( 'input' );
		ctrl.setAttribute( 'type', 'text' );
		ctrl.setAttribute( 'class', k );
		ctrl.setAttribute( 'size', '60' );
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
    output.value += ( label === undefined ? '' : label ) + str + '\n';
}

function error( str, label ) {
    var error = document.getElementById( 'error' );
    error.value += ( label === undefined ? '' : label ) + str + '\n';
}

function marker( point, title, description, src, extra ) {
	if ( ! map ) return;
	if ( title === undefined ) title = '';
	var marker = new google.maps.Marker( { position: point, map: map, title: title } );
	if ( description !== undefined ) {
		var content = "<h3>" + title + "</h3><p>" + description + "</p>";
		if ( src !== undefined )
			content += "<img src='" + src + "' height=100 width=100/>";
		if ( extra !== undefined )
			content += extra;
		var infowindow = new google.maps.InfoWindow( { content: "<div>" + content + "</div>" } );
		google.maps.event.addListener( marker, 'click', function() {
			infowindow.open( map, marker );
		} );
	}
}

function draw( data ) {
	var chart = new google.visualization.LineChart( document.getElementById( 'chart' ) );
	chart.draw( data, { curveType: "none", width: 400, height: 200 } );
}

function loadMetadata() {
	var xhttp = new XMLHttpRequest();
	xhttp.open( 'GET', '/img/metadata', false );
	xhttp.send( '' );
	return xhttp.responseXML;
}

/* A few xpath helpers */

function _nsResolver( prefix ) {  
	var ns = {  
		'xml': 'http://www.w3.org/XML/1998/namespace',
		'kml': 'http://www.opengis.net/kml/2.2',
		'dc': 'http://dublincore.org/documents/dcmi-namespace/',
		'foaf': 'http://xmlns.com/foaf/0.1/',
		'xhtml' : 'http://www.w3.org/1999/xhtml',
	};  
	return ns[ prefix ] || null;
}  

function xpath( data, query ) {
	var eval_res = data.evaluate( query, data.documentElement, _nsResolver, XPathResult.ANY_TYPE, null );
	var res = Array();
	var i;
	while ( i = eval_res.iterateNext() ) res.push( i );
	return res;
}

var _serializer = new XMLSerializer();

function serialize( res ) {
	if ( ! ( res instanceof Array ) ) return _serializer.serializeToString( res );
	var str = Array();
	for ( var i = 0; i < res.length; i++ ) str.push( _serializer.serializeToString( res[ i ] ) );
	return str;
}
