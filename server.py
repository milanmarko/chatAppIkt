from flask import Flask, request, render_template, redirect
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
    socketio.run(app = app, host="0.0.0.0", port=5000)
    
# @app.route('/allRooms')
# def allRooms():
    
def randomString(stringLength):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def loginCheck(r):
    if r["username"] != "":
        return True
    return False

@socketio.on('connect')
def on_connect():
    emit('connectedSuccesfully')
    

    
@socketio.on('joinRoom')
def onRoomJoinRequest(_roomCode):
    roomCode = _roomCode['roomID']
    print(roomCode, _roomCode["username"])
    join_room(room = roomCode)
    roomName = db.joinRoom(roomCode)
    emit('joinedRoom', {'nev': roomName[0]})
    socketio.emit('messageReceivedByServer', {"sender": "Szerver", "message": f"{_roomCode['username']} csatlakozott!", "roomID": roomCode}, to=roomCode)

@socketio.on('messageSent')
def on_messageSent(message):
    socketio.emit('messageReceivedByServer', message, to=message['roomID'])
    
@socketio.on("leaveFromRoomSIO")
def onLeaveFromRoomSIO(data):
    leave_room(room=data["roomID"])
    
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
    loginData = request.form
    username = loginData['userName']
    password = loginData['password']
    loginTp = db.login(username, password)
    if loginTp[0]:
        return {"sikeresE": True, "data": loginTp[1]}
    return {"sikeresE": False}

@app.route('/account/getAccountInfo', methods = ["POST"])
def getAccountInfo():
    data = request.form
    userData = db.getAccountInfo(data["username"], data["password"])[0]
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
    return render_template('index2.html')

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


@app.route('/chat', methods= ["GET"])
def chatHtml():
    return render_template('chat.html')

@app.route('/rooms/createRoom', methods = ["POST"])
def createRoom():
    incomingRequest = request.form
    roomCode = randomString(16)
    if db.isChatRoomNameFree(incomingRequest["roomName"]):
        db.createNewRoom(incomingRequest['roomName'], roomCode, incomingRequest['private'])
        return {"successful": True, "roomCode": roomCode, "nameError": False}
    return {"successful": False, "roomCode": "", "nameError": True}

@app.route('/checkConnection', methods = ["POST"])
def checkConnection():
    return {"connected":True}

@app.route('/rooms/leaveRoom', methods = ["POST"])
def leaveRoom():
    incomingRequest = request.form
    db.leaveFromRoom(incomingRequest["roomID"])
    
    socketio.emit('messageReceivedByServer', {"sender": "Szerver", "message": f"{incomingRequest['username']} kilépett!", "roomID": roomCode}, to=incomingRequest["roomID"])
    return {"successful": True}

@app.route('/account', methods = ["GET"])
def accountHtml():
    try:
        if loginCheck(request.cookies):
            return render_template("account.html")
        return redirect('/login', code=302)
    except:
        return redirect('/login', code=302)

@app.route('/account/editAccount', methods = ["GET"])
def editAccountHtml():
    try:
        if loginCheck(request.cookies):
            return render_template("editAccount.html")
        return redirect('/login', code=302)
    except:
        return redirect('/login', code=302)

@app.route('/rooms/newRoom', methods = ["GET"])
def createRoomHtml():
    try:
        if loginCheck(request.cookies):
            return render_template("createRoom.html")
        return redirect('/login', code=302)
    except:
        return redirect('/login', code=302)

@app.route('/rooms/joinRoom', methods = ["GET"])
def joinRoomHtml():
    try:
        if loginCheck(request.cookies):
            return render_template("joinRoom.html")
        return redirect('/login', code=302)
    except:
        return redirect('/login', code=302)

@app.route('/database', methods = ["GET"])
def databaseHtml():
    return render_template("database.html")

@app.route('/client', methods = ["GET"])
def clientHtml():
    return render_template("client.html")

@app.route('/server', methods = ["GET"])
def serverHtml():
    return render_template("server.html")

@app.route('/userinterface', methods = ["GET"])
def userinterfaceHtml():
    return render_template("userinterface.html")

@app.route('/aboutus', methods = ["GET"])
def aboutusHtml():
    return render_template("aboutus.html")
