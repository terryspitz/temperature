from bottle import route, run, template, static_file
import requests
import json

@route('/temperature')
def index():
    try:
        #using http://www.instructables.com/id/Temperature-Monitor-with-ESP8266-IoT/
        SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
        config = json.load(open(os.path.join(SITE_ROOT, 'config.json')))
        url, auth_email, auth_pass = config["url"], config["user"], config["pwd"]
        r = requests.get(url, auth=(auth_email, auth_pass))
        return '<html><body><h1>'+r.text.replace(',',' at home is ') +'C</h1></body></html>'
    except Exception as e:
        return '<html><body>{0}</body></html>'.format(e)


@route('/favicon.ico')
def get_favicon():
    return static_file('favicon.ico', root='.')
	

"""
This script runs the application using a development server.
"""

import bottle
import os
import sys

# routes contains the HTTP handlers for our server and must be imported.
import routes

if '--debug' in sys.argv[1:] or 'SERVER_DEBUG' in os.environ:
    # Debug mode will enable more verbose output in the console window.
    # It must be set at the beginning of the script.
    bottle.debug(True)

def wsgi_app():
    """Returns the application to make available through wfastcgi. This is used
    when the site is published to Microsoft Azure."""
    return bottle.default_app()

if __name__ == '__main__':
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
    STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static').replace('\\', '/')
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555

    @bottle.route('/static/<filepath:path>')
    def server_static(filepath):
        """Handler for static files, used with the development server.
        When running under a production server such as IIS or Apache,
        the server should be configured to serve the static files."""
        return bottle.static_file(filepath, root=STATIC_ROOT)

    # Starts a local test server.
    bottle.run(server='wsgiref', host=HOST, port=PORT)

#note in web.config change <filter type...
#to <filter level="TraceEventType.Error" />