from logging import StreamHandler, Formatter, getLogger, DEBUG
from os import path
from webbrowser import open_new
from wsgiref.simple_server import make_server

from kml import Kml
from server import Context

if __name__ == '__main__':
	
	ROOT_LOGGER = getLogger( "server" )
	ROOT_LOGGER.setLevel( DEBUG )
	ch = StreamHandler()
	ch.setLevel( DEBUG )
	ch.setFormatter( Formatter( "[%(asctime)s] %(levelname)s - %(name)s: %(message)s","%Y/%b/%d %H:%M:%S" ) )
	ROOT_LOGGER.addHandler( ch )
	
	kml = Kml( path.join( 'img', 'metadata.kml' ) )
	context = Context( kml )	
	server = make_server( 'localhost', 8000, context )	
	#open_new( 'http://localhost:8000/tag/upload' )
	try:
		while not context.stop: server.handle_request()
	except KeyboardInterrupt:
		pass
	kml.write()	