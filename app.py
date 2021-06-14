from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_url_path='/static')
io = SocketIO(app)

users = []
messages = []

@app.route('/')
def main():
	return render_template('index.html')

@app.route('/chat')
def chat():
	return render_template('chat.html')

@io.on('connect')
def connect(socket):
	for message in messages:
		emit('message', message)
	emit('end_init', {})

@io.on('message')
def message(socket):
	messages.append(socket)
	emit('message', socket, broadcast=True)

@io.on('is_used')
def is_used(socket):
	if socket['name'] in users:
		emit('is_used', {'is_used': True})
	else:
		users.append(socket['name'])
		emit('is_used', {'is_used': False, 'name': socket['name']})


if __name__ == '__main__':
	io.run(app, debug=False)