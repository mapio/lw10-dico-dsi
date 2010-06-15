DEBUG = true;

var millis = 0;
function tstart() {
	millis = (new Date).getTime();
}

function tstop() {
	return (new Date).getTime() - millis;
}

function a_caso( n, min, max ) {
	var res = [];
	for ( var i = 0; i < n; i++ ) res.push( Math.floor( Math.random() * ( max - min ) + min ) );
	return res;  
}

function metti( arr, elem ) {
	arr.push( elem );
}

function togli( arr, idx ) {
	if ( idx === undefined )
		return arr.shift();
	else 
	var val = arr.splice( idx, 1 );
	return val[ 0 ];
}

function smezza( arr ) {
	return [ arr.slice( 0, arr.length / 2 ), arr.slice( arr.length / 2, arr.length ) ];
}

function scambia( arr, i, j ) {
	if ( i == j ) return;
	var t = arr[ i ];
	arr[ i ] = arr[ j ];
	arr[ j ] = t;
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

function ordinato( a ) {
	for ( var i = 0; i < a.length - 1; i++ )
		if ( a[ i ] > a[ i + 1 ] ) return false;
	return true;
}

function indice_del_minimo( a, inizio ) {
	var im = inizio;
	for ( var i = inizio + 1; i < a.length; i++ )
		if ( a[ im ] > a[ i ] ) im = i;
	return im;
}

function selection_sort( a ) {
	for ( var i = 0; i < a.length - 1; i++ )
		scambia( a, i, indice_del_minimo( a, i ) ); 
	return a;
}

function merge_sort( a ) {
	if ( a.length > 1 ) {
		var m = smezza( a );
		return merge( merge_sort( m[ 0 ] ), merge_sort( m[ 1 ] ) );
	} else return a;  
}

function init() {
	input_ints( 1, 'numero di prove' );
}

function main( input ) {
	var data = table( 'N', [ 'mergesort', 'selectionsort' ] );
	var len = 100;
	var a, b, t0, t1;
	for ( var prove = input[ 0 ]; prove; prove-- ) {
		len += 100;
		a = a_caso( len, 0, 10 * len );
		tstart();
		b = merge_sort( a );
		t0 = tstop();
		if ( ! ordinato( b ) ) error( "merge_sort non ordinato: " + b );
		a = a_caso( len, 0, 10 * len );
		tstart();
		b = selection_sort( a );
		t1 = tstop();
		if ( ! ordinato( b ) ) error( "selection_sort non ordinato: " + b );
		data.addRow( [  "" + len, t0, t1 ] );
	}
	draw( data );
}
