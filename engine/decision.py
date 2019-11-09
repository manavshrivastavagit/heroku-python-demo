import requests
import json
from google.protobuf.json_format import MessageToJson

url = 'https://nero-enquero.herokuapp.com'


def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    reporting_lead = ''
    print("---------Response:"+str(response))
    jsonObj = MessageToJson(response.query_result)
    print(json.loads(jsonObj)["parameters"])
    att = json.loads(jsonObj)["parameters"]
    txt = att['col_name']
    print("TEXT: " + txt)
    if not fulfillment_text:
        if txt == 'team' and 'know_your_team' in intent:
            s = "Team members are : "
            t = requests.get(url+'/getteammembers?firstname='+firstname+'&lastname='+lastname)
            team_members = t.json()
            print(team_members)
            for name in team_members:
                s = s + str(team_members[name])
            return s
        elif txt == 'reporting_lead' and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getreportingmanager?firstname='+firstname+'&lastname='+lastname)
            rm = t.json()
            for name in rm:
                s = s + str(rm[name])
            s = s[2:-2]
            s = 'Reporting Manager: ' + s
            return s
        elif txt == 'business_unit_description' and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getbusinessunit?firstname='+firstname+'&lastname='+lastname)
            bu = t.json()
            for name in bu:
                s = s + str(bu[name])
            s = s[2:-2]
            s = 'Business Unit is: ' + s
            return s
        elif txt == 'account' and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getprojectname?firstname='+firstname+'&lastname='+lastname)
            pj = t.json()
            for name in pj:
                s = s + str(pj[name])
            s = s[2:-2]
            s = 'Account is: ' + s
            return s
        elif txt == 'reporting_lead' and 'know_others' in intent:
            firstname = att['given-name']
            lastname = att['last-name']
            print("Firstname : " + firstname)
            print(lastname)
            reporting_lead = lastname.lower() + ', ' + firstname.lower()
            s = ""
            t = requests.get(url + '/reporteecount?reporting_lead='+reporting_lead)
            rc = t.json()
            for name in rc:
                s = s + str(rc[name])
            s = s[2:-2]
            s = 'Location is: ' + s
            return s
        elif txt == 'hire_date' and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getjoiningdate?firstname='+firstname+'&lastname='+lastname)
            doj = t.json()
            for name in doj:
                s = s + str(doj[name])
            s = s[2:-2]
            s = 'Date of Joining is: ' + s
            return s
        elif txt == 'practice_lead' and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getpractielead?firstname='+firstname+'&lastname='+lastname)
            pl = t.json()
            for name in pl:
                s = s + str(pl[name])
            s = s[2:-2]
            s = 'Practice Lead is: ' + s
            return s
        elif txt == 'location_description' and 'know_others' in intent:
            firstname = att['given-name']
            lastname = att['last-name']
            s = ""
            t = requests.get(url + '/location?firstname='+firstname+'&lastname='+lastname)
            loc = t.json()
            for name in loc:
                s = s + str(loc[name])
            s = s[2:-2]
            s = 'Location is: ' + s
            return s
        elif 'largest account' in query_text or 'biggest account' in query_text and 'know_aggr' in intent:
            s = ""
            t = requests.get(url + '/largestaccount')
            cb = t.json()
            for name in cb:
                s = s + str(cb[name])
            s = s[2:-2]
            s = 'Largest account at Enquero is: ' + s
            return s


        elif 'business' in query_text or 'head count' in query_text and 'know_aggr' in intent:
            s = ""
            t = requests.get(url + '/countbybusinesstitle')
            cb = t.json()
            for name in cb:
                s = s + str(cb[name])
            s = s[2:-2]
            s = 'Business count is: ' + s
            return s



    else:
     return fulfillment_text