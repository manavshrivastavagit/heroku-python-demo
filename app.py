# app.py
from flask import Flask, request, jsonify
import psycopg2
import requests



app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print("got name {name}")

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = "Welcome {name} to our awesome platform!!"

    # Return the response in json format
    return jsonify(response)

@app.route('/post/', methods=['POST'])
def post_something():
    param = request.form.get('name')
    print(param)
    # You can add the test cases you made in the previous function, but in our case here you are just testing the POST functionality
    if param:
        return jsonify({
            "Message": "Welcome {name} to our awesome platform!!",
            # Add this option to distinct the POST request
            "METHOD" : "POST"
        })
    else:
        return jsonify({
            "ERROR": "no name found, please send a name."
        })



@app.route('/getallemployees/', methods=['GET'])
def get_all_employee_names():
    url = requests.utils.urlparse(
        'postgres://uadqvrzvvhsgvl:76e9e53176d897f8bb1290fec47bcdde69043710aecb602067de96961e1c7bc0@ec2-107-21-126-201.compute-1.amazonaws.com:5432/d7d2gs1qbqj579')

    db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

    print(url.path)
    print(url.username)
    conn = psycopg2.connect(db)
    print('Connected to Heroku')
    cur = conn.cursor()
    try:
        cur.execute("""SELECT first_name, last_name from public.enq_emp_details""")
        rows = cur.fetchall()
        employee_list = []
        for row in rows:
            employee_list.append(row[0])
        return jsonify(results = employee_list )
    except Exception as e:
        print(e)


# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to Nero server !!</h1>"
if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(threaded=True, port=5000)