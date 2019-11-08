# app.py
from flask import Flask, request, jsonify

import dialogflow

import psycopg2
import requests

from exception.employee_not_found import EmployeeNotFound

url = requests.utils.urlparse(
        'postgres://uadqvrzvvhsgvl:76e9e53176d897f8bb1290fec47bcdde69043710aecb602067de96961e1c7bc0@ec2-107-21-126-201.compute-1.amazonaws.com:5432/d7d2gs1qbqj579')

db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

print(url.path)
print(url.username)
conn = psycopg2.connect(db)

app = Flask(__name__)

@app.route('/getmsg/', methods=['GET'])
def respond():
    # Retrieve the name from url parameter
    name = request.args.get("name", None)

    # For debugging
    print("got name: " + name)

    response = {}

    # Check if user sent a name at all
    if not name:
        response["ERROR"] = "no name found, please send a name."
    # Check if the user entered a number not a name
    elif str(name).isdigit():
        response["ERROR"] = "name can't be numeric."
    # Now the user entered a valid name
    else:
        response["MESSAGE"] = "Welcome "+ name +" to our awesome platform!!"

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
        return jsonify(e)

@app.route('/getenqueroaccounts/', methods=['GET'])
def get_enquero_accounts():
    cur = conn.cursor()
    try:
        cur.execute("""select count(account) from (select distinct account from public.enq_emp_details) a """)
        account_count = cur.fetchall()
        return account_count
    except Exception as e:
        return jsonify(e)

@app.route('/getreportingmanager', methods=['GET'])
def get_reporting_manager(first_name='Ronak', last_name = 'Omprakash'):
    cur = conn.cursor()
    try:
        stm = "select first_name, last_name, reporting_lead from public.enq_emp_details where first_name = '%s' or last_name = '%s' " % (first_name, last_name)
        print ("stm-->",stm )
        cur.execute(stm)
        reporting_manager = cur.fetchall()
        if reporting_manager is None or '':
            raise EmployeeNotFound
        return jsonify(result = reporting_manager )
    except EmployeeNotFound as e:
        return jsonify('No employee found by that name')
    except Exception as e:
        return jsonify(e)

# A welcome message to test our server
@app.route('/')
def index():
    return "<h1>Welcome to our server !!</h1>"

# check DF server connection
@app.route('/api/v1/ask-nero', methods=['GET'])
def askNero():
     # Retrieve the name from url parameter
    query = request.args.get("query", None)
    return detect_intent_texts("nero-sgiuhb", "123", query, "en-US" )

# check DF server connection
@app.route('/df', methods=['GET'])
def df():
     # Retrieve the name from url parameter
     # query = request.args.get("query", None)
    return detect_intent_texts("nero-sgiuhb", "123", "Hi", "en-US" )    


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print('Session path: {}\n'.format(session))

    
    text_input = dialogflow.types.TextInput(
        text=texts, language_code=language_code)

    query_input = dialogflow.types.QueryInput(text=text_input)

    response = session_client.detect_intent(
        session=session, query_input=query_input)

    print('=' * 20)
    # print('Query text: {}'.format(response.query_result.query_text))
    print('Query text: {}'.format(response.query_result.query_text))
    print('Detected intent: {} (confidence: {})\n'.format(
        response.query_result.intent.display_name,
        response.query_result.intent_detection_confidence))
    print('Fulfillment text: {}\n'.format(
        response.query_result.fulfillment_text)) 
    print('Fulfillment query_result: {}\n'.format(
        response.query_result)) 
    return response.query_result.fulfillment_text       

if __name__ == '__main__':
    # Threaded option to enable multiple instances for multiple user access support
    app.run(debug=True, port=5000)