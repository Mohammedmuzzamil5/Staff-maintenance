import sqlite3

class TrainingDB:
    def __init__(self):
        self.conn = sqlite3.connect('training_requests.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS training_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                staff_name TEXT NOT NULL,
                training_type TEXT,
                status TEXT DEFAULT 'Pending'
            )
        ''')
        self.conn.commit()

    def add_training_request(self, staff_name, training_type):
        self.cursor.execute('''
            INSERT INTO training_requests (staff_name, training_type)
            VALUES (?, ?)
        ''', (staff_name, training_type))
        self.conn.commit()

    def get_all_training_requests(self):
        self.cursor.execute('SELECT * FROM training_requests')
        return self.cursor.fetchall()

    def update_request_status(self, request_id, status):
        self.cursor.execute('''
            UPDATE training_requests
            SET status = ?
            WHERE id = ?
        ''', (status, request_id))
        self.conn.commit()

    def close_connection(self):
        self.conn.close()
