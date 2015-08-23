#!/usr/bin/env python3

import requests
import json
import os

X_HON_Client_Id = os.getenv("X_HON_Client_Id")
X_HON_API_Token = os.getenv("X_HON_API_Token")

headers = {"X-HON-Client-Id":X_HON_Client_Id,"X-HON-API-Token":X_HON_API_Token}
API_URL = "https://api.happy-or-not.com/v1"

class HappyOrNot:

  def __init__(self):
    self.results = self.getFolders()

  def getFolders(self):
    url = API_URL + "/folders?surveys=true" 
    r = requests.get(url, headers=headers)
    return r.json()
  
  def getSurveyResults(self, key):
    url = API_URL + "/surveys/" + key + "/results"
    r = requests.get(url, headers=headers)
    return r.json()
  
  def addSurveyResults(self):
    for agency in self.results["folders"]:
      try:
        for f in agency["folders"]:
          for s in f["surveys"]:
            s["results"] = self.getSurveyResults(str(s["key"]))
      except:
        next
    return self.results

  def getJSON(self):
    return json.dumps(self.addSurveyResults(),indent=2)

#print(HappyOrNot().getJSON())
