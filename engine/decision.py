import requests
import json

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    if not fulfillment_text:
        if 'team members' in query_text and 'know_your_team' in intent:
            s = "Team members are : "
            t = requests.get(url+'/getteammembers?firstname='+firstname+'&lastname='+lastname)
            team_members = t.json()
            print(team_members)
            for name in team_members:
                s = s + str(team_members[name])
            return s
        elif 'reporting manager' in query_text and 'know_self' in intent:
            s = "Reporting Manager is: "
            firstname = 'shruti'
            lastname = 'jain'
            t = requests.get(url + 'getreportingmanager?firstname='+firstname+'&lastname='+lastname)
            rm = t.json()
            for name in rm:
                s = s + str(rm[name])
            return s

    else:
     return fulfillment_text