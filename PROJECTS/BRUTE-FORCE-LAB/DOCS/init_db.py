import sqlite3
import bcrypt

conn = sqlite3.connect('users.db')
cur = conn.cursor()

cur.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password BLOB
)
''')

username = 'admin'
password = 'Admin123!'

hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

try:
    cur.execute(
        'INSERT INTO users (username, password) VALUES (?, ?)',
        (username, hashed)
    )
except:
    pass

conn.commit()
conn.close()

print('Database initialized.')