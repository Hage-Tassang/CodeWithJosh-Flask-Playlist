import os
import logging
from datetime import datetime
from typing import Dict
import random

#chatting app server using flask framework n socketio for real-time 
#Tech stack: Python, Flask, Flask-SocketIO, html, css, js
from flask import Flask, render_template, request, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from werkzeug.middleware.proxy_fix import ProxyFix



# Setting up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',        
)
logger = logging.getLogger(__name__)


class Config:
    """Configuration class for Flask app."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'your_secret_key')
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() in ('true','1','t')
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*')


    #Chat rooms
    CHAT_ROOMS = [
                'General', 
                'Technology', 
                'Gaming',
                'Music',
                'Movies',
                'Brain Rot',
        ]

# Setting the flask app and socketio
app = Flask(__name__)
app.config.from_object(Config)

#handle reverse proxy
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

#set up socketio
socketIO = SocketIO(
    app,
    cors_alllowed_origins=app.config['CORS_ORIGINS'],
    Logger=True,
    engineio_Logger = True
)

# make a database / Dict
#chat_history: Dict[str, list] = {room: [] for room in Config.CHAT_ROOMS}
active_users: Dict[str, set] = {room: set() for room in Config.CHAT_ROOMS}

#Make a generate random user
@app.route('/generate_random_user')
def generate_random_user():
    timestamp = datetime.now().strftime('%H%M')
    return f'Guest{timestamp}{random.randint(1000,9999)}'

#Home route
@app.route('/')
def index():
    if "username" not in session:
        session['username'] = generate_random_user()
        logger.info(f"Generated random username: {session['username']}")

    return render_template(
        'index.html', 
         chat_rooms=Config.CHAT_ROOMS,
         username=session['username']
    )


#Make a connection event
@socketIO.on('connect')
def connect():
    try:
        if 'username' not in session:
            session['username'] = generate_random_user()
            
        active_users[request.sid] = {
            'username': session['username'],
            'connected_at': datetime.now().isoformat()
        }

        emit('active_users', {
            'users': [user['username'] for user in active_users.values()]
            }, broadcast=True)    
        
        logger.info(f"Generated random username at time:{datetime.now().isoformat()} with name: {session['username']}")

    except Exception as e:
        logger.error(f"Error during connection: {e}")
        return False

#Disconnect user from current session or chat

@socketIO.event('disconnect')
def Disconnect():
    try:
        if request.sid in active_users:
            username  = active_users[request.sid] ['username']  
            del active_users[request.sid]

        emit('active_users', {
            'users': [user['username'] for user in active_users.values()]
            }, broadcast=True)    
        
        logger.info(f"user disconnected at time:{datetime.now().isoformat()} with name: {username}")

    except Exception as e:
        logger.error(f"Disconnection error: {e}")
        return False



# __name__ == '__main__' means that the script is being run directly and not imported as a module
if __name__ == '__main__':
    app.run(debug=True)

