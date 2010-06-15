function scambia( arr, i, j ) {
	if ( i == j ) return;
	var t = arr[ i ];
	arr[ i ] = arr[ j ];
	arr[ j ] = t;
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

function init() {
	input_ints( 1, 'numero di elementi' );
}

function main( input ) {
	var a = a_caso( input[ 0 ], 0, 10 );
	selection_sort( a );
	output( a );
}
