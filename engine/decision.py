import requests

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    #print("My RESPONSE ------> ", response)
    print('Query - My Text : ' , response.query_result.query_text)
    #requests.get(url+'/')