from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders
                 (id TEXT, user TEXT, customer TEXT, product TEXT, status TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_order():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders VALUES (?,?,?,?,?)",
              (data['id'], data['user'], data['customer'], data['product'], data['status']))
    conn.commit()
    conn.close()
    return jsonify({"msg":"saved"})

@app.route('/get')
def get_orders():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders")
    data = c.fetchall()
    conn.close()
    return jsonify(data)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("UPDATE orders SET status=? WHERE id=?",(data['status'],data['id']))
    conn.commit()
    conn.close()
    return jsonify({"msg":"updated"})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)