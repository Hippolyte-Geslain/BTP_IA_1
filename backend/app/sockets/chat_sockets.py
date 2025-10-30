from flask_socketio import emit, join_room, leave_room
from flask import request
from app import socketio, db
from app.models.user import Message, User
from datetime import datetime

active_users = {}


@socketio.on('connect')
def handle_connect():
    print(f'Client connected: {request.sid}')


@socketio.on('disconnect')
def handle_disconnect():
    user_id = active_users.pop(request.sid, None)
    if user_id:
        emit('user_left', {'user_id': user_id}, broadcast=True)
        print(f'User {user_id} disconnected')


@socketio.on('join')
def handle_join(data):
    user_id = data.get('user_id')
    if user_id:
        active_users[request.sid] = user_id
        emit('user_joined', {
            'user_id': user_id,
            'active_users': list(set(active_users.values()))
        }, broadcast=True)
        print(f'User {user_id} joined chat')


@socketio.on('send_message')
def handle_message(data):
    try:
        user_id = data.get('user_id')
        content = data.get('content')
        
        # Save to database
        message = Message(
            contenu=content,
            user_id=user_id,
            timestamp=datetime.utcnow()
        )
        db.session.add(message)
        db.session.commit()
        
        # Get user info
        user = User.query.get(user_id)
        
        # Broadcast to all clients
        emit('new_message', {
            'id': message.id,
            'content': content,
            'user': user.to_dict() if user else {'nom': 'Unknown'},
            'timestamp': message.timestamp.isoformat()
        }, broadcast=True)
        
    except Exception as e:
        print(f'Error sending message: {e}')
        emit('error', {'message': str(e)})


@socketio.on('typing')
def handle_typing(data):
    user_id = data.get('user_id')
    user = User.query.get(user_id)
    if user:
        emit('user_typing', {
            'user_id': user_id,
            'user_name': user.nom
        }, broadcast=True, include_self=False)


@socketio.on('stop_typing')
def handle_stop_typing(data):
    user_id = data.get('user_id')
    emit('user_stop_typing', {'user_id': user_id}, broadcast=True, include_self=False)
