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

// init è chiamato dall'onload di body

function init() {
	input_floats( 2, [ 'latitudine', 'longitudine' ] );
	output( 'Prova con le coordinate: 45.477822, 9.169501' );
}

// main è chiamato dall'onclick del bottone della form

function main( input ) {
	var p = new Point( input[ 0 ], input[ 1 ] );
	marker( p );
}
