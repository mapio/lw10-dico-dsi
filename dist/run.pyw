import runpy, sys

sys.path.append( 'server.zip' )
sys.argv[ 0 ] = 'server.zip'
runpy.run_module( '__main__' )
