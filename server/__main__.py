# Copyright (C) 2010 Massimo Santini
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from logging import StreamHandler, Formatter, getLogger, DEBUG
from os import path
from sys import argv
from wsgiref.simple_server import make_server

import server

if __name__ == '__main__':
	
	ROOT_LOGGER = getLogger( "server" )
	ROOT_LOGGER.setLevel( DEBUG )
	ch = StreamHandler()
	ch.setLevel( DEBUG )
	ch.setFormatter( Formatter( "[%(asctime)s] %(levelname)s - %(name)s: %(message)s","%Y/%b/%d %H:%M:%S" ) )
	ROOT_LOGGER.addHandler( ch )
	
	simple_server = make_server( 'localhost', 8000, server.application )	
	try:
		while not server.stop: simple_server.handle_request()
	except KeyboardInterrupt:
		pass
	server,halt()
