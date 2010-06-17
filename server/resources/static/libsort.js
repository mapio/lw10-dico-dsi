var millis = 0;
function tstart() {
	millis = (new Date).getTime();
}

function tstop() {
	return (new Date).getTime() - millis;
}

function a_caso( n, min, max ) {
	var res = [];
	if ( min === undefined ) min = 0;
	if ( max === undefined ) max = n;
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
