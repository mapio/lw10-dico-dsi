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

from ConfigParser import ConfigParser
from io import StringIO
from os.path import exists
from string import Template
from sys import argv
from xml.dom.minidom import parseString
from zipfile import ZipFile

__data = dict()

with open( argv[ 0 ], 'rb' ) as f:
	zf = ZipFile( f, 'r' )
	prefix_len = len( 'resources/' )
	for zi in zf.infolist():
		if zi.file_size and zi.filename.startswith( 'resources/' ):
			name = zi.filename[ prefix_len : ]
			data = zf.read( zi )
			__data[ name ] = Template( data ) if name.startswith( 'templates/' ) else data
	zf.close()

if exists( 'data.zip' ): 
	with open( 'data.zip', 'rb' ) as f:
		zf = ZipFile( f, 'r' )
		for zi in zf.infolist():
			if zi.file_size: __data[ zi.filename ] = zf.read( zi )
		zf.close()

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
	try:
		string = __data[ 'img/metadata.kml' ] 
	except KeyError:
		return None
	return parseString( string )

def load_appsconfig():
	cp = ConfigParser( { 'a': 'adef' } )
	cp.readfp( StringIO( __data[ 'userapps.cfg' ] ) )
	return cp

def save_metadata( string ):
	__data[ 'img/metadata.kml' ] = string

def dump():
	with open( 'data.zip', 'wb' ) as f:
		zf = ZipFile( f, 'w' )
		for arcname, bytes in __data.iteritems():
			prefix_is = arcname.startswith
			if prefix_is( 'code/' ) or prefix_is( 'img/'): zf.writestr( arcname, bytes )
		zf.close()
