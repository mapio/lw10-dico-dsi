DEBUG = true;

function init() {
	input_ints( 1, 'numero di prove' );
}

function main( input ) {
	var data = table( 'N', [ 'mergesort', 'selectionsort', 'bubblesort' ] );
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
		a = a_caso( len, 0, 10 * len );
		tstart();
		b = bubble_sort( a );
		t2 = tstop();
		if ( ! ordinato( b ) ) error( "bubble_sort non ordinato: " + b );
		data.addRow( [  "" + len, t0, t1, t2 ] );
	}
	draw( data );
}
