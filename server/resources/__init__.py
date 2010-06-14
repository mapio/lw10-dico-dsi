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

from logging import getLogger
from os.path import exists
from string import Template
from sys import argv
from zipfile import ZipFile, BadZipfile

LOGGER = getLogger( "server.resources" )

__data = dict()

def __init():
	filterzi = lambda prefix: lambda zi: zi.filename if zi.filename.startswith( prefix + '/' ) and not zi.filename.endswith( '/' ) else None
	fzi_res = filterzi( 'resources' )
	len_res = len( 'resources/' )
	def filter_res( zi ):
		name = fzi_res( zi )
		return name[ len_res: ] if name else None
	def zip( path, read_as ):
		try:
			with open( path, 'rb' ) as f:
				zf = ZipFile( f, 'r' )
				for zi in zf.infolist():
					t = read_as( zi )
					if t: 
						__data[ t ] = zf.read( zi )
				zf.close()
		except ( BadZipfile, IOError ):
			LOGGER.warn( 'Failed to read ' + path )
	zip( argv[ 0 ], filter_res )
	zip( 'code.zip', filterzi( 'code' ) )
	zip( 'data.zip', filterzi( 'data' ) )
	LOGGER.info( 'Read {0} resources'.format( len( __data.keys() ) ) )

__init()

def load_static( name ):
	return __data[ 'static/' + name ]

def load_template( name ):
	return __data[ 'templates/{0}.html'.format( name ) ]

def load_code( name ):
	return __data[ 'code/{0}.js'.format( name ) ]

def save_code( name, code ):
	__data[ 'code/{0}.js'.format( name ) ] = code

def load_image( num ):
	return __data[ 'data/{0:03d}.jpg'.format( num ) ]

def save_image( num, image ):
	__data[ 'data/{0:03d}.jpg'.format( num ) ] = image
	
def load_metadata():
	return __data[ 'data/metadata.kml' ] 

def save_metadata( string ):
	__data[ 'data/metadata.kml' ] = string

def load_appscfg():
	return __data[ 'code/apps.cfg' ]

def append_appscfg( string ):
	__data[ 'code/apps.cfg' ] += string

def dump():
	def zip( path, must_write ):
		with open( path, 'wb' ) as f:
			zf = ZipFile( f, 'w' )
			for arcname, bytes in __data.iteritems():
				prefix_is = arcname.startswith
				if must_write( arcname ): zf.writestr( arcname, bytes )
			zf.close()
	zip( 'data.zip', lambda f : f.startswith( 'data/' ) )
	zip( 'code.zip', lambda f : f.startswith( 'code/' ) )
