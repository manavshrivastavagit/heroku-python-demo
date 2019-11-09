import requests

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    print("My RESPONSE ------> ", response)
    #requests.get(url+'/')