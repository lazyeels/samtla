import requests, time, simplejson as json

class model(object):
    def __init__(self, username=None, password=None, gazetteer={}):
        if username == None:
            print("Please setup your credentials with username as the first argument, and password as the second.")
            return
        self.url = 'http://www.samtla.com/samtlaAPI/v1/'
        self.gazetteer = {}
        self.token = self.login(username, password)

    def login(self, username, password):
        endpoint = "login/"
        r = requests.post(self.url + endpoint, data={'username': username, 'password': password})
        return json.loads(r.text).get("token", None)
        

    def starsToRaw(self, star):
        if star == None: return 0
        return (star - 3.0) / 2.0

    def getSenti(self, text=None, gaz={}):
        if self.token == None: print("You must login to continue...")
        endpoint = 'getSenti/'
        if gaz == None:
            gaz = self.gazetteer
        if text == None:
            print("You have not specified the text content as the first argument to this function call.") 
            return {}
        response = requests.post(self.url + endpoint, data={'token': self.token, 'text': text, 'gaz': json.dumps(gaz)})
        response = response.json()
        response['sentiment_score'] = self.starsToRaw(response.get('Stars',0))
        return response


m = model("USERNAME","PASSWORD")
sa = m.getSenti("this text is amazing!")
print(sa)
