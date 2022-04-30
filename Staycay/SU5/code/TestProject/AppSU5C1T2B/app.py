# import the Flask module and create an app using it
from flask import Flask, json, request
app = Flask(__name__)

data = [
    {'id': '1', 'username': 'John', 'email': 'john@gmail.com'},
    {'id': '2', 'username': 'Mary', 'email': 'mary@gmail.com'},
    {'id': '3', 'username': 'Peter', 'email': 'peter@gmail.com'},
    {'id': '4', 'username': 'Ann', 'email': 'ann@gmail.com'},
]


@app.route('/')
def main():
    return 'ICT239 T02 Website'


# Read
@app.route('/students')
def students():
    return json.dumps(data)


@app.route('/students/<idx>')
def detail(idx):
    for item in data:
        if item['id'] == idx:
            return json.dumps(item)
    return 'No Student with ID ' + idx


# Delete
@app.route('/students/delete/<idx>')
def delete(idx):
    for i, item in enumerate(data):
        if item['id'] == idx:
            removed_item = data.pop(i)
            return 'Removed ' + json.dumps(removed_item)
    return 'No Student with ID ' + idx


# Create
@app.route('/students/add', methods=['POST', 'GET'])
def add():
    if request.method == 'POST':
        # auto generating id by incrementing 1
        # from id of last item in the list
        idx = int(data[len(data)-1]['id']) + 1
        d = dict()
        d['id'] = str(idx)
        d['username'] = request.form.get('username')
        d['email'] = request.form.get('email')
        data.append(d)
        return json.dumps(data)
    return """
    <form method='POST'>
        <label for='username'>Username</label>
        <input id='username' name='username'><br>
        <label for='email'>Email</label>
        <input name='email'><br>
        <button>Submit</button>
    </form>
    """


# Update
@app.route('/students/update/<idx>', methods=['POST', 'GET'])
def update(idx):
    if request.method == 'POST':
        email = request.form.get('email')
        for item in data:
            if item['id'] == idx:
                item['email'] = email
                return json.dumps(item)
                break
    return """
    <form method='POST'>
        <label for='email'>Email</label>
        <input name='email'><br>
        <button>Submit</button>
    </form>
    """


# check if the executed file is the main program; if so, run the app
if __name__ == '__main__':
    app.run(debug=True)


