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
		if ( ! ( labels === undefined || labels[ i ] === undefined ) )
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

function output( str ) {
	var output = document.getElementById( 'output' );
	output.value += str + '\n';
}

function _main() {
	var input = Array();
	var inputs = document.getElementsByTagName( 'input' );
	for ( i = 0; i < inputs.length; i++ ) {
		input[ i ] = inputs[ i ].value;
		if ( inputs[ i ].getAttribute( 'class' ) == 'int' ) input[ i ] -= 0;
	}
	var output = document.getElementById( 'output' );
	output.value = '';
	main( input );
}
