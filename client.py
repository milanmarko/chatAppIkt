from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QGridLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QHeaderView, QScrollArea, QCheckBox
from PyQt5.QtCore import Qt, pyqtSignal
import hashlib, requests, datetime, socketio

# global usernameGlobal, passwordGlobal, emailGlobal
usernameGlobal = ""
passwordGlobal = ""
emailGlobal = ""
roomCode = ""
roomName = ""

sio = socketio.Client()
sio.connect('http://127.0.0.1:5000')

class RegWindow(QWidget):
    sikeresReg = pyqtSignal()
    
    def __init__(self):
        super(RegWindow, self).__init__()
        
        self.setWindowTitle("Regisztráció")
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(75)
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(5)]
        
        self.emailFirstLabel = QLabel("Email cím: ")
        self.emailFirstLabel.setFixedSize(400, 100)
        self.emailFirstLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.emailFirstLabel.font()
        self.font.setPointSize(25)
        self.emailFirstLabel.setFont(self.font)
        self.layout.addWidget(self.emailFirstLabel, 0, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        
        self.usernameLabel = QLabel("Felhasználónév: ")
        self.usernameLabel.setFixedSize(400, 100)
        self.usernameLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.usernameLabel.font()
        self.font.setPointSize(25)
        self.usernameLabel.setFont(self.font)
        self.layout.addWidget(self.usernameLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.passwordLabel = QLabel("Jelszó: ")
        self.passwordLabel.setFixedSize(400, 100)
        self.passwordLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordLabel.font()
        self.font.setPointSize(25)
        self.passwordLabel.setFont(self.font)
        self.layout.addWidget(self.passwordLabel, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)

        self.passwordTwoLabel = QLabel("Jelszó újra: ")
        self.passwordTwoLabel.setFixedSize(400, 100)
        self.passwordTwoLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordTwoLabel.font()
        self.font.setPointSize(25)
        self.passwordTwoLabel.setFont(self.font)
        self.layout.addWidget(self.passwordTwoLabel, 3, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.backButton = QPushButton("Vissza")
        self.backButton.setFixedSize(300, 100)
        self.backButton.setFont(self.font)
        self.layout.addWidget(self.backButton, 4, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
                
        self.regButton = QPushButton("Regisztráció")
        self.regButton.setFixedSize(300, 100)
        self.regButton.setFont(self.font)
        self.regButton.clicked.connect(self.register)
        self.layout.addWidget(self.regButton, 4, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.emailOneInput = QLineEdit()
        self.emailOneInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.emailOneInput.setFixedSize(300, 50)
        self.emailOneInput.setFont(self.font)
        self.layout.addWidget(self.emailOneInput, 0, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        
        self.usernameInput = QLineEdit()
        self.usernameInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.usernameInput.setFixedSize(300, 50)
        self.usernameInput.setFont(self.font)
        self.layout.addWidget(self.usernameInput, 1, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.passwordInput = QLineEdit()
        self.passwordInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.passwordInput.setFixedSize(300, 50)
        self.passwordInput.setFont(self.font)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passwordInput, 2, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.passwordTwoInput = QLineEdit()
        self.passwordTwoInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.passwordTwoInput.setFixedSize(300, 50)
        self.passwordTwoInput.setFont(self.font)
        self.passwordTwoInput.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passwordTwoInput, 3, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.setLayout(self.layout)
        
    def register(self):
        msg = QMessageBox()
        p1 = self.passwordInput.text()
        p2 = self.passwordTwoInput.text()
        if p1 != p2:
            msg.setText("A 2 jelszó nem ugyan az!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Felhasználó név hiba")
            msg.exec_()
            return
        email = self.emailOneInput.text()
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        r = requests.post('http://localhost:5000/account/register', {"userEmail": email, "userName": username, "password": password})
        r = r.json()
        if not r["sikeresE"] :
            if r["isUsernameUsed"]:
                msg.setWindowTitle("Használt felhasználónév!")
                msg.setIcon(QMessageBox.Critical)
                msg.setText("Ez a felhasználónév már használt!")
                msg.exec_()
        else:
            msg.setWindowTitle("Sikeres regisztráció!")
            msg.setIcon(QMessageBox.Information)
            msg.setText("Sikeres regisztráció!")
            msg.exec_()
            self.sikeresReg.emit()
        
    
class LoginWindow(QWidget):
    
    sikeresLogin = pyqtSignal()
    
    def __init__(self):
        super(LoginWindow, self).__init__()
        
        self.setWindowTitle("Belépés")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(3)]


        
        self.usernameLabel = QLabel("Felhasználónév: ", self)
        self.usernameLabel.setFixedSize(400, 100)
        self.usernameLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.usernameLabel.font()
        self.font.setPointSize(20)
        self.usernameLabel.setFont(self.font)
        self.layout.addWidget(self.usernameLabel, 0, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.passwordLabel = QLabel("Jelszó: ", self)
        self.passwordLabel.setFixedSize(400, 100)
        self.passwordLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordLabel.font()
        self.font.setPointSize(20)
        self.passwordLabel.setFont(self.font)
        self.layout.addWidget(self.passwordLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)

        self.usernameInput = QLineEdit()
        self.usernameInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.usernameInput.setFixedSize(300, 50)
        self.usernameInput.setFont(self.font)
        self.layout.addWidget(self.usernameInput, 0, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)

        self.passwordInput = QLineEdit()
        self.passwordInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.passwordInput.setFixedSize(300, 50)
        self.passwordInput.setFont(self.font)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passwordInput, 1, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.toRegButton = QPushButton("Regisztráció")
        self.toRegButton.setFixedSize(300, 100)
        self.toRegButton.setFont(self.font)
        self.layout.addWidget(self.toRegButton, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)


        self.loginButton = QPushButton("Belépés")
        self.loginButton.setFixedSize(300, 100)
        self.loginButton.setFont(self.font)
        self.layout.addWidget(self.loginButton, 2, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        self.loginButton.clicked.connect(self.login)


        self.setLayout(self.layout)
    
    def login(self):
        print(f"Login elkezédése: {datetime.datetime.now()}")
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        global passwordGlobal
        passwordGlobal = password
        print(f"Login Api request küldve: {datetime.datetime.now()}")
        r = requests.post('http://localhost:5000/account/login', {"userName": username, "password": password})
        r = r.json()
        print(f"Login Api request megkapva: {datetime.datetime.now()}")
        
        if r["sikeresE"]:
            print("nyom")
            global usernameGlobal
            usernameGlobal = username
            global emailGlobal
            emailGlobal = r["data"][1]
            self.sikeresLogin.emit()
        else:
            msg = QMessageBox()
            msg.setText("Hibás felhasználónév és/vagy jelszó!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Sikertelen bejelentkezés")
            msg.exec_()
        print(f"Login kész: {datetime.datetime.now()}")
        
            

class MainMenu(QWidget):
    def __init__(self):
        super(MainMenu, self).__init__()
        
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(1)]
        [self.layout.setRowStretch(i, 1) for i in range(5)]

        
        
        
    def updateAfterLogin(self):
        global usernameGlobal
        self.usernameLabel = QLabel(f"Bejelentkezve mint: {usernameGlobal}")
        self.font_ = self.usernameLabel.font()
        self.font_.setPointSize(20)
        self.usernameLabel.setFont(self.font_)
        self.layout.addWidget(self.usernameLabel, 0, 0, Qt.AlignTop | Qt.AlignHCenter)
        
        self.createNewRoomButton = QPushButton("Új szoba létrehozása")
        self.createNewRoomButton.setFixedSize(300, 75)
        self.createNewRoomButton.setFont(self.font_)
        self.layout.addWidget(self.createNewRoomButton, 1, 0, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.joinToRoomButton = QPushButton("Belépés chatszobába")
        self.joinToRoomButton.setFixedSize(300, 75)
        self.joinToRoomButton.setFont(self.font_)
        self.layout.addWidget(self.joinToRoomButton, 2, 0, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.editProfileButton = QPushButton("Profil módosítása")
        self.editProfileButton.setFixedSize(300, 75)
        self.editProfileButton.setFont(self.font_)
        self.layout.addWidget(self.editProfileButton, 3, 0, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.logOutButton = QPushButton("Kijelentkezés")
        self.logOutButton.setFixedSize(300, 75)
        self.logOutButton.setFont(self.font_)
        self.layout.addWidget(self.logOutButton, 4, 0, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.setLayout(self.layout)
        

class EditProfile(QWidget):
    
    accountInfoChangeSuccesfull = pyqtSignal()
    
    def __init__(self):
        super(EditProfile, self).__init__()
        
        
        self.isPasswordBeingEdited = False
        
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(6)]

    
    def update(self):
        # r = requests.post('http://localhost:5000/account/getAccountInfo', {"username": usernameGlobal, "password": passwordGlobal})
        # r = r.json()
        self.emailLabel = QLabel("Email cím:")
        self.font_ = self.emailLabel.font()
        self.font_.setPointSize(20)
        self.emailLabel.setFont(self.font_)
        self.layout.addWidget(self.emailLabel, 0, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.usernameLabel = QLabel("Felhasználónév:")
        self.usernameLabel.setFont(self.font_)
        self.layout.addWidget(self.usernameLabel, 1, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.oldPassword = QLabel("Régi jelszó:")
        self.oldPassword.setFont(self.font_)
        self.layout.addWidget(self.oldPassword, 2, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.newEmailInput = QLineEdit()
        self.newEmailInput.setFont(self.font_)
        global emailGlobal
        self.newEmailInput.setPlaceholderText(emailGlobal)
        self.layout.addWidget(self.newEmailInput, 0, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.newUsernameInput = QLineEdit()
        self.newUsernameInput.setFont(self.font_)
        global usernameGlobal
        self.newUsernameInput.setPlaceholderText(usernameGlobal)
        self.layout.addWidget(self.newUsernameInput, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.oldPasswordInput = QLineEdit()
        self.oldPasswordInput.setFont(self.font_)
        self.oldPasswordInput.setEchoMode(QLineEdit.Password)
        self.oldPasswordInput.textEdited.connect(self.editPassword)
        self.layout.addWidget(self.oldPasswordInput, 2, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.changeButton = QPushButton("Változtatás")
        self.changeButton.setFixedSize(300, 100)
        self.changeButton.setFont(self.font_)
        self.layout.addWidget(self.changeButton, 5, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.changeButton.clicked.connect(self.changeAccountInfo)

        self.backButton = QPushButton("Vissza")
        self.backButton.setFixedSize(300, 100)
        self.backButton.setFont(self.font_)
        self.layout.addWidget(self.backButton, 5, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.setLayout(self.layout)
        
    def editPassword(self):
        
        if not self.isPasswordBeingEdited:
            
            self.newPasswordOneLabel = QLabel("Új jelszó:")
            self.newPasswordOneLabel.setFont(self.font_)
            self.layout.addWidget(self.newPasswordOneLabel, 3, 0, Qt.AlignCenter | Qt.AlignRight)

            self.newPasswordTwoLabel = QLabel("Új jelszó másodszor:")
            self.newPasswordTwoLabel.setFont(self.font_)
            self.layout.addWidget(self.newPasswordTwoLabel, 4, 0, Qt.AlignCenter | Qt.AlignRight)
            
            self.newPasswordOneInput = QLineEdit()
            self.newPasswordOneInput.setFont(self.font_)
            self.newPasswordOneInput.setEchoMode(QLineEdit.Password)
            self.newPasswordOneInput.textEdited.connect(self.editPassword)
            self.layout.addWidget(self.newPasswordOneInput, 3, 1, Qt.AlignCenter | Qt.AlignLeft)
            
            self.newPasswordTwoInput = QLineEdit()
            self.newPasswordTwoInput.setFont(self.font_)
            self.newPasswordTwoInput.setEchoMode(QLineEdit.Password)
            self.newPasswordTwoInput.textEdited.connect(self.editPassword)
            self.layout.addWidget(self.newPasswordTwoInput, 4, 1, Qt.AlignCenter | Qt.AlignLeft)
            
            self.setLayout(self.layout)
            self.isPasswordBeingEdited = True


        if self.oldPasswordInput.text() == "":
            
            self.newPasswordOneLabel.hide()
            self.newPasswordTwoLabel.hide()
            self.newPasswordOneInput.hide()
            self.newPasswordTwoInput.hide()
                       
            self.newPasswordOneLabel = None
            self.newPasswordTwoLabel = None
            self.newPasswordOneInput = None
            self.newPasswordTwoInput = None
            self.isPasswordBeingEdited = False
            
    def changeAccountInfo(self):
        isUsernameBeingChanged = True
        global usernameGlobal
        newEmail = self.newEmailInput.text()
        if newEmail == "":
            global emailGlobal
            newEmail = emailGlobal
        newUsername = self.newUsernameInput.text()
        if newUsername == "":
            global usernameGlobal
            print(newUsername )
            newUsername = usernameGlobal
            isUsernameBeingChanged = False
        if self.isPasswordBeingEdited:
            oldPassword = hashlib.md5(self.oldPasswordInput.text().encode('utf-8')).hexdigest()
            newPasswordOne = hashlib.md5(self.newPasswordOneInput.text().encode('utf-8')).hexdigest()
            newPasswordTwo = hashlib.md5(self.newPasswordTwoInput.text().encode('utf-8')).hexdigest()
            if newPasswordOne != newPasswordTwo:
                msg = QMessageBox()
                msg.setText("A 2 jelszó nem ugyan az!")
                msg.setIcon(QMessageBox.Critical)
                msg.setWindowTitle("Sikertelen jelszóváltoztatás")
                msg.exec_()
                return
            r = requests.post('http://localhost:5000/account/editAccountInfo', {"newEmail": newEmail, "newUsername": newUsername, "oldUsername": usernameGlobal, "oldPassword": oldPassword, "newPassword": newPasswordOne, "isUsernameBeingChanged": isUsernameBeingChanged})
        else:
            r = requests.post('http://localhost:5000/account/editAccountInfo', {"newEmail": newEmail, "newUsername": newUsername, "oldUsername": usernameGlobal, "oldPassword": passwordGlobal, "newPassword": "", "isUsernameBeingChanged": isUsernameBeingChanged})
        r = r.json()
        
        if r["sikeresE"]:
            msg = QMessageBox()
            msg.setText("Sikeres változtatás!")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Sikeres változtatás")
            msg.exec_()
            # global emailGlobal
            # global usernameGlobal
            # global passwordGlobal
            emailGlobal = r["data"]["email"]
            usernameGlobal = r["data"]["username"]
            passwordGlobal = r["data"]["password"]
            self.accountInfoChangeSuccesfull.emit()
            
        elif r["isUsernameUsed"]:
            msg = QMessageBox()
            msg.setText("Használt felhasználónév!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Sikertelen felhasználónév változtatás")
            msg.exec_()
            

            
                

class AllRoom(QWidget):
    joiningToRoom = pyqtSignal()
    
    def __init__(self):
        super(AllRoom, self).__init__()
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(1)]
        [self.layout.setRowStretch(i, 1) for i in range(1)]
        
    def update(self):
        r = requests.get('http://localhost:5000/rooms/getAll')
        self.rooms = r.json()["rooms"]
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.rooms))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(['Szoba neve', 'Résztvevők száma', 'Csatlakozás'])
        self.tableWidget.setVerticalHeaderLabels([])
        
        for index, row in enumerate(self.rooms):
            self.tableWidget.setItem(index, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget.setCellWidget(index, 2, QPushButton("Csatlakozás"))
            self.tableWidget.cellWidget(index, 2).clicked.connect(lambda: self.connectToRoom(row[0], row[2]))    
            
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.layout.addWidget(self.tableWidget, 0, 0)
        self.setLayout(self.layout)

    def connectToRoom(self, roomName_, roomCode_):
        global roomName
        roomName = roomName_
        global roomCode
        roomCode = roomCode_
        self.joiningToRoom.emit()
        
        
class ChatRoomWindow(QWidget):
    
    def __init__(self):
        super(ChatRoomWindow, self).__init__()
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        # [self.layout.setColumnStretch(i, 2) for i in range(1)]
        self.layout.setColumnStretch(0, 3)
        self.layout.setColumnStretch(1, 1)
        # [self.layout.setRowStretch(i, 2) for i in range(1)]
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 3)
        self.layout.setRowStretch(2, 1)
        
        self.title = QLabel(f"Chatszoba: {roomName}")
        self.font_ = self.title.font()
        self.font_.setPointSize(20)
        self.title.setFont(self.font_)
        self.layout.addWidget(self.title, 0, 1, 1, 2, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.chatView = QScrollArea()
        self.layout.addWidget(self.chatView, 1, 0, 1, 2, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.chatInput = QLineEdit()
        self.layout.addWidget(self.chatInput, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.chatButton = QPushButton("Küldés")
        self.layout.addWidget(self.chatButton, 2, 1, 1, 1, Qt.AlignCenter | Qt.AlignHCenter)
        
        # self.asd = QLabel("LAS")
        # self.layout.addWidget(self.asd, 0, 0)
        
        self.setLayout(self.layout)
        
class CreateRoomWindow(QWidget):
    roomCreated = pyqtSignal()
    
    def __init__(self):
        super(CreateRoomWindow, self).__init__()
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(4)]
        
        self.createChatRoomLabel = QLabel("Chatszoba létrehozása")
        self.font_ = self.createChatRoomLabel.font()
        self.font_.setPointSize(25)
        self.createChatRoomLabel.setFont(self.font_)
        self.layout.addWidget(self.createChatRoomLabel, 0, 0, 1, 2, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.chatRoomNameLabel = QLabel("Chatszoba neve:")
        self.font_.setPointSize(20)
        self.chatRoomNameLabel.setFont(self.font_)
        self.layout.addWidget(self.chatRoomNameLabel, 1, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.chatRoomVisibilityLabel = QLabel("Privát-e:")
        self.chatRoomVisibilityLabel.setFont(self.font_)
        self.layout.addWidget(self.chatRoomVisibilityLabel, 2, 0, Qt.AlignCenter | Qt.AlignRight)
        
        self.createRoomButton = QPushButton("Létrehozás")
        self.createRoomButton.setFixedSize(200, 67)
        self.createRoomButton.setFont(self.font_)
        self.createRoomButton.clicked.connect(self.createRoom)
        self.layout.addWidget(self.createRoomButton, 3, 1, Qt.AlignCenter | Qt.AlignLeft)
        

        self.backButton = QPushButton("Vissza")
        self.backButton.setFixedSize(200, 67)
        self.backButton.setFont(self.font_)
        self.layout.addWidget(self.backButton, 3, 0, Qt.AlignCenter | Qt.AlignRight)
        
        
        self.chatRoomNameInput = QLineEdit()
        self.chatRoomNameInput.setFont(self.font_)
        self.layout.addWidget(self.chatRoomNameInput, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.privateCheckBox = QCheckBox()
        self.privateCheckBox.setStyleSheet("QCheckBox { font-size: 50px; }")
        self.layout.addWidget(self.privateCheckBox, 2, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        
        self.setLayout(self.layout)
        
    def createRoom(self):
        name = self.chatRoomNameInput.text()
        private = self.privateCheckBox.isChecked()
        r = requests.post('http://localhost:5000/rooms/createRoom', {"roomName":name, "private": private})
        r = r.json()
        if r["successful"]:
            global roomCode
            roomCode = r["roomCode"]
            self.roomCreated.emit()
            msg = QMessageBox()
            msg.setText("Sikeresen létrehozva!")
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Szoba sikeresen létrehozva")
            msg.exec_()
        elif r["nameError"]:
            msg = QMessageBox()
            msg.setText("Már van ilyen nevű szoba!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Szoba név hiba")
            msg.exec_()

class MainWindow(QWidget):
    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(1000, 700)
        self.loginw = LoginWindow()
        self.loginw.show()
        self.loginw.toRegButton.clicked.connect(lambda: self.openReg(self.loginw))
        self.loginw.sikeresLogin.connect(lambda: self.openMainMenu(self.loginw))        
        # self.setCentralWidget(self.loginw)
        
    def openReg(self, before):
        before.close()
        self.regw = RegWindow()
        self.regw.backButton.clicked.connect(lambda: self.openLogin(self.regw))
        self.regw.sikeresReg.connect(lambda: self.openLogin(self.regw))
        self.regw.show()
        
    def openLogin(self, before):
        before.close()
        self.loginw = LoginWindow()
        self.loginw.toRegButton.clicked.connect(lambda: self.openReg(self.loginw))
        self.loginw.sikeresLogin.connect(lambda: self.openMainMenu(self.loginw))  
        global usernameGlobal      
        usernameGlobal = ""
        self.loginw.show()
        
    def openMainMenu(self, before):
        before.close()
        self.mainw = MainMenu()
        self.mainw.updateAfterLogin()
        self.mainw.logOutButton.clicked.connect(lambda: self.openLogin(self.mainw))
        self.mainw.editProfileButton.clicked.connect(lambda: self.openEditProfile(self.mainw))
        self.mainw.joinToRoomButton.clicked.connect(lambda: self.openAllRoom(self.mainw))
        self.mainw.createNewRoomButton.clicked.connect(lambda: self.openCreateChatRoom(self.mainw))
        self.mainw.show()
        
    def openAllRoom(self, before):
        self.allroomw = AllRoom()
        self.allroomw.update()
        self.allroomw.joiningToRoom.connect(self.joiningRoom)
        self.allroomw.show()
        before.close()
        
    def openEditProfile(self, before):
        self.editprofilew = EditProfile()
        self.editprofilew.show()
        self.editprofilew.update()
        self.editprofilew.backButton.clicked.connect(lambda: self.openMainMenu(self.editprofilew))
        self.editprofilew.accountInfoChangeSuccesfull.connect(lambda: self.openMainMenu(self.editprofilew))
        before.close()
        
    def joiningRoom(self):
        sio.emit('joinRoom', {"roomID": roomCode})
        sio.on('joinedRoom')
        try:
            self.openChatRoom(self.createchatroomw)
        except:
            pass
        try:
            self.openChatRoom(self.allroomw)
        except:
            pass
        # self.chatroomw = ChatRoomWindow()
        # self.chatroomw.show()
        
    def openChatRoom(self, before):
        before.close()
        self.chatroomw = ChatRoomWindow()
        self.chatroomw.show()
        
    def openCreateChatRoom(self, before):
        before.close()
        self.createchatroomw = CreateRoomWindow()
        self.createchatroomw.roomCreated.connect(self.joiningRoom)
        self.createchatroomw.show()
        
    
app = QApplication([])
# w = MainWindow()
w = MainWindow()
# w.show()
app.exec()