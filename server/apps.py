from collections import namedtuple

import resources

GMAP_JS = 'http://maps.google.com/maps/api/js?sensor=false'
GMAP_DIV = '<div id="map_canvas" style="width:100%; height:100%"></div>'

Application = namedtuple( 'Application', 'title body css js body_attrs' )

applications = {
	'basic': Application( 'Una sempilce mappa', None, [ GMAP_JS ], GMAP_DIV, 'onload="initialize()"' ),
}

template = resources.load_template( 'base' )

def html( title, body = None, css = '', js = '', body_attr = '' ):
	if body is None:
		return template.substitute( title = title, body = body, css = css, js = js, body_attr = body_attr )
	else:
		app = applications[ title ]
		if app.css:
			css = '\n'.join( '<style type="text/css" src="{0}"></style>'.format( _ ) for _ in app.css )
		if app.js:
			js = '\n'.join( '<script type="text/javascript" src="{0}"></script>'.format( _ ) for _ in app.js )
