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

function indice_del_minimo( a, inizio ) {
	var im = inizio;
	for ( var i = inizio + 1; i < a.length; i++ )
		if ( a[ im ] > a[ i ] ) im = i;
	return im;
}
