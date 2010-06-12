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

def _zip2data( path, read_as ):
	try:
		with open( path, 'rb' ) as f:
			zf = ZipFile( f, 'r' )
			for zi in zf.infolist():
				t = read_as( zi )
				if t: __data[ t ] = zf.read( zi )
			zf.close()
	except ( BadZipfile, IOError ):
		LOGGER.warn( 'zip2data: fail to read ' + path )

def _data2zip( path, must_write ):
	with open( path, 'wb' ) as f:
		zf = ZipFile( f, 'w' )
		for arcname, bytes in __data.iteritems():
			prefix_is = arcname.startswith
			if must_write( arcname ): zf.writestr( arcname, bytes )
		zf.close()

__data = dict()
_zip2data( argv[ 0 ], lambda zi : zi.filename[ len( 'resources/' ) : ] if zi.filename.startswith( 'resources/' ) else None )
_zip2data( 'data.zip', lambda zi : zi.filename )

def load_static( name ):
	return __data[ 'static/' + name ]

def load_template( name ):
	return __data[ 'templates/{0}.html'.format( name ) ]

def load_code( name ):
	return __data[ 'code/{0}.js'.format( name ) ]

def save_code( name, code ):
	__data[ 'code/{0}.js'.format( name ) ] = code

def load_image( num ):
	return __data[ 'img/{0:03d}.jpg'.format( num ) ]

def save_image( num, image ):
	__data[ 'img/{0:03d}.jpg'.format( num ) ] = image
	
def load_metadata():
	return __data[ 'img/metadata.kml' ] 

def load_userappsconfig():
	return __data[ 'userapps.cfg' ]

def save_metadata( string ):
	__data[ 'img/metadata.kml' ] = string

def dump():
	with open( 'data.zip', 'wb' ) as f:
		zf = ZipFile( f, 'w' )
		for arcname, bytes in __data.iteritems():
			prefix_is = arcname.startswith
			if prefix_is( 'code/' ) or prefix_is( 'img/'): zf.writestr( arcname, bytes )
		zf.close()
