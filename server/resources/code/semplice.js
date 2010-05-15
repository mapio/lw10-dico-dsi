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
  src = "/img/" + parseInt( point.parentNode.attributes.getNamedItem('xml:id').value.split( '_' )[ 1 ] );
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
