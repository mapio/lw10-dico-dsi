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

var editor = null;

function init() {
	editor = CodeMirror.fromTextArea( "code", {
		parserfile: [ "tokenizejavascript.js", "parsejavascript.js" ],
		stylesheet: "/static/codemirror/jscolors.css",
		path: "/static/codemirror/",
		lineNumbers: true,
		height: "480px",
		content: load(),
	} );
	editor.focus();
}

function load() {
	var xhr = new XMLHttpRequest();
	xhr.open( 'GET', document.URL.replace( /\/+$/, '' ) + '/load', false );
	xhr.send( null );
	return xhr.responseText;
}

function revert() {
	editor.setCode( load() );
}

function run() {
	window.location = document.URL.replace( /\/+$/, '' ).replace( /\/edit\//, '/run/' );
}

function save() {
	var data = 
		'--9a644c6e5fd25298e3d4763b7354617d\r\n' +
		'Content-Disposition: form-data; name="code"\r\n' +
		'\r\n' + 
		editor.getCode() + '\r\n' +
		'--9a644c6e5fd25298e3d4763b7354617d--\r\n'
	var xhr = new XMLHttpRequest();
	xhr.open( 'POST', document.URL.replace( /\/+$/, '' ) + '/save', false );
	xhr.setRequestHeader( 'Content-Type', 'multipart/form-data; boundary=9a644c6e5fd25298e3d4763b7354617d' );
	xhr.send( data );
}
