import requests

url = 'https://nero-enquero.herokuapp.com'
def response_parser(response, firstname, lastname):
    query_text = response.query_result.query_text
    fulfillment_text = response.query_result.fulfillment_text
    print('^^^^^^^', response)
    print('======= response completed')
    intent = response.query_result.intent.display_name
    print('-------------', intent)
    if not fulfillment_text:
        if 'team members' in query_text:
            pass
    else:
     return fulfillment_text