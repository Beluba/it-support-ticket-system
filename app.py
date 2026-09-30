from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
DB = 'tickets.db'

def init_db():
    if not os.path.exists(DB):
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('''CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            priority TEXT,
            status TEXT,
            created_at TEXT
        )''')
        conn.commit()
        conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT * FROM tickets ORDER BY id DESC')
    tickets = c.fetchall()
    conn.close()
    return render_template('index.html', tickets=tickets)

@app.route('/create', methods=['GET','POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        priority = request.form['priority']
        status = 'Open'
        created_at = datetime.utcnow().isoformat()
        conn = sqlite3.connect(DB)
        c = conn.cursor()
        c.execute('INSERT INTO tickets (title, description, priority, status, created_at) VALUES (?,?,?,?,?)',
                  (title, description, priority, status, created_at))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

@app.route('/update/<int:id>', methods=['POST'])
def update(id):
    status = request.form['status']
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('UPDATE tickets SET status=? WHERE id=?', (status, id))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
