import requests

def check_response(r):
    '''
    This function prints the requests response only if response
    is something other than expected
    '''
    if r.status_code == 200:
        return None
    else:
        raise ImportError('Expected response from API: <Response [200]> got: {}'.format(r))

def getBuildingTrendLogs():
    '''
    This function is to be used with Kaizen's get all building api, not done yet, but API can be used to
    create
    '''
    url = 'https://login.coppertreeanalytics.com/oauth/token'

    my_header = {'content-type': 'application/x-www-form-urlencoded'}
    my_data = {
        'grant_type': 'client_credentials',
        'client_id': "fe4kRNoVOPW8aBLBivYbAWSkfSNlh1gJ",
        'client_secret': "Xo7mShCR3msTbf-AnWAxL81EKqdNinSnrIt88eMjqk5FjiCdYqGdqUqBJ6jt-QRa",
        'audience': 'organize'
    }

    r = requests.post(url, headers=my_header, data=my_data)
    check_response(r)
    # print(r.json())
    access_token = r.json()['access_token']
    # print(access_token)
    jwt_header = {'Authorization': 'Bearer ' + access_token,'API':'1351f2dddfc940e2'}
    print(jwt_header)
    url = 'https://kaizen.coppertreeanalytics.com/api/v3/trend_log_objects/?building=2169&page=1'
    print(url)
    web = requests.get(url, headers = jwt_header,data='1351f2dddfc940e2')
    print(web)
    print(web.json())