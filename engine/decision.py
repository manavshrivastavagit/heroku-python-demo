import requests
import json

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    s = "Team members are : "
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    if not fulfillment_text:
        if 'team members' in query_text and 'know_your_team' in intent:
            t = requests.get(url+'/getteammembers?firstname='+firstname+'&lastname='+lastname)
            team_members = t.json()
            print(team_members)
            tm = json.loads(team_members)
            for name in tm:
                for n in name:
                    s = s + n
            print(s)
            return s
    else:
     return fulfillment_text