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

GMAP_JS = 'http://maps.google.com/maps/api/js?sensor=false'
IO_JS = '/static/io.js'
BASIC_CSS = '/static/basic.css'

Template = namedtuple( 'Template', 'title body_template js css' )

ALL = {
	'home': Template( 'Home', 'home', None, None ),
	'upload': Template( 'Upload', 'upload', None, None ),
	'metadata': Template( 'Annota aggiungendo metadati', 'metadata', None, None ),
	'confirm': Template( 'Conferma', 'confirm', None, None ),
	'edit': Template( 'Edit', 'edit', [ '/static/codemirror/codemirror.js', '/static/edit.js' ], [ BASIC_CSS ] ),
	'shell': Template( 'Shell', 'shell', [ '/static/shell.js' ], [ BASIC_CSS, '/static/shell.css' ] ),
	'somma': Template( 'Somma', 'somma', [ '/edit/somma/load' ], None ),
	'somma-io': Template( 'Somma (con libreria I/O)', 'io', [ '/edit/somma-io/load', IO_JS ], None ),
	'semplice': Template( 'Una semplice mappa', 'basicmap', [ GMAP_JS, '/edit/semplice/load' ], [ BASIC_CSS ] ),
}

APPS = [ 'somma', 'somma-io', 'semplice' ]

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
