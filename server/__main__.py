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

from logging import StreamHandler, Formatter, getLogger, DEBUG
from os import path
from sys import argv
from wsgiref.simple_server import make_server

ROOT_LOGGER = getLogger( "server" )
ROOT_LOGGER.setLevel( DEBUG )
sh = StreamHandler()
sh.setLevel( DEBUG )
sh.setFormatter( Formatter( "[%(asctime)s] %(levelname)s - %(name)s: %(message)s","%Y/%b/%d %H:%M:%S" ) )
ROOT_LOGGER.addHandler( sh )

import server

simple_server = make_server( 'localhost', 8000, server.application )	
ROOT_LOGGER.info( 'Serving on http://localhost:8000/' )
try:
	while not server.stop: simple_server.handle_request()
except KeyboardInterrupt:
	pass
server.halt()
