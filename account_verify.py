from linepy import *
import requests, json, time, os, string, random

host = 'https://gwk.line.naver.jp'
LA = "BIZIOS\t1.7.5\tiOS\t10.2"
header = {
    'Accept': "application/json",
    "Accept-Language": "ja-KR",
    "X-LHM": 'GET',
    "X-LPV": '1',
    'X-Line-Application': LA
}
path = os.path.dirname(os.path.abspath(__file__))
CMSToken = open(path + '/cms.txt').read()
udidHash = open(path + '/udidHash.txt').read()

count = 10 # Number what you want to create
base_name = 'りんね#'


def randstr(n):
    random_str = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(n)])
    return random_str


for z in range(count):
    random_str = randstr(10)
    name = base_name + random_str
    header.update({'X-CMSToken': CMSToken})

    # phase1 requestRegisterToken
    header.update({'X-LHM': 'GET'})
    endpoint = '/plc/api/core/account/prepare'
    res = requests.post(host + endpoint, headers=header)
    registerToken = res.json()['registerToken']

    # phase2 registerAccount
    endpoint = '/plc/api/core/account/register'
    header.update({'X-LHM': 'POST'})
    payload = {"registerToken": registerToken, "majorCategory": 117, "minorCategory": 1153, "ageVerified": False,
               "displayName": name, "allowBcoaFriendship": 'false',
               "deviceInfo": {"udidHash": udidHash,
                              "model": "iPad5,1"}, "country": "KR"}
    res = requests.post(host + endpoint, data=json.dumps(payload), headers=header)
    accessToken = res.json()['accessToken']
    mid = res.json()['mid']
    
    # phase 2.5 uploadProfilePicture
    line = LINE(idOrAuthToken=accessToken, userAgent=LA)
    path = os.path.dirname(os.path.abspath(__file__)) + '/kizunaai.jpg'
    line.updateProfilePicture(path=path)

    # phase3 requestUnregisterToken
    endpoint = '/plc/api/core/auth/atCC/1418234097'
    payload = {"botMid": mid}
    res = requests.post(host + endpoint, data=json.dumps(payload), headers=header)
    atcc = res.json()['at_cc']

    # phase4 unregisterAccount
    header = {
        'Accept': "application/json",
        "Accept-Language": "ja-KR",
        "X-LHM": 'POST',
        "X-LPV": '1',
        'X-Line-Application': LA,
        'X-CMSToken': CMSToken,
        'X-ATCC': atcc
    }
    endpoint = '/plc/api/core/account/resign'
    random_str = randstr(40)
    payload = {"resignToken": random_str.upper()}
    res = requests.post(host + endpoint, data=json.dumps(payload), headers=header)
