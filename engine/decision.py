import requests
import json

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    if not fulfillment_text:
        if 'team members' in query_text and 'know_your_team' in intent:
            team_members = requests.get(url+'/getteammembers?firstname='+firstname+'&lastname='+lastname)
            print(team_members)
            return team_members
    else:
     return fulfillment_text