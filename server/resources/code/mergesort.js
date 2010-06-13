DEBUG = true;

var millis = 0;
function start() {
	var d = new Date();
	millis = d.getMilliseconds();
}

function stop() {
	var d = new Date();
	return d.getMilliseconds() - millis;
}

function aCaso( n, min, max ) {
	var res = [];
	for ( var i = 0; i < n; i++ ) res.push( Math.floor( Math.random() * ( max - min ) + min ) );
	return res;  
}

function metti( arr, elem ) {
	arr.push( elem );
}

function togli( arr ) {
	return arr.shift();
}

function smezza( arr ) {
	return [ arr.slice( 0, arr.length / 2 ), arr.slice( arr.length / 2, arr.length ) ];
}

function merge( a, b ) {
	var c = [];

	while ( a.length && b.length ) 
		if ( a[0] <= b[0] ) metti( c, togli( a ) );
		else metti( c, togli( b ) );
	while ( a.length ) metti( c, togli( a ) );
	while ( b.length ) metti( c, togli( b ) );

	return c;
}

function sort( a ) {
	if ( a.length > 1 ) {
		var m = smezza( a );
		return merge( sort( m[ 0 ] ), sort( m[ 1 ] ) );
	} else return a;  
}

function init() {}

function main( input ) {
	var a = aCaso( 10, 0, 10 );

	var data = new Table();
	data.addColumn( 'string', 'N' );
	data.addColumn( 'number', 'ms' );
	for ( var len = 10; len < 100000; len *= 2 ) {
		var a = aCaso( len, 0, 10 * len );
		start();
		sort( a );
		var t = stop();
		data.addRow( [  "" + len, t ] );
	}
	draw( data );
}
