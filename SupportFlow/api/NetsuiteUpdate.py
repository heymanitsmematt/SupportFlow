import requests
import simplejson

class MassNetsuiteGet:
    def __init__(self, updateRange):
        '''
	update range will be either 'all' or a list of (startdate, title, customer) tuples
        '''
        self.auth = 'NLAuth nlauth_account=926273, nlauth_email=mwillis@motionsoft.net, nlauth_signature=@Power88cake, nlauth_role=3'
	self.headers = {}
	self.headers['Authorization'] = self.auth
	self.headers['Content-Type'] = 'application/json'
	self.headers['Accept'] = '*/*'
	self.data = {}
	self.data['data'] = updateRange
	self.data = simplejson.dumps(self.data)
	self.url = 'https://rest.netsuite.com/app/site/hosting/restlet.nl?script=32&deploy=1'

    def post(self):
	self.req = requests.post(self.url, data=self.data, headers = self.headers)
	self.tickets = simplejson.loads(self.req.json())

