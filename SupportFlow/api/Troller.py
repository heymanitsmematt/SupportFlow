import sys
import os
import simplejson
import requests
import HTMLParser
from time import sleep


class EmailTroller:
    def __init__(self):
        parser = HTMLParser.HTMLParser()
        email = 'mwillis@motionsoft.net'
        password = '8Richard&'
        self.url = 'https://outlook.office365.com/ews/odata/Me/Folders/JunkEmail/Messages'
        self.params = {'$orderby':'DateTimeReceived desc', '$top' : '25', '$select' : 'Subject,Body'}
        while 1:
            try:
                self.mostRecentEmail = requests.get(self.url, params=self.params, auth=(email,password))
                self.mostRecentEmailRaw = self.mostRecentEmail.json()['value'][0]['Body']['Content']
                self.cleanup1 = self.mostRecentEmailRaw.split('{')
                self.cleanup2 = self.cleanup1[1].split('}')[0]
                self.cleaned = parser.unescape(self.cleanup2).replace('"','')

                self.subject = self.mostRecentEmail.json()['value'][0]['Subject']

                dicty = {}
        
                for item in self.cleaned.split(','):
                    key, value = item.split(':')
                    if dicty.get(key):
                        dicty[key] += value
                    else:
                        dicty[key] = value

		self.ticketJSON = simplejson.dumps(dicty)

		r = requests.post("http://10.89.30.244/saveNetsuiteTicket/", data=dicty)
                
                print "trolled for", dicty['caseNumber'], r
	
            except:
                print "passed", sys.exc_info()[0] 
                pass
            sleep(10)

troll = EmailTroller()
