from bottle import route, run, template
import requests

@route('/temp')
def index():
    #using http://www.instructables.com/id/Temperature-Monitor-with-ESP8266-IoT/
    r = requests.get(r'https://www.ic2pro.com/Wire/connector/get?id=930d6623-21f4-4d61-affd-2f370202145d&TEMPERATURE', auth=('terryspitz@gmail.com','temperature'))
    return r.text +"C"

run(host='localhost', port=8080)