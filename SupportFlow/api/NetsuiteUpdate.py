import requests
import simplejson
from app.models import *
from jira.client import JIRA
#from api.views import jira_username, jira_password
import pdb
import sys

jira_username = 'mwillis'
jira_password = 'Richard*&'

class MassNetsuiteGet:
    def __init__(self, updateRange, trackedUpdate=False, fixUpdate=False, debug=False):
        '''
	updateRange will be either 'all' or a list of (startdate, title, customer) tuples *note ns limits search to 1000
        fixUpdate will only search netsuite for those tickets with the Jira Status populated in Netsuite but no fix version etc.
        dubug will allow the user to set a cookie provided by netsuite in the console
        '''
        self.debug = debug
        self.trackedUpdate = trackedUpdate
        self.errors = list()
        self.auth = 'NLAuth nlauth_account=926273, nlauth_email=mwillis@motionsoft.net, nlauth_signature=@Power88cake, nlauth_role=3'
	self.headers = {}
        self.headers['Authorization'] = self.auth
	self.headers['Content-Type'] = 'application/json'
	self.headers['Accept'] = '*/*'
        self.data = {}
	self.data['data'] = updateRange
	self.data = simplejson.dumps(self.data)
        if trackedUpdate == False:
            self.url = 'https://rest.netsuite.com/app/site/hosting/restlet.nl?script=32&deploy=1'
        elif trackedUpdate == True:
            self.url = 'https://rest.netsuite.com/app/site/hosting/restlet.nl?script=35&deploy=1'
            if fixUpdate == True:
                self.url = 'https://rest.netsuite.com/app/site/hosting/restlet.nl?script=36&deploy=1'
        joptions = {'server':'http://jira.motionsoft.com:8080'}
        self.jCon = JIRA(joptions, basic_auth=(jira_username, jira_password))


    def post(self):
        if self.trackedUpdate == False:
            self.req = requests.post(self.url, data=self.data, headers = self.headers)
        elif self.trackedUpdate == True:
            self.req = requests.get(self.url, data=self.data, headers = self.headers)
	self.tickets = simplejson.loads(self.req.json())

    def save(self):

        for ticket in self.tickets:
            try:
                thisTicket = Ticket.objects.get_or_create(netsuite_id = ticket['id'])[0]
            except:
                thisTicket = Ticket.objects.all().filter(netsuite_id = ticket['id'])[0]
            thisTicket.customer = ticket['columns']['company']['name']
            try:
                thisTicket.caller = ticket['columns']['caller']['name']
            except KeyError: pass
            thisTicket.netsuite_case_number = ticket['columns']['casenumber']
            thisTicket.case_type = ticket['columns']['category']['name']
            thisTicket.status = ticket['columns']['status']['name']
            try:
                thisTicket.assigned_to = ticket['columns']['assigned']['name']
            except: pass
            try:
                thisTicket.opened_by = ticket['columns']['custeventcase_created_user']['name']
            except KeyError: pass
            thisTicket.save()

    def updateTrackedStatus(self, fix=False):
        '''
            TO DO: Add in ns fields for Priority, Fix Version, and Last Updated Date. Populate with JIRA info
        '''

        self.updateURL = 'https://rest.netsuite.com/app/site/hosting/restlet.nl?script=35&deploy=1'
        updatedJissues = []

        if self.debug == True:
            self.headers.pop('Authorization')
            nsver = raw_input("Enter the NSVER from the Netsuite Debugger ")
            jsessionid = raw_input("Enter the JSESSIONID from the Netsuite Debugger ")
            self.cookies = {'JSESSIONID':jsessionid, 'NS_VER':nsver}

        for ticket in self.tickets:
            try:
                localJissue = JiraTicket.objects.get(jira_issue = ticket['columns']['custeventsn_case_number'])
                newJissue = False
            except:
                try:
                    localJissue = JiraTicket.objects.create(jira_issue = ticket['columns']['custeventsn_case_number'])
                    newJissue = True
                except:
                    print ticket['id']
            try:
                jiraIssue = self.jCon.issue(ticket['columns']['custeventsn_case_number'])
                
                #hackey fix to get around Jira Tickets tracked to multiple Jira Issues
                if newJissue == False and localJissue in (updatedJissues):
                    newJissue = True

                if localJissue.status != jiraIssue.fields.status.name or newJissue == True:
                    self.payload = {}
                    self.payload['id'] = ticket['id']
                    self.payload['jiraStatus'] = jiraIssue.fields.status.name
                    self.payload['fixVersions'] = ', '.join([f.name for f in jiraIssues.fields.fixVersions])
                    self.payload['priority'] = jiraIssue.fields.priority.name
                    #components can be a list, flatten that to a string
                    self.payload['components'] = ', '.join([c.name for c in jiraIssue.fields.components])

                    self.payload = simplejson.dumps(self.payload)
                    if self.debug == False:
                        pass
                        updateReq = requests.post(self.updateURL, data=self.payload, headers=self.headers)
                    elif self.debug == True:
                        updateReq = requests.post(self.updateURL, data=self.payload, cookies=self.cookies, headers=self.headers)
                    print ticket['columns']['casenumber']
                    localJissue.status = jiraIssue.fields.status.name
                    localJissue.save()
                    updatedJissues.append(localJissue)
                else:
                    pass
            except:
                err = sys.exc_info()
                #pdb.set_trace()
                self.errors.append(ticket)
                
        del updatedJissues[:]


