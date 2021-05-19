from flask import Flask, request, jsonify
from csv import DictReader, DictWriter

app = Flask(__name__)

@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    try:
        with open('users.csv', "r+") as f:
            open_file = f.readlines()
            for row in DictReader(open_file):
                if(row['email'] == data.get('email')):
                    return ('', 422)
                        
            headers = get_headers()
            last_id = open_file[-1].split(',')[0]
            if last_id == 'id':
                last_id = 0
            writer = DictWriter(f, fieldnames=headers)
            body = {**data, 'id': int(last_id) + 1}
            writer.writerows([body])
            f.close()            
            return jsonify(body)                        
    except:
        return jsonify(FileNotFoundError)


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        with open('users.csv', "r") as f:
            open_file = f.readlines()
            for row in DictReader(open_file):
                if(row['email'] == data.get('email') and row['password'] == data.get('password')):
                    row.pop('password')
                    return jsonify(row)
            f.close()
        return ('', 401)
    except:
        return jsonify(FileNotFoundError)

@app.route('/profile/<int:user_id>', methods=['PATCH'])
def update(user_id):
    data = request.json
    data_complete = []
    edit_row = ""
    if(user_id):
        try:
            with open('users.csv', "r") as f:
                open_file = f.readlines()
                headers = get_headers()
                for row in DictReader(open_file):

                    if(int(row['id']) == user_id):
                        if data.get('name'):
                            row['name'] = data.get('name')
                        if data.get('email'):
                            row['email'] = data.get('email')
                        if data.get('age'):
                            row['age'] = data.get('age')
                        if data.get('password'):
                            row['password'] = data.get('password')
                        row['id'] = int(row['id'])
                        edit_row = row
                    data_complete.append({'id': int(row['id']), 'name': row['name'], 'email': row['email'], 'age': int(row['age']), 'password': row['password']})    
                f.close()
                if(edit_row):
                    edit_row.pop('password')
                    with open('users.csv', 'w') as file:
                        writer = DictWriter(file, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(data_complete)
                        file.close()
                    return jsonify(edit_row)
                else:
                    return ('', 404)
        except:
            return jsonify(FileNotFoundError)
    else:
        return ('', 401)

@app.route('/users', methods=['GET'])
def get():
    list_data = []
    try:
        with open('users.csv', "r") as f:
            for row in DictReader(f):
                list_data.append({'id': int(row['id']), 'name': row['name'], 'email': row['email'], 'age': int(row['age'])})
            return jsonify(list_data)
    except:
        return jsonify(FileNotFoundError)

@app.route('/profile/<int:user_id>', methods=['DELETE'])
def deletes(user_id):
    if(user_id):
        list_data = []
        try:
            with open('users.csv', "r") as f:
                open_file = f.readlines()
                headers = get_headers()
                for row in DictReader(open_file):
                    if(int(row['id']) != user_id):
                        list_data.append(row)

                f.close()
                if(list_data):
                    with open('users.csv', 'w') as file:
                        writer = DictWriter(file, fieldnames=headers)
                        writer.writeheader()
                        writer.writerows(list_data)
                        file.close()
                    return ('', 204)

        except:
            return ('', 404)
    else:
        return ('', 401)

def get_headers():
    try:
        with open('users.csv', "r") as f:
            open_file = f.readlines()
            headers = list(open_file[0].split(','))
            headers[-1] = headers[-1][:8]
            f.close()
            return headers
    except:
        return []

    
