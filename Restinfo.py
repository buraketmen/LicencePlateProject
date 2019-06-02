import requests
import pprint

url = 'https://my-json-server.typicode.com/typicode/demo/comments'
getRestApi = requests.get(url)
##########get#############
getRestApi_json = getRestApi.json()
print(type(getRestApi_json))
pprint.pprint(getRestApi_json)
elements = getRestApi_json
for x in elements:
    print("id: {0} \t b:{1}".format(x['id'], x['body']))

########post##############
username = "buraketmen"
name="Burak"
payloadwithdata= "{\"username\":"+username+",\"name\":\""+name+"\}"
payload = "{\"username\":\"buraketmen\",\password\": \"burak\"}"
response = requests.request("POST",url,data=payloadwithdata)
#r_cookie = response.json()['cookie']
#headers = {'cookie': r_cookie}
#responsewithcookie=requests.request("POST", url, data=payloadwithdata, headers=headers)
#print(response.text)
#print(response.headers)