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

function _input( n, k ) {
	var input = document.getElementById( 'input' );
	for ( i = 0; i < n; i++ ) {
		var ctrl = document.createElement( 'input' );
		ctrl.setAttribute( 'type', 'text' );
		ctrl.setAttribute( 'class', k );
		input.appendChild( ctrl );
	}
}

function input_ints( n ) {
	_input( n, 'int' );
}

function input_strings( n ) {
	_input( n, 'string' );
}

function output( str ) {
	var output = document.getElementById( 'output' );
	output.value += str + '\n';
}
function _main() {
	var input = Array();
	var inputs = document.getElementById( 'input' ).childNodes;
	for ( i = 0; i < inputs.length; i++ ) {
		input[ i ] = inputs[ i ].value;
		if ( inputs[ i ].getAttribute( 'class' ) == 'int' ) input[ i ] -= 0;
	}
	main( input );
}
