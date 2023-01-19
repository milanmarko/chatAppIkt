from flask import Flask, request
from flask_socketio import SocketIO, join_room, emit, leave_room
from adatbazisMuveletek import Adatbazis
import random, string


app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

global roomCode
roomCode = ""

db = Adatbazis()

if __name__ == '__main__':
    socketio.run(app)
    
# @app.route('/allRooms')
# def allRooms():
    
def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

@socketio.on('connect')
def on_connect():
    print("connect")
    emit('connectedSuccesfully')
    
@socketio.on('requestRoom')
def roomRequested(chatSzobaRequest):
    roomCode = randomString(16)
    db.createNewRoom(chatSzobaRequest['nev'], roomCode, chatSzobaRequest['privatE'])
    emit('roomCreated', {'roomID': roomCode})
    
@socketio.on('joinRoom')
def onRoomJoinRequest(_roomCode):
    roomCode = _roomCode['roomID']
    join_room(room = roomCode)
    roomName = db.joinRoom(roomCode)
    emit('joinedRoom', {'nev': roomName[0]})
    
@socketio.on('getAllRoom')
def getAllRoom():
    sendLista = []
    codes = []
    lista = db.getAllRooms()
    for elem in lista:
        sendLista.append(f"{elem[1]}\t\t\t{elem[3]}")
        codes.append(elem[2])
    print(sendLista)
    socketio.emit('allRoom', {'list': sendLista, 'codes':codes})


@socketio.on('messageSent')
def on_messageSent(message):
    print(message['roomID'])
    socketio.emit('messageReceivedByServer', message, to=message['roomID'])
    
@app.route('/account/register', methods = ["POST"])
def register():
    registrationData = request.form
    email = registrationData['userEmail']
    username = registrationData['userName']
    password = registrationData['password']
    if db.isUsernameFree(username):
        db.register(email, username, password)
        return {"sikeresE": True}
    else:
        return {"sikeresE": False, "isUsernameUsed": True}
    
@app.route('/account/login', methods = ["POST"])
def login():
    loginData = request.form
    username = loginData['userName']
    password = loginData['password']
    if db.login(username, password):
        return {"sikeresE": True}
    return {"sikeresE": False}