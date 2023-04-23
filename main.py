# pip install flask
# pip install jsonify
# pip install flask-restful
# pip install flask-cors

from flask import flash, request, jsonify
import sqlite3
from db import conn # it forces the database to be created, if it doesn't exist
from app import app # it starts the flask api sharing process

# route to provide all records/info for all books in the inventory 
@app.route('/inventory')
def inventory():
    try:
        # open connection to database
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # retrieve all records from inventory table
        cur.execute("SELECT * FROM inventory;")
        rows = cur.fetchall()
        
        # close connection to database
        cur.close()
        conn.close()

        # if rows/results are found:
        if len(rows) > 0:
            resp = jsonify(rows) # jsonify results for delivery
            resp.status_code = 200 # tag response as code 200/OK
            return resp # return response/results

        # else, no records found:
        else:
            # create error message for delivery
            message = {
                'status': 402,
                'message': 'No records found!'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 402 # tag response with error code
            return resp # return response/error
    
    # any other errors/exceptions will ba catched here:
    except Exception as e:

	    # create error message for delivery:
        message = {
            'status': 500,
            'message': 'Error: ' + str(e)
        }
        resp = jsonify(message) # jsonify response/message for delivery
        resp.status_code = 500 # tage response/message with error code
        return resp # return response
        
# route to create record in inventory
@app.route('/inventory/create', methods=['POST'])
def add_book():
    try:
        # retrieve data/info from frontend/client
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']

        # open connection to database
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # if required fields are not empty:
        if name and category and price and stock:
            
            # insert data/info into inventory table

            cur.execute("INSERT INTO inventory(name, description, category, price, stock) VALUES(?, ?, ?, ?, ?);", 
                        (name, description, category, price, stock))

            # changes are commited and connection to database closed
            conn.commit()
            cur.close() 
            conn.close()

            # create success response message
            message = {
                'status': 200,
                'message': 'The user was created successfully'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 200 # tag response with code 200/OK
        
        # else required fields are empty:
        else:
            # create error message
            message = {
                'status': 510,
                'message': 'Some of the fields are empty'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 510 # tag response with error code
        
        return resp # return appropriate response
    
    # any other errors/exceptions will ba catched here:
    except Exception as e:
        # close connection to database in case it doesn't close properly
        cur.close()
        conn.close()

	    # create error message for delivery:
        message = {
            'status': 500,
            'message': 'Error: ' + str(e)
        }
        resp = jsonify(message) # jsonify response/message for delivery
        resp.status_code = 500 # tage response/message with error code
        return resp # return response  

# route to delete record from the inventory table with provided id
@app.route('/inventory/delete/<int:id>')
def delete_book(id):
    try:
        # open connection to database
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()
        
        # retrieve data from record to be retrieved
        cur.execute("SELECT * FROM inventory WHERE bookId = ?;", (id, ))
        rows = cur.fetchall()

        # if record is found:
        if len(rows) > 0:
            # retrieve record from table
            cur.execute("DELETE FROM inventory WHERE bookId = ?;", (id, ))

            # changes are commited and connection to database closed
            conn.commit()
            cur.close() 
            conn.close()

            # create success message
            message = {
                'status': 200,
                'message': 'The user with ID ' + str(id) + ' was deleted successfully'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 200 # tag response with error code
            return resp # return response

        # else record not found:
        else:
            # close connection to the database
            cur.close() 
            conn.close()
            # create error message
            message = {
                'status': 414,
                'message': 'The user with the ID specified does NOT exist'
            }
            resp = jsonify(message) # jsonify response for delivery
            resp.status_code = 414 # tag response with error code
            return resp # return response

    # any other errors/exceptions will ba catched here:
    except Exception as e:
        # close connection to database in case it doesn't close properly
        cur.close()
        conn.close()

	    # create error message for delivery:
        message = {
            'status': 500,
            'message': 'Error: ' + str(e)
        }
        resp = jsonify(message) # jsonify response/message for delivery
        resp.status_code = 500 # tage response/message with error code
        return resp # return response


# route to edit a record from the inventory table
@app.route('/inventory/edit', methods=['POST'])
def edit_user():
    try:
        bookId = request.form['bookId']
        name = request.form['name']
        description = request.form['description']
        category = request.form['category']
        price = request.form['price']
        stock = request.form['stock']

        # open connection to database
        conn = sqlite3.connect("database.db")
        cur = conn.cursor()

        # if required fields are not empty:
        if bookId and name and category and price and stock:
            
            # edit the record with given data 
            cur.execute("UPDATE inventory SET name = ?, description = ?, category = ?, price = ?, stock = ? WHERE bookId = ?;", 
                        (bookId, name, description, category, price, stock))
            
            # changes are commited and connection to database closed
            conn.commit()
            cur.close() 
            conn.close()

            # create success message
            message = {
                'status': 200,
                'message': 'The user was modified successfully'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 200 # tag response with error code
            return resp # return response
        
        # if required fields are empty:
        else:
            # close connection to the database
            cur.close() 
            conn.close()
            
            # create error message
            message = {
                'status': 510,
                'message': 'Some of the fields are empty'
            }
            resp = jsonify(message) # jsonify message for delivery
            resp.status_code = 510 # tag message with error code
            return resp # return response
    
    # any other errors/exceptions will ba catched here:
    except Exception as e:
        # close connection to database in case it doesn't close properly
        cur.close()
        conn.close()

	    # create error message for delivery:
        message = {
            'status': 500,
            'message': 'Error: ' + str(e)
        }
        resp = jsonify(message) # jsonify response/message for delivery
        resp.status_code = 500 # tage response/message with error code
        return resp # return response


# URL not found error catched here
@app.errorhandler(404)
def not_found(error = None):
    # create error message
    message = {
        'status': 404,
        'message': 'Not found: ' + request.url
    }
    resp = jsonify(message) # jsonify message for delivery
    resp.status_code = 404 # tag error message with code
    return resp # return response


# launch application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000', debug=True)

