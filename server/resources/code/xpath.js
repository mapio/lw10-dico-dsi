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
	input_strings( 1,'query' );
	output( 'Prova con: "//kml:Placemark/dc:creator" (senza virgolette)' );
}

function main( input ) {
	var d = loadMetadata();
	var r = xpath( d, input[ 0 ] );
	output( '' + serialize( r ) );
}
