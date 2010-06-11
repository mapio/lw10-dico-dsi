/*
	Copyright (C) 2010 Massimo Santini

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
