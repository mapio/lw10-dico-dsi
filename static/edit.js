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
