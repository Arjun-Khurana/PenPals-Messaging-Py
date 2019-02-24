from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import json

app = Flask(__name__)
socketio = SocketIO(app)

@app.route('/')
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    #save into database!
    print('message received')

@socketio.on('my event')
def handle_my_custom_event(event, methods=['GET', 'POST']):
    print('received my event: ' + str(event))
    #call api
    URL = 'https://rocky-mesa-28651.herokuapp.com'
    msg = event['message']
    d = json.dumps({
        "language" : "es",
        "text" : msg
    })
    headers = {'Content-Type': "application/json"}
    r = requests.post(URL, headers=headers, data=d)
    msgjson = r.json()
    msgjson['user_name'] = event['user_name']
    msgjson['message'] = msgjson['translatedText']
    socketio.emit('my response', msgjson, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    