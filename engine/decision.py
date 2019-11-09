import requests

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    print('---------------' , query_text)
    fulfillment_text = response['query_result'].get('fulfillment_text')
    if fulfillment_text is None:
        print('no text recived routing')
    else:
        print('---------------', fulfillment_text)