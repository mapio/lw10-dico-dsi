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
	input_ints( 2, [ "primo addendo", "secondo addendo" ] ); // aggiunge due campi "int" alla form
	input_strings( 2, [ "prima parola", "seconda parola" ] ); // aggiunge due campi "string" alla form
}

// main è chiamato dall'onclick del bottone della form

function main( input ) {
	output( input[ 0 ] + input[ 1 ] );
	output( input[ 2 ] + input[ 3 ] );
}
