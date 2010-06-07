/**
    Copyright (C) 2010 Massimo Santini, Mattia Monga

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

function init() {
	var metadata = loadMetadata();
	points = metadata.getElementsByTagName('Point');
	for ( var i = 0; i < points.length ; i++ ) {
		point = points[ i ];
		lat_lng = point.firstChild.firstChild.nodeValue.split( ',' );
		title = point.parentNode.getElementsByTagName( 'name' )[ 0 ].firstChild.nodeValue;
		description = point.parentNode.getElementsByTagName( 'description' )[ 0 ].firstChild.nodeValue;
		src = '/img/' + parseInt( point.parentNode.attributes.getNamedItem( 'xml:id' ).value.split( '_' )[ 1 ] );		
		var ltA = parseFloat( lat_lng[ 0 ] );
		var lgA = parseFloat( lat_lng[ 1 ] );
		var s = '';
		for ( var j = 0; j < points.length; j++ ) {
			if ( j != i ) {
				lat_lng = points[ j ].firstChild.firstChild.nodeValue.split( ',' );		
				var ltB = parseFloat( lat_lng[0] );
				var lgB = parseFloat( lat_lng[1] );
				var d = gcircle( ltA, lgA, ltB, lgB );
				s += " (" + ltB + "," + lgB + ") => " + d.toFixed() + "m<br/>";
			}
		}
		marker( new Point( ltA, lgA ), title, description, src, '<p>' + s + '</p>' );
	}
}

