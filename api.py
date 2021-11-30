#!/usr/bin/python
import sqlite3
from robyn import Robyn, jsonify


def connect_to_db():
    conn = sqlite3.connect('database.db')
    return conn


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''DROP TABLE users''')
        conn.execute('''
            CREATE TABLE users (
                user_id INTEGER PRIMARY KEY NOT NULL,
                name TEXT NOT NULL,
                email TEXT NOT NULL,
                phone TEXT NOT NULL,
                address TEXT NOT NULL,
                country TEXT NOT NULL
            );
        ''')

        conn.commit()
        print("User table created successfully")
    except:
        print("User table creation failed - Maybe table")
    finally:
        conn.close()


def insert_user(user):
    inserted_user = {}
    print(user)
    print(user["name"])
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (name, email, phone, address, country) VALUES (?, ?, ?, ?, ?)", (user['name'], user['email'], user['phone'], user['address'], user['country']) )
        conn.commit()
        inserted_user = get_user_by_id(cur.lastrowid)
    except:
        conn().rollback()

    finally:
        conn.close()

    return inserted_user


def get_users():
    users = []
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        # convert row objects to dictionary
        for i in rows:
            user = {}
            user["user_id"] = i["user_id"]
            user["name"] = i["name"]
            user["email"] = i["email"]
            user["phone"] = i["phone"]
            user["address"] = i["address"]
            user["country"] = i["country"]
            users.append(user)

    except:
        users = []

    return users


def get_user_by_id(user_id):
    user = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cur.fetchone()

        # convert row object to dictionary
        user["user_id"] = row["user_id"]
        user["name"] = row["name"]
        user["email"] = row["email"]
        user["phone"] = row["phone"]
        user["address"] = row["address"]
        user["country"] = row["country"]
    except:
        user = {}

    return user


def update_user(user):
    updated_user = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE users SET name = ?, email = ?, phone = ?, address = ?, country = ? WHERE user_id =?", (user["name"], user["email"], user["phone"], user["address"], user["country"], user["user_id"],))
        conn.commit()
        #return the user
        updated_user = get_user_by_id(user["user_id"])

    except:
        conn.rollback()
        updated_user = {}
    finally:
        conn.close()

    return updated_user


def delete_user(user_id):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE from users WHERE user_id = ?", (user_id,))
        conn.commit()
        message["status"] = "User deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete user"
    finally:
        conn.close()

    return message


users = []
user0 = {
    "name": "Charles Effiong",
    "email": "charles@gamil.com",
    "phone": "067765665656",
    "address": "Lui Str, Innsbruck",
    "country": "Austria"
}

user1 = {
    "name": "Sam Adebanjo",
    "email": "samadebanjo@gamil.com",
    "phone": "098765465",
    "address": "Sam Str, Vienna",
    "country": "Austria"
}

user2 = {
    "name": "John Doe",
    "email": "johndoe@gamil.com",
    "phone": "067765665656",
    "address": "John Str, Linz",
    "country": "Austria"
}

user3 = {
    "name": "Mary James",
    "email": "maryjames@gamil.com",
    "phone": "09878766676",
    "address": "AYZ Str, New york",
    "country": "United states"
}

users.append(user0)
users.append(user1)
users.append(user2)
users.append(user3)

create_db_table()

for i in users:
    print(insert_user(i))




app = Robyn(__file__)

@app.get('/api/users')
def api_get_users():
    return jsonify(get_users())

@app.get('/api/users/:<user_id>')
def api_get_user(user_id):
    return jsonify(get_user_by_id(user_id))

@app.post('/api/users/add')
def api_add_user(request):
    body = bytearray(request["body"]).decode("utf-8")
    print(body)
    import json
    # print(json.loads(body)["abd"])


    # user = request.get_json()
    return jsonify(insert_user(json.loads(body)))
    return ""

@app.put('/api/users/update')
def api_update_user(request):
    # user = request.get_json()
    body = bytearray(request["body"]).decode("utf-8")
    import json
    print(json.loads(body)["abd"])

    # return jsonify(update_user(user))
    return ""
    
@app.delete('/api/users/delete/:user_id')
def api_delete_user(request):
    print(request["params"]['user_id'])
    return jsonify(delete_user(int(request["params"]['user_id'])))


if __name__ == "__main__":
    #app.debug = True
    #app.run(debug=True)
    app.start(port=8081)


# curl -X POST -d "{ \"name\": \"Mary James\",\"email\": \"maryjames@gamil.com\", \"phone\": \"09878766676\", \"address\": \"AYZ Str, New york\", \"country\": \"United states\"}" http://127.0.0.1:8081/api/users/add

