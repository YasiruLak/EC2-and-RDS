from flask import Flask, request, render_template,jsonify
from flask_cors import CORS, cross_origin

import mysql.connector

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}})
#app.config['MYSQL_HOST'] = 'localhost'
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = '1234'
#app.config['MYSQL_DB'] = 'customer'
app.config['MYSQL_HOST'] = 'database-1-instance-1.cwqlykfccxgl.us-east-1.rds.amazonaws.com'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = '41RcW9yTn6DdbQZg8Kf8'
app.config['MYSQL_DB'] = 'database-1'

conn = mysql.connector.connect(
    host=app.config['MYSQL_HOST'],
    user=app.config['MYSQL_USER'],
    password=app.config['MYSQL_PASSWORD'],
    database=app.config['MYSQL_DB']
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/save', methods=['POST'])
@cross_origin()
def save_data():
    if request.method == 'POST':
        id = request.json['id']
        name = request.json['name']
        age = request.json['age']
        address = request.json['address']
        contact = request.json['contact']
        
        cursor = conn.cursor()
        cursor.execute('INSERT INTO customers (id,name,age, address, contact) VALUES (%s, %s, %s, %s, %s)', (id, name, age, address, contact))
        conn.commit()
        conn.close()
        return jsonify({'status': 200})
    
@app.route('/update', methods=['PUT'])
@cross_origin()
def update_data():
    if request.method == 'PUT':
        id = request.json['id']
        name = request.json['name']
        age = request.json['age']
        address = request.json['address']
        contact = request.json['contact']
        
        cursor = conn.cursor()
        query = 'UPDATE customers SET name=%s, age=%s, address=%s, contact=%s WHERE id=%s'
        values = (name, age, address, contact, id)
        cursor.execute(query, values)
        conn.commit()
        conn.close()
        return jsonify({'status': 200})
    
@app.route('/get', methods=['GET'])
@cross_origin()
def get_data():
    if request.method == 'GET':
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        rows = cursor.fetchall()
        conn.close()
        return jsonify({'status': 200, 'data': rows})
    
@app.route('/delete', methods=['DELETE'])
@cross_origin()
def delete_data():
    if request.method == 'DELETE':
        id = request.json.get('id')
        if id:
            cursor = conn.cursor()
            query = 'DELETE FROM customers WHERE id = %s'
            values = (id,)
            cursor.execute(query, values)
            conn.commit()
            conn.close()
            return jsonify({'status': 200, 'message': 'Successfully Deleted!'})
        else:
            return jsonify({'status': 400, 'message': 'No ID provided'})

if __name__ == '__main__':
    app.run(debug=True)

