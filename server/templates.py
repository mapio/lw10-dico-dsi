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

from collections import namedtuple
from ConfigParser import ConfigParser
from io import StringIO
from string import Template

import resources

AppTemplate = namedtuple( 'Template', 'title body_template js css' )

__SYSTEM = {
	'home': AppTemplate( 'Home', 'home', None, None ),
	'upload': AppTemplate( 'Upload', 'upload', None, None ),
	'metadata': AppTemplate( 'Annota aggiungendo metadati', 'metadata', None, None ),
	'confirm': AppTemplate( 'Conferma', 'confirm', None, None ),
	'edit': AppTemplate( 'Edit', 'edit', [ '/static/codemirror/codemirror.js', '/static/edit.js' ], [ '/static/edit.css' ] ),
	'shell': AppTemplate( 'Shell', 'shell', [ '/static/shell.js' ], [ '/static/shell.css' ] ),
}

ALL = __SYSTEM.copy()

uac = ConfigParser( { 
	'GMAP_JS': 'http://maps.google.com/maps/api/js?sensor=false',
	'GCHART_JS': 'http://www.google.com/jsapi?autoload=%7B%22modules%22%3A%5B%7B%22name%22%3A%22visualization%22%2C%22version%22%3A%221%22%2C%22packages%22%3A%5B%22linechart%22%5D%7D%5D%7D', # obtained via http://code.google.com/apis/ajax/documentation/autoloader-wizard.html
} )
uac.readfp( StringIO( resources.load_userappsconfig().decode( 'utf8' ) ) )

USER_APPS = uac.sections()
for app in USER_APPS:
	js = uac.get( app, 'javascript' ).split() if uac.has_option( app, 'javascript' ) else []
	js.append( '/static/applib.js' )
	js.append( '/static/fvlogger/logger.js' )
	js.append( '/edit/{0}/load'.format( app ) )
	ALL[ app ] = AppTemplate( uac.get( app, 'title' ).encode( 'utf8' ), uac.get( app, 'template' ), js, [ '/static/fvlogger/logger.css' ] )

def base_template( title, body, js = '',css = '' ):
	return base_template.t.substitute( title = title, body = body, js = js, css = css )
base_template.t = Template( resources.load_template( 'base' ) )

def html( name, **kwargs ):
	t = ALL[ name ]
	try:
		j = '\n\t'.join
		js = j( '<script type="text/javascript" src="{0}"></script>'.format( _ ) for _ in t.js ) if t.js else ''
		css = j( '<link rel="stylesheet" type="text/css" href="{0}" />'.format( _ ) for _ in t.css ) if t.css else ''
		body = Template( resources.load_template( t.body_template ) ).substitute( **kwargs )
	except KeyError:
		raise RuntimeError # the caller intercepts KeyError as a signe that no app is configured, so we swallow other similar execptions and rerise a different one
	return base_template( t.title, body, js, css )
