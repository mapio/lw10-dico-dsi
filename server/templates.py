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

Template = namedtuple( 'Template', 'title body_template js css' )

__SYSTEM = {
	'home': Template( 'Home', 'home', None, None ),
	'upload': Template( 'Upload', 'upload', None, None ),
	'metadata': Template( 'Annota aggiungendo metadati', 'metadata', None, None ),
	'confirm': Template( 'Conferma', 'confirm', None, None ),
	'edit': Template( 'Edit', 'edit', [ '/static/codemirror/codemirror.js', '/static/edit.js' ], [ '/static/edit.css' ] ),
	'shell': Template( 'Shell', 'shell', [ '/static/shell.js' ], [ '/static/shell.css' ] ),
}

ALL = __SYSTEM.copy()

uac = resources.load_userappsconfig()
USER_APPS = uac.get( 'User Applications', 'list' ).split()
for app in USER_APPS:
	js = uac.get( app, 'javascript' ).split() if uac.has_option( app, 'javascript' ) else []
	js.append( '/static/applib.js' )
	js.append( '/edit/{0}/load'.format( app ) )
	ALL[ app ] = Template( uac.get( app, 'title' ).encode( 'utf8' ), uac.get( app, 'template' ), js, None )

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
