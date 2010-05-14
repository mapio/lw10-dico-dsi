from sys import argv
from zipfile import ZipFile
from io import BytesIO

def zip2dict( filename ):
	data = dict()
	with open( filename, 'r' ) as f:
		zf = ZipFile( f )
		for zi in zf.infolist():
			data[ zi.filename ] = zf.read( zi )
	return data

def dict2zip( data, filename ):
	with open( filename, 'w' ) as f:
		zf = ZipFile( f )
		for arcname, bytes in data.iteritems():
			zf.writestr( arcname, bytes )

def bytes2file( bytes ):
	return BytesIO( bytes )

def f( a, b = None, **kwargs ):
	print a, b, kwargs

if __name__ == '__main__':
	print zip2dict( argv[ 1 ] )
	print f( 1, x =3)
