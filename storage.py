import mysql.connector
import pickle
from datetime import datetime
from zoneinfo import ZoneInfo
class Store:
    def __init__(self,details):
        self.details = details
    
    def connect(self):
        return mysql.connector.connect(**self.details)
    
    def setup_database(self):
        con = self.connect()
        cursor = con.cursor()
        cursor.execute('create database if not exists storage')
        cursor.execute('use storage')
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS userdata (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255) UNIQUE,
                wins INT,
                losses INT,
                draws INT
            )
        """)
        con.commit()
        con.close()
    def store_user(self,name):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("SELECT name FROM userdata WHERE name=%s" ,(name,))
        result = cursor.fetchone()
        if result:
            con.close()
            return False
        else:
            cursor.execute("insert into userdata(name,wins,losses,draws) values(%s,%s,%s,%s)", (name,0,0,0))
            con.commit()
            con.close()
            return True

    def update_win(self,name1,name2):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("update userdata set wins = wins+1 where name = %s",(name1,))
        cursor.execute("update userdata set losses = losses+1 where name = %s",(name2,))
        con.commit()
        con.close()
        
    def update_draw(self,name1,name2):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("update userdata set draws = draws + 1 where name = %s or name =%s ",(name1,name2))
        con.commit()
        con.close()
        
    def fetchall(self):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("select name, wins, losses, draws from userdata")
        result = cursor.fetchall()
        con.close()
        return result
    
    def fetch_user(self,name):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("select name, wins, losses, draws from userdata where name = %s",(name,))
        result = cursor.fetchall()
        con.close()
        return result
    
    def delete_user(self, name):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("SELECT name FROM userdata WHERE name=%s", (name,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM userdata WHERE name=%s", (name,))
            con.commit()
            con.close()
            return True
        else:
            con.close()
            return False
    
    def update_user_stats(self, name, wins, losses, draws):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("SELECT name FROM userdata WHERE name=%s", (name,))
        result = cursor.fetchone()
        if result:
            cursor.execute("UPDATE userdata SET wins=%s, losses=%s, draws=%s WHERE name=%s", (wins, losses, draws, name))
            con.commit()
            con.close()
            return True
        else:
            con.close()
            return False

    def delete_all_users(self):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        try:
            cursor.execute("TRUNCATE TABLE userdata")
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(e)
            con.close()
            return False

    def setup_game_database(self):
        con = self.connect()
        cursor = con.cursor()
        cursor.execute('create database if not exists storage')
        cursor.execute('use storage')
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS gamedata(
                id int auto_increment primary key,
                time varchar(255) UNIQUE,
                player1 varchar(255),
                player2 varchar(255),
                gamestate BLOB
                )
        """)
        con.commit()
        con.close()
    def save_game(self,player1,player2,gamestate):
        game = pickle.dumps(gamestate)
        timezone = ZoneInfo("Asia/Kolkata")
        now = datetime.now(timezone)
        self.setup_game_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute('use storage')
        cursor.execute("insert into gamedata(time,player1,player2,gamestate) values(%s,%s,%s,%s )", (now.strftime("%d/%m/%y %H:%M"),player1,player2,game))
        con.commit()
        con.close()
    
    def get_saved_games(self):
        self.setup_game_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("USE storage")
        cursor.execute("""
            SELECT id, time, player1, player2
            FROM gamedata
            ORDER BY id ASC
        """)
        result = cursor.fetchall()
        con.close()
        return result
    def load_game(self, game_id):
        self.setup_game_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("USE storage")
        cursor.execute("SELECT gamestate FROM gamedata WHERE id=%s",(game_id,))
        result = cursor.fetchone()
        con.close()
        if result:
            return pickle.loads(result[0])
        return None
    def delete_game(self, game_id):
        self.setup_database()
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        cursor.execute("SELECT id FROM gamedata WHERE id=%s", (game_id,))
        result = cursor.fetchone()
        if result:
            cursor.execute("DELETE FROM gamedata WHERE id=%s", (game_id,))
            con.commit()
            con.close()
            return True
        else:
            con.close()
            return False
    def delete_all_games(self):
        self.setup_game_database
        con = self.connect()
        cursor = con.cursor()
        cursor.execute("use storage")
        try:
            cursor.execute("TRUNCATE TABLE gamedata")
            con.commit()
            con.close()
            return True
        except Exception as e:
            print(e)
            con.close()
            return False