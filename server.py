from flask import Flask, request, render_template
from flask_socketio import SocketIO, join_room, emit, leave_room
from adatbazisMuveletek import Adatbazis
import random, string, datetime


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
    

    
@socketio.on('joinRoom')
def onRoomJoinRequest(_roomCode):
    roomCode = _roomCode['roomID']
    join_room(room = roomCode)
    roomName = db.joinRoom(roomCode)
    emit('joinedRoom', {'nev': roomName[0]})
    
# @socketio.on('getAllRoom')
# def getAllRoom():
#     sendLista = []
#     codes = []
#     lista = db.getAllRooms()
#     for elem in lista:
#         sendLista.append(f"{elem[1]}\t\t\t{elem[3]}")
#         codes.append(elem[2])
#     print(sendLista)
#     socketio.emit('allRoom', {'list': sendLista, 'codes':codes})


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
    if db.isUsernameFree(username, False):
        db.register(email, username, password)
        return {"sikeresE": True}
    else:
        return {"sikeresE": False, "isUsernameUsed": True}
    
@app.route('/account/login', methods = ["POST"])
def login():
    print(f"Login megkezdése: {datetime.datetime.now()}")
    loginData = request.form
    username = loginData['userName']
    password = loginData['password']
    loginTp = db.login(username, password)
    print(f"Login kész: {datetime.datetime.now()}")
    if loginTp[0]:
        return {"sikeresE": True, "data": loginTp[1]}
    return {"sikeresE": False}

@app.route('/account/getAccountInfo', methods = ["POST"])
def getAccountInfo():
    data = request.form
    userData = db.getAccountInfo(data["username"], data["password"])[0]
    print(userData)
    return {"username": userData[2], "email": userData[1]}

@app.route('/rooms/getAll', methods = ["GET"])
def getAllRoom():
    roomsListToReturn = []
    rooms = db.getAllRooms()
    for room in rooms:
        # if not room[4]:
        roomsListToReturn.append((room[1], room[3], room[2]))
    
    return {"rooms": roomsListToReturn}

@app.route('/index', methods= ["GET"])
def index():
    return render_template('index.html')

@app.route('/account/editAccountInfo', methods = ["POST"])
def editAccountInfo():
    data = request.form
    if db.isUsernameFree(data["newUsername"], data["isUsernameBeingChanged"]):
        db.editAccountInfo(data["newEmail"], data['newUsername'], data["oldUsername"], data["oldPassword"], data["newPassword"])
        return {"sikeresE": True, "data": {"email": data['newEmail'], "username": data["newUsername"], "password": data['newPassword']}}
    return {"sikeresE": False, "isUsernameUsed": True}
    # try:
    #     password
    
@app.route('/login', methods= ["GET"])
def loginHtml():
    return render_template('login.html')

@app.route('/registration', methods= ["GET"])
def registrationHtml():
    return render_template('register.html')

@app.route('/rooms/createRoom', methods = ["POST"])
def createRoom():
    incomingRequest = request.form
    roomCode = randomString(16)
    if db.isChatRoomNameFree(incomingRequest["roomName"]):
        db.createNewRoom(incomingRequest['roomName'], roomCode, incomingRequest['private'])
        return {"successful": True, "roomCode": roomCode, "nameError": False}
    return {"successful": False, "roomCode": "", "nameError": True}