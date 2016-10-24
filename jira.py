import json
import pickle
import requests

def getUsername():
    file_name = "config"
    return_val = ''

    try:
        file_object = open(file_name, 'rb')
        c = pickle.load(file_object)
        return_val = c['username']
    except:
        pass

    return return_val

def getPassword():
    file_name = "config"
    return_val = ''

    try:
        file_object = open(file_name, 'rb')
        c = pickle.load(file_object)
        return_val = c['password']
    except:
        pass

    return return_val

def getURL():
    file_name = "config"
    return_val = ''

    try:
        file_object = open(file_name, 'rb')
        c = pickle.load(file_object)
        return_val = c['URL']
    except:
        pass

    return return_val

def getsessionURL():
    file_name = "config"
    return_val = ''

    try:
        file_object = open(file_name, 'rb')
        c = pickle.load(file_object)
        return_val = c['sessionURL']
    except:
        pass

    return return_val


class jirasession(requests.Session):
    def __init__(self, sessionurl, username, password):
        super().__init__()
        self.verify = False  # because I don't have a verified cert
        self.get(sessionurl, auth=(username, password))  # need to use encrypted auth

    def issue(self, url, key):
        url = url + '/issue/{0}'.format(key)
        session_response = self.get(url)
        if session_response.status_code != 200:
            raise Exception(session_response.status_code)

        return json.loads(session_response.text)

    def query(self, url, jql, fields, maxresults):
        url = url + '/search?jql={0}&fields={1}&maxResults={2}'.format(jql, fields, maxresults)
        print(url)
        print(self)
        session_response = self.get(url)
        if session_response.status_code != 200:
            raise Exception(session_response.status_code)

        return json.loads(session_response.text)


