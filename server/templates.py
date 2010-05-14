from collections import namedtuple

import resources

GMAP_JS = 'http://maps.google.com/maps/api/js?sensor=false'

Application = namedtuple( 'Application', 'title body js css' )

applications = {
	'basic': Application( 'Una sempilce mappa', 'basicmap', [ GMAP_JS, '/edit/basic/load' ], None ),
}

_base_template = reaources.load_template( 'base' )

def base_template( title, body, js = '',css = '' ):
	return _base_template.substitute( title = title, body = body, js = js, css = css )

def html( name, **kwargs ):
	app = applications[ name ]
	js = '\n'.join( '<script type="text/javascript" src="{0}"></script>'.format( _ ) for _ in app.js ) if app.js else ''
	css = '\n'.join( '<style type="text/css" src="{0}"></style>'.format( _ ) for _ in app.css ) if app.css else ''
	body = resources.load_template( app.body ).substitute( **kwargs )
	resources.base_template( app.title, body, js, css )
