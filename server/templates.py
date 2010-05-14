from collections import namedtuple

import resources

GMAP_JS = 'http://maps.google.com/maps/api/js?sensor=false'
BASIC_CSS = '/static/basic.css'

Template = namedtuple( 'Template', 'title body_template js css' )

__templates = {
	'upload': Template( 'Upload', 'upload', None, None ),
	'metadata': Template( 'Annota aggiungendo metadati', 'metadata', None, None ),
	'confirm': Template( 'Conferma', 'confirm', None, None ),
	'edit': Template( 'Edit', 'edit', [ '/static/codemirror/codemirror.js', '/static/edit.js' ], [ BASIC_CSS ] ),
	'basic': Template( 'Una sempilce mappa', 'basicmap', [ GMAP_JS, '/edit/basic/load' ], [ BASIC_CSS ] ),
}

__base_template = resources.load_template( 'base' )

def base_template( title, body, js = '',css = '' ):
	return __base_template.substitute( title = title, body = body, js = js, css = css )

def html( name, **kwargs ):
	t = __templates[ name ]
	j = '\n\t'.join
	js = j( '<script type="text/javascript" src="{0}"></script>'.format( _ ) for _ in t.js ) if t.js else ''
	css = j( '<link rel="stylesheet" type="text/css" href="{0}" />'.format( _ ) for _ in t.css ) if t.css else ''
	body = resources.load_template( t.body_template ).substitute( **kwargs )
	return base_template( t.title, body, js, css )
