# Copyright (C) 2010 Massimo Santini
# 
# This file is part of lw09-dico-dsi.
#
# lw09-dico-dsi is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# lw09-dico-dsi is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with lw09-dico-dsi.  If not, see <http://www.gnu.org/licenses/>.

from atexit import register
from logging import Formatter, getLogger, DEBUG
from logging.handlers import RotatingFileHandler
from os import path
try:
	from signal import signal, SIGHUP
except ImportError:
	pass
from sys import argv
from wsgiref.simple_server import make_server, WSGIRequestHandler

ROOT_LOGGER = getLogger( 'server' )
ROOT_LOGGER.setLevel( DEBUG )
lh = RotatingFileHandler( 'server.log', maxBytes = 1 * 1024 * 1024 , backupCount = 2 )
lh.setLevel( DEBUG )
lh.setFormatter( Formatter( "[%(asctime)s] %(levelname)s - %(name)s: %(message)s","%Y/%b/%d %H:%M:%S" ) )
ROOT_LOGGER.addHandler( lh )

class LogMixin:
	def log_message( self, format, *args ):
		ROOT_LOGGER.info( 'WSGIRequestHandler: %s - - [%s] %s' % ( self.address_string(), self.log_date_time_string(), format % args ) )

class LogginWSGIRequestHandler( LogMixin, WSGIRequestHandler ): pass

import server

register( server.halt )
try:
	signal( SIGHUP, lambda signum, frame: server.halt() )
except NameError:
	pass

simple_server = make_server( 'localhost', 8000, server.application, handler_class = LogginWSGIRequestHandler )	
ROOT_LOGGER.info( 'Serving on http://localhost:8000/' )
try:
	while not server.stop: simple_server.handle_request()
except KeyboardInterrupt:
	pass
