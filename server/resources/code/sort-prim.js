function scambia( arr, i, j ) {
	if ( i == j ) return;
	var t = arr[ i ];
	arr[ i ] = arr[ j ];
	arr[ j ] = t;
}

function compara( x, y ) {
	if ( x < y ) return -1;
	if ( x == y ) return 0;
	return 1;
}
