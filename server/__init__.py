import logging

ROOT_LOGGER = logging.getLogger( "server" )
ROOT_LOGGER.setLevel( logging.DEBUG )
ch = logging.StreamHandler()
ch.setLevel( logging.DEBUG )
ch.setFormatter( logging.Formatter( "[%(asctime)s] %(levelname)s - %(name)s: %(message)s","%Y/%b/%d %H:%M:%S" ) )
ROOT_LOGGER.addHandler( ch )
