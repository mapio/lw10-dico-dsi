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

from collections import namedtuple

import resources

GCHART_JS = 'http://www.google.com/jsapi?autoload=%7B%22modules%22%3A%5B%7B%22name%22%3A%22visualization%22%2C%22version%22%3A%221%22%2C%22packages%22%3A%5B%22linechart%22%5D%7D%5D%7D' # obtained via http://code.google.com/apis/ajax/documentation/autoloader-wizard.html
GMAP_JS = 'http://maps.google.com/maps/api/js?sensor=false'
APPLIB_JS = '/static/applib.js'
COORD_JS = '/edit/coord/load' # Questa libreria puo` essere cambiata dall'utente

Template = namedtuple( 'Template', 'title body_template js css' )

ALL = {
# system apps
	'home': Template( 'Home', 'home', None, None ),
	'upload': Template( 'Upload', 'upload', None, None ),
	'metadata': Template( 'Annota aggiungendo metadati', 'metadata', None, None ),
	'confirm': Template( 'Conferma', 'confirm', None, None ),
	'edit': Template( 'Edit', 'edit', [ '/static/codemirror/codemirror.js', '/static/edit.js' ], [ '/static/edit.css' ] ),
	'shell': Template( 'Shell', 'shell', [ '/static/shell.js' ], [ '/static/shell.css' ] ),
# user apps (examples)
	'somma': Template( 'Somma', 'io', [ APPLIB_JS, '/edit/somma/load' ], None ),
	'marker': Template( 'Marker', 'io', [ GMAP_JS, APPLIB_JS, '/edit/marker/load' ], None ),
	'mappa': Template( 'Mappa', 'map', [ GMAP_JS, APPLIB_JS, '/edit/mappa/load' ], None ),
	'chart': Template( 'Grafico', 'io', [ GCHART_JS, APPLIB_JS, '/edit/chart/load' ], None ),
	'coord': Template( 'Operazioni con le coordinate geografiche', 'io', [ '/edit/coord/load', APPLIB_JS ], None ),
	'semplice-dist': Template( 'Una semplice mappa con distanze', 'map', [ GMAP_JS, COORD_JS, APPLIB_JS, '/edit/semplice-dist/load' ], None ),
}

USER_APPS = [ 'somma', 'marker', 'mappa', 'chart', 'coord', 'semplice-dist' ]

def base_template( title, body, js = '',css = '' ):
	return base_template.t.substitute( title = title, body = body, js = js, css = css )
base_template.t = resources.load_template( 'base' )

def html( name, **kwargs ):
	t = ALL[ name ]
	j = '\n\t'.join
	js = j( '<script type="text/javascript" src="{0}"></script>'.format( _ ) for _ in t.js ) if t.js else ''
	css = j( '<link rel="stylesheet" type="text/css" href="{0}" />'.format( _ ) for _ in t.css ) if t.css else ''
	body = resources.load_template( t.body_template ).substitute( **kwargs )
	return base_template( t.title, body, js, css )
