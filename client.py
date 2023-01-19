from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QMainWindow, QLineEdit, QGridLayout
from PyQt5.QtCore import Qt

class LoginWindow(QWidget):
    def __init__(self):
        super(LoginWindow, self).__init__()
        
        self.layout = QGridLayout()
        self.layout.setContentsMargins(50,50,50,50)
        self.layout.setHorizontalSpacing(100)
        [self.layout.setColumnStretch(i, 1) for i in range(2)]
        [self.layout.setRowStretch(i, 1) for i in range(3)]


        
        self.felhasznalonevLabel = QLabel("Felhasználónév: ", self)
        self.felhasznalonevLabel.setFixedSize(400, 100)
        self.felhasznalonevLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.felhasznalonevLabel.font()
        self.font.setPointSize(20)
        self.felhasznalonevLabel.setFont(self.font)
        self.layout.addWidget(self.felhasznalonevLabel, 0, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)
        
        self.jelszoLabel = QLabel("Jelszó: ", self)
        self.jelszoLabel.setFixedSize(400, 100)
        self.jelszoLabel.setAlignment(Qt.AlignCenter | Qt.AlignRight)
        self.font = self.jelszoLabel.font()
        self.font.setPointSize(20)
        self.jelszoLabel.setFont(self.font)
        self.layout.addWidget(self.jelszoLabel, 1, 0, 1, 1, Qt.AlignCenter | Qt.AlignRight)

        self.felhasznalonevInput = QLineEdit()
        self.felhasznalonevInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.felhasznalonevInput.setFixedSize(300, 50)
        self.felhasznalonevInput.setFont(self.font)
        self.layout.addWidget(self.felhasznalonevInput, 0, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)

        self.jelszoInput = QLineEdit()
        self.jelszoInput.setAlignment(Qt.AlignCenter | Qt.AlignLeft)
        self.jelszoInput.setFixedSize(300, 50)
        self.jelszoInput.setFont(self.font)
        self.layout.addWidget(self.jelszoInput, 1, 1, 1, 1, Qt.AlignCenter | Qt.AlignLeft)


        self.setLayout(self.layout)

        
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(1000, 700)
        self.login = LoginWindow()
        self.setCentralWidget(self.login)
        


app = QApplication([])
# w = MainWindow()
w = MainWindow()
w.show()
app.exec()