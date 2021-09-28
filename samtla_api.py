import requests, time, simplejson as json

class model(object):
    def __init__(self, username=None, password=None, gazetteer={}):
        if username == None:
            print("Please setup your credentials with username as the first argument, and password as the second.")
            return
        self.url = 'http://www.samtla.com/samtlaAPI/v1/'
        self.gazetteer = {}
        self.token = self.login(username, password)
        print("Token:", self.token)

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

    def trainNER(self, gaz=None):
        endpoint = 'trainNER/'
        print("Training the NER on your data")
        print("This may take some time depending on the size of your corpus...")

        if gaz == None:
            gaz = self.gazetteer 
        for i in range(0, 6):
            if i == 0:
                print ("Training baseline model...")
            else:
                print("Training iteration: ", i)
            response = requests.post(self.url + endpoint, data={'token': self.token, '_id': i, 'gazetteer': gaz})
        return response

    def getNER(self, text):
        endpoint = 'getNER/'
        response = requests.post(self.url + endpoint, data={'token': self.token, 'text': text})
        return response.json()

    def getProgress(self):
        endpoint = 'getProgress/'
        response = requests.post(self.url + endpoint, data={'token': self.token})
        return response.json()

    

m = model("<USERNAME>","<PASSWORD>")
sent = m.getSenti("The word 'amazing' is now negative. Pretty cool.", {'amazing':-5})
print(sent)

q1 = '''
Transport Secretary Grant Shapps said more than £25m of historical payments due to the Department for Transport were not paid.
He said the Operator of Last Resort would take over the running of rail services in the south east to protect taxpayers' interests.
Southeastern said passengers would see no change in day-to-day operations.
Mr Shapps said: "We won't accept anything less from the private sector than a total commitment to their passengers, and transparency with taxpayers.
'''

NER = m.getNER(q1)
print(NER)
