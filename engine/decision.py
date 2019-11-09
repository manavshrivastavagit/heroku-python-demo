import requests

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    print(response)
    #requests.get(url+'/')