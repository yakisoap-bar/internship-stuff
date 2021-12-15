import requests

# send prediction POST request to specified URL
def predict_post(url, data):
    '''
    Send POST request to specified URL. 

    PARAMETERS
    url: URL to send post request to
    data: prediction arrays to send to `url`

    Returns a list containing the returned status code 
    and json body from server: `[status, <json>]`.
    '''
    # put data into dict for sending to server
    body = {'data' : data}

    # send request
    r = requests.post(url, json=body)

    if len(r.text) == 0:
        return [r.status_code, {'message' : 'Invalid URL.'}]

    return [r.status_code, r.json()]