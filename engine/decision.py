import requests
import json

url = 'https://nero-enquero.herokuapp.com'


def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    intent = response.query_result.intent.display_name
    reporting_lead = ''
    print('^^^^^^^^^^' + response.query_result.parameters.fields.attribute)
    print("---------Response:"+str(response))
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
            s = ""
            t = requests.get(url + '/getreportingmanager?firstname='+firstname+'&lastname='+lastname)
            rm = t.json()
            for name in rm:
                s = s + str(rm[name])
            s = s[2:-2]
            s = 'Reporting Manager: ' + s
            return s
        elif 'business unit' in query_text or 'bu' in query_text and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getbusinessunit?firstname='+firstname+'&lastname='+lastname)
            bu = t.json()
            for name in bu:
                s = s + str(bu[name])
            s = s[2:-2]
            s = 'Business Unit is: ' + s
            return s
        elif 'project' in query_text or 'account' in query_text and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getprojectname?firstname='+firstname+'&lastname='+lastname)
            pj = t.json()
            for name in pj:
                s = s + str(pj[name])
            s = s[2:-2]
            s = 'Account is: ' + s
            return s
        elif 'who all report' in query_text and 'know_others' in intent:
            firstname = response.query_result.fields.given-name
            lastname = response.query_result.fields.last-name
            print(firstname)
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
        elif 'doj' in query_text or 'date of joining' in query_text or 'joining date' in query_text or 'hiring' in query_text or 'hire' in query_text and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getjoiningdate?firstname='+firstname+'&lastname='+lastname)
            doj = t.json()
            for name in doj:
                s = s + str(doj[name])
            s = s[2:-2]
            s = 'Date of Joining is: ' + s
            return s
        elif 'practice lead' in query_text or 'project lead' in query_text and 'know_self' in intent:
            s = ""
            t = requests.get(url + '/getpractielead?firstname='+firstname+'&lastname='+lastname)
            pl = t.json()
            for name in pl:
                s = s + str(pl[name])
            s = s[2:-2]
            s = 'Practice Lead is: ' + s
            return s
        elif 'location' in query_text or 'place' in query_text and 'know_others' in intent:
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