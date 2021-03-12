import pyrebase
from collections import OrderedDict

config = {
    "apiKey": "AIzaSyDi3zfU3Rvss13z48DoIggFJcLh_L0TLs8",
    "authDomain": "accordianapp-dfd8a.firebaseapp.com",
    "databaseURL": "https://accordianapp-dfd8a-default-rtdb.firebaseio.com",
    "projectId": "accordianapp-dfd8a",
    "storageBucket": "accordianapp-dfd8a.appspot.com",
    "messagingSenderId": "851198765234",
    "appId": "1:851198765234:web:f43b855613d2399db481ab",
    "measurementId": "G-8E0YH12FJT"
}

firebase = pyrebase.initialize_app(config)

db = firebase.database()

from flask import *

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def basic():
    if request.method == 'POST':
        if request.form['submit'] == 'add':
            name = request.form['name']
            db.child("todo").push(name)
            todo = db.child("todo").get()
            to = todo.val()
            return render_template('index.html', t=to.values())
        elif request.form['submit'] == 'delete':
            db.child("todo").remove()
        return render_template('index.html')
    return render_template('index.html')


@app.route('/string_match', methods=['GET'])
def string_match():
    # Obtain string from POST request, number that is keyed in the lock
    string_ = request.args.get("string")
    # string_ = request.form['keypad']

    # db.child("todo").child("1234").update({"done":True,"itemDataText":"1111","uid":"lmao"})
    # TESTING to search through details dictionary
    details = db.child("todo").get()
    details = dict(OrderedDict(details.val()))
    print(details)

    for key, value in details.items():
        print("key", key)
        print("value", value)
        if value['itemDataText'] == string_:
            print("THANK GOD")
            uid = value["uid"]
            itemDataText = value["itemDataText"]
            print("value uid:",uid)
            print("value value:",itemDataText)
            # Update 'done' in server
            db.child("todo").child(value['uid']).update({"done": False, "itemDataText": itemDataText, "uid": uid})


if __name__ == '__main__':
    app.run(host="192.168.31.197", debug=False)
