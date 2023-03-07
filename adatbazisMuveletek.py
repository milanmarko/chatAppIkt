import mysql.connector, datetime

class Adatbazis:
    pass
    
    def __init__(self) -> None:
        self.db = mysql.connector.connect(
            host= 'localhost',
            user= 'root',
            password= '',
            database= 'chatApp'
        
            )
        
    def getAllRooms(self):
        with self.db.cursor() as cursor:
            cursor.execute('SELECT * FROM szobak WHERE privatE = false')
            return cursor.fetchall()
    
    def createNewRoom(self, szobaNev, szobaId, privatE):
        with self.db.cursor() as cursor:
            cursor.execute(f'INSERT INTO szobak (szobaNev, szobaID, szobaResztvevok, privatE) VALUES ("{szobaNev}", "{szobaId}", 0, {privatE})')
        self.db.commit()
        print("lol")
    
    def joinRoom(self, szobaId):
        with self.db.cursor() as cursor:
            print("cc")
            cursor.execute(f"UPDATE szobak SET szobaResztvevok = szobaResztvevok + 1 WHERE szobaID = '{szobaId}'")
            self.db.commit()
            cursor.execute(f"SELECT szobaNev FROM szobak WHERE szobaID = '{szobaId}'")
            return cursor.fetchall()
        
    def leaveFromRoom(self, szobaID):
        with self.db.cursor() as cursor:
            cursor.execute(f"UPDATE szobak SET szobaResztvevok = szobaResztvevok - 1 WHERE szobaID = '{szobaID}'")
            self.db.commit()
            cursor.execute(f"DELETE FROM szobak WHERE szobaResztvevok = 0")
            self.db.commit()
    
    def isUsernameFree(self, username, mode):
        if username == "":
            return True
        with self.db.cursor(buffered=True) as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            if len(cursor.fetchall()) == 0 if not mode else 1:
                return True
            return False
    
    def register(self, email, username, password):
        with self.db.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (email, username, password) VALUES ('{email}', '{username}', '{password}')")
            self.db.commit()
            
    def login(self, username, password):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            r = cursor.fetchall()
            if len(r) == 1:
                return (True, r[0])
            return (False,)
    
    def getAccountInfo(self, username, password):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            return cursor.fetchall()
        
    def editAccountInfo(self, newEmail, newUsername, oldUsername, oldPassword, newPassword = ""):
        with self.db.cursor() as cursor:
            if newPassword != "":
                print(newPassword + 'ÁaSD')
                cursor.execute(f"UPDATE users SET email = '{newEmail}', username = '{newUsername}', password = '{newPassword}' WHERE (password = '{oldPassword}' AND username = '{oldUsername}')")
                self.db.commit()
            else:
                cursor.execute(f"UPDATE users SET email = '{newEmail}', username = '{newUsername}' WHERE (password = '{oldPassword}' AND username = '{oldUsername}')")
                self.db.commit()
        
    def isChatRoomNameFree(self, chatRoomName):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM szobak WHERE szobaNev = '{chatRoomName}'")
            if len(cursor.fetchall()) == 0:
                return True
            return False