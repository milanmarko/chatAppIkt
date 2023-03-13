from PyQt5.QtWidgets import *
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtCore import Qt, pyqtSignal
import hashlib, requests, socketio, functools, re

# global usernameGlobal, passwordGlobal, emailGlobal
usernameGlobal = ""
passwordGlobal = ""
emailGlobal = ""
roomCode = ""
roomName = ""
serverIp = "" 
sio = socketio.Client()


def checkEmail(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if re.fullmatch(regex, email):
        return True
    return False

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
        self.font.setPointSize(20)
        self.emailFirstLabel.setFont(self.font)
        self.layout.addWidget(self.emailFirstLabel, 0, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        
        self.usernameLabel = QLabel("Felhasználónév: ")
        self.usernameLabel.setFixedSize(400, 100)
        self.usernameLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.usernameLabel.font()
        self.font.setPointSize(20)
        self.usernameLabel.setFont(self.font)
        self.layout.addWidget(self.usernameLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.passwordLabel = QLabel("Jelszó: ")
        self.passwordLabel.setFixedSize(400, 100)
        self.passwordLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordLabel.font()
        self.font.setPointSize(20)
        self.passwordLabel.setFont(self.font)
        self.layout.addWidget(self.passwordLabel, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)

        self.passwordTwoLabel = QLabel("Jelszó újra: ")
        self.passwordTwoLabel.setFixedSize(400, 100)
        self.passwordTwoLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordTwoLabel.font()
        self.font.setPointSize(20)
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
        if not checkEmail(email):
            msg.setText("Ilyen e-mail nincs!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("E-mail cím hiba")
            msg.exec_()
            return
        
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        r = requests.post(f'http://{serverIp}/account/register', {"userEmail": email, "userName": username, "password": password})
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
        

class IpSelectWindow(QWidget):
    ipSelectedIsGood = pyqtSignal()
    
    
    def __init__(self):
        super(IpSelectWindow, self).__init__()
        self.setWindowTitle("Belépés")
        
        self.setFixedSize(600,300)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(4)]

        self.title = QLabel("Ip cím választás")
        self.font_ = self.title.font()
        self.font_.setPointSize(15)
        self.title.setFont(self.font_)
        self.layout.addWidget(self.title, 0, 0, 1, 2, Qt.AlignTop | Qt.AlignHCenter)
        
        self.ipLabel = QLabel("Ip cím és portszám:")
        self.ipLabel.setFont(self.font_)
        self.layout.addWidget(self.ipLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.ipInput = QLineEdit()
        self.font_.setPointSize(12)
        self.ipInput.setFont(self.font_)
        self.ipInput.setFixedSize(200, 30)
        self.layout.addWidget(self.ipInput, 1, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.okButton = QPushButton("Tovább")
        self.okButton.setFixedSize(150, 50)
        self.okButton.clicked.connect(self.serverCheck)
        self.layout.addWidget(self.okButton, 3, 0, 1, 2, Qt.AlignCenter | Qt.AlignHCenter)
        
        self.setLayout(self.layout)

    def serverCheck(self):
        ip = self.ipInput.text()
        try:
            r = requests.post(f"http://{ip}/checkConnection")
            r = r.json()
            if r["connected"]:
                global sio
                sio.connect(f"http://{ip}")
                global serverIp
                serverIp = ip
                msg = QMessageBox()
                msg.setText("Sikeres csatlakozás!")
                msg.setWindowTitle("Csatlakozva")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                self.ipSelectedIsGood.emit()
        except:
            msg = QMessageBox()
            msg.setText("Sikertelen csatlakozás!")
            msg.setWindowTitle("Sikertelen csatlakozás")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

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
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        global passwordGlobal
        passwordGlobal = password
        r = requests.post(f'http://{serverIp}/account/login', {"userName": username, "password": password})
        r = r.json()
        
        if r["sikeresE"]:
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
        # r = requests.post(f'http://{serverIp}/account/getAccountInfo', {"username": usernameGlobal, "password": passwordGlobal})
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
        global usernameGlobal, passwordGlobal, emailGlobal
        newEmail = self.newEmailInput.text()
        if newEmail == "":
            global emailGlobal
            newEmail = emailGlobal
        elif not checkEmail(newEmail):
            msg = QMessageBox()
            msg.setText("Hibás e-mail cím!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Sikertelen változtatás")
            msg.exec_()
            return
        newUsername = self.newUsernameInput.text()
        if newUsername == "":
            global usernameGlobal
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
            r = requests.post(f'http://{serverIp}/account/editAccountInfo', {"newEmail": newEmail, "newUsername": newUsername, "oldUsername": usernameGlobal, "oldPassword": oldPassword, "newPassword": newPasswordOne, "isUsernameBeingChanged": isUsernameBeingChanged})
        else:
            r = requests.post(f'http://{serverIp}/account/editAccountInfo', {"newEmail": newEmail, "newUsername": newUsername, "oldUsername": usernameGlobal, "oldPassword": passwordGlobal, "newPassword": "", "isUsernameBeingChanged": isUsernameBeingChanged})
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
        # [self.layout.setRowStretch(i, 1) for i in range(2)]
        self.layout.setRowStretch(0, 5)
        self.layout.setRowStretch(1, 1)
        
    def update(self):
        r = requests.get(f'http://{serverIp}/rooms/getAll')
        self.rooms = r.json()["rooms"]
        
        self.roomDicts = {}        
        
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.rooms))
        self.tableWidget.setColumnCount(3)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setHorizontalHeaderLabels(['Szoba neve', 'Résztvevők száma', 'Csatlakozás'])
        self.tableWidget.setVerticalHeaderLabels([])
        
        for index, row in enumerate(self.rooms):
            self.roomDicts[row[0]] = lambda: self.connectToRoom(row[0], row[2])
            self.tableWidget.setItem(index, 0, QTableWidgetItem(row[0]))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(str(row[1])))
            self.tableWidget.setCellWidget(index, 2, QPushButton("Csatlakozás"))
            self.tableWidget.cellWidget(index, 2).clicked.connect(functools.partial(self.connectToRoom, row[0], row[2])) 
           
            
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        
        self.layout.addWidget(self.tableWidget, 0, 0)
        
        self.backButton = QPushButton("Vissza")
        self.backButton.setFixedSize(150, 50)
        self.layout.addWidget(self.backButton, 1, 0, Qt.AlignCenter | Qt.AlignHCenter)
        
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
        self.setWindowTitle(f"Chatszoba: {roomName}")
        
        self.messageHistory = QListWidget()
        
        gridChatRoom = QGridLayout()

        self.scrollRecords = QScrollArea()
        self.scrollRecords.setWidget(self.messageHistory)
        self.font_ = self.scrollRecords.font()
        self.font_.setPointSize(17)
        self.scrollRecords.setFont(self.font_)
        self.scrollRecords.setWidgetResizable(True)
        # self.sendComboBox.activated[str].connect(self.send_choice)
        self.lineEdit = QLineEdit()
        self.lineEdit.setFont(self.font_)
        self.lineEnterBtn = QPushButton("Enter")
        self.lineEnterBtn.setFixedSize(100, 50)
        # self.lineEnterBtn.clicked.connect(self.enter_line)
        # self.lineEdit.returnPressed.connect(self.enter_line)
        
        self.emojiBox = QGroupBox("Emoji")
        self.emojiBtn1 = QPushButton("ก็ʕ•͡ᴥ•ʔ ก้")
        self.emojiBtn1.clicked.connect(lambda: self.sendEmoji("ก็ʕ•͡ᴥ•ʔ ก้"))
        self.emojiBtn2 = QPushButton("(｡◕∀◕｡)")
        self.emojiBtn2.clicked.connect(lambda: self.sendEmoji("(｡◕∀◕｡)"))
        self.emojiBtn3 = QPushButton("( ˘･з･)")
        self.emojiBtn3.clicked.connect(lambda: self.sendEmoji("( ˘･з･)"))
        self.emojiBtn4 = QPushButton("ᕦ(ò_óˇ)ᕤ")
        self.emojiBtn4.clicked.connect(lambda: self.sendEmoji("ᕦ(ò_óˇ)ᕤ"))
        emojiLayout = QHBoxLayout()
        self.backButton = QPushButton("Vissza")
        self.backButton.setFixedSize(100, 50)
        emojiLayout.addWidget(self.emojiBtn1)
        emojiLayout.addWidget(self.emojiBtn2)
        emojiLayout.addWidget(self.emojiBtn3)
        emojiLayout.addWidget(self.emojiBtn4)
        self.emojiBox.setLayout(emojiLayout)
        gridChatRoom.addWidget(self.scrollRecords,0,0,2,3)
        gridChatRoom.addWidget(self.backButton,1,3, Qt.AlignCenter | Qt.AlignRight)
        gridChatRoom.addWidget(self.lineEdit,2,0,1,3)
        gridChatRoom.addWidget(self.lineEnterBtn,2,3,1,1)
        gridChatRoom.addWidget(self.emojiBox,3,0,1,4)
        gridChatRoom.setColumnStretch(0, 9)
        gridChatRoom.setColumnStretch(1, 9)
        gridChatRoom.setColumnStretch(2, 9)
        gridChatRoom.setColumnStretch(3, 1)
        gridChatRoom.setRowStretch(0, 9)
        
        self.lineEnterBtn.clicked.connect(self.sendMessage)


        self.setLayout(gridChatRoom)
    
    def sendMessage(self):
        sio.emit('messageSent', {'sender': usernameGlobal, 'roomID': roomCode, 'message': self.lineEdit.text()})
        self.lineEdit.setText("")

    def sendEmoji(self, emoji):
        sio.emit('messageSent', {'sender': usernameGlobal, 'roomID': roomCode, 'message': emoji})
    

    @sio.on('messageReceivedByServer')
    def messageReceivedByServer(message):
        
        w.chatroomw.messageHistory.addItem(f"{message['sender']}: {message['message']}")
        
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
        r = requests.post(f'http://{serverIp}/rooms/createRoom', {"roomName":name, "private": private})
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
        
        self.ipselectw = IpSelectWindow()
        self.ipselectw.show()
        self.ipselectw.ipSelectedIsGood.connect(lambda: self.openLogin(self.ipselectw))
        
        
    #     self.loginw = LoginWindow()
    #     self.loginw.show()
    #     self.loginw.toRegButton.clicked.connect(lambda: self.openReg(self.loginw))
    #     self.loginw.sikeresLogin.connect(lambda: self.openMainMenu(self.loginw))        
    #     # self.setCentralWidget(self.loginw)
    

    def sioLogin(self, ip):
        global sio
        sio.connect(ip)
        
        
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
        self.allroomw.joiningToRoom.connect(self.joiningOldRoom)
        self.allroomw.show()
        self.allroomw.backButton.clicked.connect(lambda: self.openMainMenu(self.allroomw))
        before.close()
        
    def openEditProfile(self, before):
        self.editprofilew = EditProfile()
        self.editprofilew.show()
        self.editprofilew.update()
        self.editprofilew.backButton.clicked.connect(lambda: self.openMainMenu(self.editprofilew))
        self.editprofilew.accountInfoChangeSuccesfull.connect(lambda: self.openMainMenu(self.editprofilew))
        before.close()
        
    def joiningNewRoom(self):
        sio.emit('joinRoom', {"roomID": roomCode, "username": usernameGlobal})
        sio.on('joinedRoom')
        self.openChatRoom(self.createchatroomw)

    def joiningOldRoom(self):
        sio.emit('joinRoom', {"roomID": roomCode, "username": usernameGlobal})
        sio.on('joinedRoom')
        self.openChatRoom(self.allroomw)

        
    def leaveChatRoom(self):
        msg = QMessageBox()
        choice = msg.question(self, "Kilépés", "Biztos ki szeretnél lépni?", QMessageBox.Yes | QMessageBox.No)
        if choice == QMessageBox.Yes:
            r = requests.post(f"http://{serverIp}/rooms/leaveRoom", {"roomID": roomCode, "username": usernameGlobal})
            r = r.json()
            if r["successful"]:
                self.openAllRoom(self.chatroomw)
            
        
        
    def openChatRoom(self, before):
        before.close()
        self.chatroomw = ChatRoomWindow()
        self.chatroomw.backButton.clicked.connect(self.leaveChatRoom)
        self.chatroomw.show()
        
    def openCreateChatRoom(self, before):
        before.close()
        self.createchatroomw = CreateRoomWindow()
        self.createchatroomw.roomCreated.connect(self.joiningNewRoom)
        self.createchatroomw.backButton.clicked.connect(lambda: self.openMainMenu(self.createchatroomw))
        self.createchatroomw.show()
        
    
app = QApplication([])
# w = MainWindow()
w = MainWindow()
# w.show()
app.exec()