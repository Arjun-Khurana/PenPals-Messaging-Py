from flask import Flask, render_template
from flask_socketio import SocketIO
import requests
import json
from flask_cors import CORS

app = Flask(__name__)
socketio = SocketIO(app)
#CORS(app)

@app.route('/', methods=['GET', 'POST'])
def sessions():
    return render_template('session.html')

def messageReceived(methods=['GET', 'POST']):
    #save into database!
    print('message received')

@socketio.on('scooby')
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
    socketio.emit('shaggy', msgjson, callback=messageReceived)

if __name__ == '__main__':
    socketio.run(app, debug=True)
    