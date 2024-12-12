import pymysql

class Database:
    def __init__(self):
        self.conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",
            database="SomalilandNID"
        )
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)

    def fetch_all_users(self):
        self.cursor.execute("SELECT * FROM users")
        return self.cursor.fetchall()

    def insert_user(self, full_name, nid_number, email, video_image):
        query = """
        INSERT INTO users (full_name, nid_number, email, video_image) 
        VALUES (%s, %s, %s, %s)
        """
        self.cursor.execute(query, (full_name, nid_number, email, video_image))
        self.conn.commit()
