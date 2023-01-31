from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QGridLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
import hashlib, requests

global usernameGlobal
usernameGlobal = ""
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
        self.font.setPointSize(15)
        self.emailFirstLabel.setFont(self.font)
        self.layout.addWidget(self.emailFirstLabel, 0, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.emailSecondLabel = QLabel("Email cím újra: ")
        self.emailSecondLabel.setFixedSize(400, 100)
        self.emailSecondLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.emailSecondLabel.font()
        self.font.setPointSize(15)
        self.emailSecondLabel.setFont(self.font)
        self.layout.addWidget(self.emailSecondLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.usernameLabel = QLabel("Felhasználónév: ")
        self.usernameLabel.setFixedSize(400, 100)
        self.usernameLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.usernameLabel.font()
        self.font.setPointSize(15)
        self.usernameLabel.setFont(self.font)
        self.layout.addWidget(self.usernameLabel, 2, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.passwordLabel = QLabel("Jelszó: ")
        self.passwordLabel.setFixedSize(400, 100)
        self.passwordLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.passwordLabel.font()
        self.font.setPointSize(15)
        self.passwordLabel.setFont(self.font)
        self.layout.addWidget(self.passwordLabel, 3, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
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
        
        self.emailTwoInput = QLineEdit()
        self.emailTwoInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.emailTwoInput.setFixedSize(300, 50)
        self.emailTwoInput.setFont(self.font)
        self.layout.addWidget(self.emailTwoInput, 1, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.usernameInput = QLineEdit()
        self.usernameInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.usernameInput.setFixedSize(300, 50)
        self.usernameInput.setFont(self.font)
        self.layout.addWidget(self.usernameInput, 2, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.passwordInput = QLineEdit()
        self.passwordInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.passwordInput.setFixedSize(300, 50)
        self.passwordInput.setFont(self.font)
        self.passwordInput.setEchoMode(QLineEdit.Password)
        self.layout.addWidget(self.passwordInput, 3, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)
        
        self.setLayout(self.layout)
        
    def register(self):
        msg = QMessageBox()
        e1 = self.emailOneInput.text()
        e2 = self.emailTwoInput.text()
        if e1 != e2:
            msg.setText("A 2 email cím nem ugyan az!")
            msg.setIcon(QMessageBox.Critical)
            msg.setWindowTitle("Felhasználó név hiba")
            msg.exec_()
            return
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        r = requests.post('http://localhost:5000/account/register', {"userEmail": e1, "userName": username, "password": password})
        r = r.json()
        # print(r)
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
        username = self.usernameInput.text()
        password = hashlib.md5(self.passwordInput.text().encode('utf-8')).hexdigest()
        r = requests.post('http://localhost:5000/account/login', {"userName": username, "password": password})
        r = r.json()
        if r["sikeresE"]:
            global usernameGlobal
            usernameGlobal = username
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
        

class AllRoom(QWidget):
    def __init__(self):
        super(AllRoom, self).__init__()
        self.setWindowTitle("Chat App")
        
        self.setFixedSize(1000,700)
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(1)]
        [self.layout.setRowStretch(i, 1) for i in range(5)]
        
    def update(self):
        r = requests.get('localhost:5000/rooms/getAll')
        self.rooms = r.json()
        





class MainWindow(QWidget):
    
    
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(1000, 700)
        self.loginw = LoginWindow()
        self.regw = RegWindow()
        self.mainw = MainMenu()
        self.allroomw = AllRoom()
        self.loginw.show()
        self.loginw.toRegButton.clicked.connect(lambda: self.openReg(self.loginw))
        self.regw.backButton.clicked.connect(lambda: self.openLogin(self.regw))
        
        self.regw.sikeresReg.connect(lambda: self.openLogin(self.regw))
        self.loginw.sikeresLogin.connect(lambda: self.openMainMenu(self.loginw))
        # self.setCentralWidget(self.loginw)
        
    def openReg(self, before):
        before.close()
        self.regw.show()
        
    def openLogin(self, before):
        before.close()
        self.loginw.show()
        
    def openMainMenu(self, before):
        before.close()
        self.mainw.updateAfterLogin()
        self.mainw.show()
        
    def openAllRoom(self, before):
        before.close()
        self.allroomw.show()
        


app = QApplication([])
# w = MainWindow()
w = MainWindow()
# w.show()
app.exec()