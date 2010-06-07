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

function init() {
	input_ints( 1, 'Numero di punti' );
}

function main( input ) {
	var data = new Table();
	data.addColumn( 'number', 'linea' );
	data.addColumn( 'number', 'parabola' );
	for ( var i = 0; i < input[ 0 ]; i++ ) data.addRow( [ i, i * i ] );
	draw( data );
}
