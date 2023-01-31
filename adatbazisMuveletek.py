import mysql.connector

class Adatbazis:
    
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
    
    def isUsernameFree(self, username):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")
            if len(cursor.fetchall()) == 0:
                return True
            return False
    
    def register(self, email, username, password):
        with self.db.cursor() as cursor:
            cursor.execute(f"INSERT INTO users (email, username, password) VALUES ('{email}', '{username}', '{password}')")
            self.db.commit()
            
    def login(self, username, password):
        with self.db.cursor() as cursor:
            cursor.execute(f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'")
            if len(cursor.fetchall()) == 1:
                return True
            return False