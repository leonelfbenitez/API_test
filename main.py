# pip install flask-cors

import pymysql
from app import app
from db_config import mysql
from flask import jsonify
from flask import flash, request

#Get records from a specific table in JSON format
#http://localhost/user
@app.route('/users') #Changed the path to 'users'
def users():
    try:
        #MySQL connection
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor) #The function is actually cursor(), not cur()
        
        cur.execute("SELECT * FROM user;")
        rows = cur.fetchall()
        print("Records returned: "+str(len(rows)))

        if len(rows) > 0:
            resp = jsonify(rows)
            resp.status_code = 200
            return resp

        else:
            message = {
                'status': 404,
                'message': 'The table is empty'
            }
            resp = jsonify(message)
            resp.status_code = 404
            return resp

        cur.close() #The finally block was removed and its content was placed here
        conn.close()

    except Exception as e: #(If there is an error, it will be returned in a JSON format)
        message = {
            'status': 500,
            'message': 'Error: '+str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp

#Select a specific record from a specific table
    #The record will be obtained based on the ID specified in the URI
    #Only a single record will be returned in a JSON format
    #Error message should be displayed in a JSON format (if operation failed)
    #If record not found, a message should be returned in a JSON format

@app.route('/user/<int:id>')
def view_user(id):
    try:
        #MySQL connection
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor) #The function is actually cursor(), not cur()
        
        cur.execute("SELECT * FROM user WHERE id = %s;",id)
        rows = cur.fetchall()
        print("Records returned: "+str(len(rows)))

        if len(rows) > 0:
            resp = jsonify(rows)
            resp.status_code = 200
            return resp

        else:
            message = {
                'status': 414,
                'message': 'The user with the ID specified does NOT exist'
            }
            resp = jsonify(message)
            resp.status_code = 414
            return resp

        cur.close() #The finally block was removed and its content was placed here
        conn.close()

    except Exception as e: #(If there is an error, it will be returned in a JSON format)
        message = {
        'status': 500,
        'message': 'Error: '+str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp


#Create an user into a specific table from a database
    #Using an HTML form
    #Fields must not be empty during submission
    #A 200 status code must be returned if operation is successful (JSON format)
    #Error should be displayed in a JSON format (if operation failed)
    #There is no need to check for duplicates since the ID is generated automatically by the RDBMS
@app.route('/user/create', methods=['POST'])
def add_user():
    try:
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']

        #MySQL connection
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        if username and email and phone:

            sql = "INSERT INTO user(username, email, phone) VALUES(%s, %s, %s)"
            data = (username, email, phone)

            cur.execute(sql, data)
            conn.commit()

            message = {
                'status': 200,
                'message': 'The user was created successfully'
            }
            resp = jsonify(message)
            resp.status_code = 200
        
        else:
            message = {
                'status': 510,
                'message': 'Some of the fields are empty'
            }
            resp = jsonify(message)
            resp.status_code = 510

        cur.close() #The finally block was removed and its content was placed here
        conn.close()

        return resp
    
    except Exception as e: #(If there is an error, it will be returned in a JSON format)
        message = {
        'status': 500,
        'message': 'Error: '+str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp

#Delete a specific record from a specific table
    #Check if the user exists (if not, return an error message in a JSON format)
    #A 200 status code must be returned if operation is sucessful (JSON format)
    #Error should be displayed in a JSON format (if operation failed)
    #Parameter specificed in the URI must be valid (number)

@app.route('/user/delete/<int:id>')
def delete_user(id):
    try:
        #MySQL connection
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor) #The function is actually cursor(), not cur()
        
        cur.execute("SELECT * FROM user WHERE id = %s;",id)
        rows = cur.fetchall()
        print("Records returned: "+str(len(rows)))

        if len(rows) > 0:
            cur.execute("DELETE FROM user WHERE id = %s;",id)
            conn.commit()
            message = {
                'status': 200,
                'message': 'The user with ID '+str(id)+' was deleted successfully'
            }
            resp = jsonify(message)
            resp.status_code = 414
            return resp

        else:
            message = {
                'status': 414,
                'message': 'The user with the ID specified does NOT exist'
            }
            resp = jsonify(message)
            resp.status_code = 414
            return resp

        cur.close() #The finally block was removed and its content was placed here
        conn.close()

    except Exception as e: #(If there is an error, it will be returned in a JSON format)
        message = {
        'status': 500,
        'message': 'Error: '+str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp

#Edit an existing record, using JavaScript+AJAX
@app.route('/user/edit', methods=['POST'])
def edit_user():
    try:
        id = request.form['userId']
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']

        #MySQL connection
        conn = mysql.connect()
        cur = conn.cursor(pymysql.cursors.DictCursor)

        if username and email and phone:
            
            sql = "UPDATE user SET username = %s,email = %s,phone = %s WHERE id = %s;"
            data = (username, email, phone, id)

            cur.execute(sql, data)
            conn.commit()

            message = {
                'status': 200,
                'message': 'The user was modified successfully'
            }
            resp = jsonify(message)
            resp.status_code = 200
        
        else:
            message = {
                'status': 510,
                'message': 'Some of the fields are empty'
            }
            resp = jsonify(message)
            resp.status_code = 510

        cur.close() #The finally block was removed and its content was placed here
        conn.close()

        return resp
    
    except Exception as e: #(If there is an error, it will be returned in a JSON format)
        message = {
        'status': 500,
        'message': 'Error: '+str(e)
        }
        resp = jsonify(message)
        resp.status_code = 500
        return resp


#List records in a table using JavaScript+AJAX
#Custom search (using GET method)

@app.errorhandler(404)
def not_found(error = None):
    message = {
        'status': 404,
        'message': 'Not found: '+request.url
    }

    resp = jsonify(message)
    resp.status_code = 404

    return resp

# launch application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)

