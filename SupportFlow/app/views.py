import time
import re
import traceback
import sys
from django.shortcuts import render_to_response , render
from django.template import RequestContext
from app.models import *
from django.http import HttpResponseRedirect, HttpResponse
from os import path
import simplejson
from django.core import serializers
from app.forms import *
from django.views.decorators.csrf import csrf_exempt
import pyPdf
import requests
import jira.client
from jira.exceptions import JIRAError
from jira.client import JIRA
import json
from api.cookies import nsver, jsessionid


PROJECT_ROOT = path.dirname(path.abspath(path.dirname(__file__)))
jira_username = 'mwillis'
jira_password = '8Richard&'

def empmain(request):
    template_name = 'app/empmain.html'
    tickets = Ticket.objects.all()

    data = list(tickets)

    json = serializers.serialize('json', data) 

    return render_to_response(template_name, {'tickets': tickets}, context_instance = RequestContext(request)) 

def ticket(request):
    tickets = Ticket.objects.all()
    data = list(tickets)
    json = serializers.serialize('json', data)

    return HttpResponse(json, content_type='application/json')

@csrf_exempt
def saveNetsuiteTicket(request): 
    postData = request.POST
    ticket = Ticket
    numberizer = re.compile(r'[^\d.]+')
    i=0    

    if postData['id'] != '' and postData['id'] !='To Be Generated':
        try:    
	    thisTicket = ticket.objects.get(netsuite_id = numberizer.sub('', postData['id']))
	except:
	    thisTicket = ticket.objects.create(netsuite_id = numberizer.sub('', postData['id']))	
    elif postData['caseNumber'] == 'To Be Generated':
	try:
             thisTicket = ticket.objects.filter(netsuite_case_number__exact = 0, short_description__exact = postData['shortDescription'])
	     thisTicket = thisTicket[0]
	except:
             thisTicket = ticket.objects.create(netsuite_case_number = i)
    elif postData['caseNumber'] != '':
        try:
            thisTicket = ticket.objects.get(netsuite_case_number = numberizer.sub('', postData['caseNumber']))
	except:
	    thisTicket = ticket.objects.create(netsuite_case_number = numberizer.sub('', postData['caseNumber']))
    else:
        try:
            thisTicket = ticket.objects.get(customer = postData['customer'], open_date = postData['openDate'])
        except:
            thisTicket = ticket.objects.create(customer = postData['customer'])

    if numberizer.sub('', postData['caseNumber']) == '':
	thisTicket.netsuite_case_number = i
    else:
	thisTicket.netsuite_case_number = numberizer.sub('',postData['caseNumber'])
    
    try:
	thisTicket.customer = postData['customer']
	thisTicket.callback_phone = postData['callbackPhone']
	thisTicket.case_type = postData['caseType']
	thisTicket.case_origin = postData['caseOrigin']
	thisTicket.product = postData['product']
	thisTicket.module = postData['module']
	thisTicket.short_description = postData['shortDescription']
	thisTicket.status = postData['status']
	thisTicket.severity = postData['severity']
	thisTicket.priority = postData['priority']
	thisTicket.assigned_to = postData['assignedTo']
	thisTicket.escalated_to = postData['escalatedTo']
	thisTicket.open_date = postData['openDate']
	thisTicket.opened_by = postData['openedBy']
	thisTicket.first_call_resolution = postData['firstCallResolution']
	thisTicket.last_updated = postData['lastUpdated']
	thisTicket.jira_issue = postData['jiraIssue']
	thisTicket.most_recent_comment = postData['mostRecentComment']

    	thisTicket.save()   
	i += 1    
    except:
        print "error saving ticket", sys.exc_info()[0]
        traceback.print_exc()
	
    return HttpResponse({'msg':'success?'}, content_type = 'application/json')

def updateNetsuiteTickets(request):
    ticket = Ticket
    skeletonTickets = ticket.objects.filter(netsuite_case_number__exact = 0).values() 
    
    updater = restletUpdater(skeletonTickets)
    print updater.ticketsOut() 
    try:
        for ticket in updater.ticketsOut():
	    try:
	        thisTicket = ticket.objects.get(id = ticket.kbId) 
   	        print thisTicket
	        thisTicket.company = ticket.company
    	        thisTicket.netsuite_case_number = ticket.nsCaseNumber
	        thisTicket.save()
	    except:
	        print "could not find/save ticket", ticket
	msg = {}
	msg["msg"] = "returned restlet successfully"
    except:
	msg=sys.exc_info()[0]
	#simplejson.dumps(msg)
	#with open('/./SupportFlow/SupportFlow/testlog.txt', 'w+') as theFile:
	    #theFile.write(str(sys.exc_info()[0]))
	    #theFile.write(skeletonTickets)
	
    return HttpResponse(msg, content_type='application/json')

class restletUpdater:
    def __init__(self, ticketsIn):
        self.ticketsIn = ticketsIn

    def ticketsOut(self):
        requestDict = {}
	headers = {}
	cookies = {}
	cookies['NS_VER'] = nsver
	cookies['JSESSIONID'] = jsessionid
	headers['Authorization'] = 'NLAuth nlauth_account=926273,nlauth_email=mwillis@motionsoft.net,nlauth_signature=@Power88cake,nlauth_role=3'
	headers['Content-Type'] = 'application/json'
	headers['Accept'] = 'application/json'
        for ticket in self.ticketsIn:
	    thisTicketDict = {}
	    thisTicketDict['kbId'] = ticket['id']
	    thisTicketDict['openDate'] = ticket['open_date']
	    thisTicketDict['shortDescription'] = ticket['short_description']
	    requestDict[ticket['id']] = thisTicketDict
        requestJSON = simplejson.dumps(requestDict)
	#with open('/requestlog.txt', 'w+') as logFile:
	    #logFile.write(requestJSON)
        updatedResults = requests.post('https://rest.netsuite.com/app/site/hosting/restlet.nl?script=31&deploy=1', data=requestJSON, headers=headers, cookies=cookies)
        ticketsOut = updatedResults.raw

        return ticketsOut
	



def refreshJiraFromNs(request):
    try:
	connectionOptions = {'server':'http://jira.motionsoft.com:8080'}
	jcon = JIRA(connectionOptions, basic_auth = (jira_username, jira_password))
    except:
	msg = {'error':'could not connect to JIRA' }
	return HttpResponse(msg, content_type='application/json') 

    tics = Ticket.objects.exclude(jira_issue__isnull = True).exclude(jira_issue__exact = '')
    for t in tics:
	key = t.netsuite_case_number
	value = t.jira_issue
	if len(value)>13:
	    values = value.split('`')
	    j, created = t.jiraticket_set.get_or_create(jira_issue = values[0])
	    j, created = t.jiraticket_set.get_or_create(jira_issue = values[1])
	else:
	    j, created = t.jiraticket_set.get_or_create(jira_issue = value)

    jtics = JiraTicket.objects.all()
    errorList = []
    for jtic in jtics:
       
	try:
            issue = jcon.issue(jtic.jira_issue)
	    jtic.status = issue.fields.status.name
	    jtic.description = issue.fields.description
	    jtic.assignee = issue.fields.assignee
	    jtic.reporter = issue.fields.reporter
	    jtic.summary = issue.fields.summary
	    jtic.created_date = issue.fields.created
	    jtic.last_viewed = issue.fields.lastViewed
	    jtic.save()
	except:
	    errorList.append(jtic)
	
    jtics = list(JiraTicket.objects.all()) + list(errorList)
    json = serializers.serialize('json',jtics)

    return HttpResponse(json, content_type='application/json')

def updateTrackedTicketStatus(request):
    #connect to Jira     
    try:
	connectionOptions = {'server':'http://jira.motionsoft.com:8080'}
	j = JIRA(connectionOptions, basic_auth = (jira_username, jira_password))
    except:
	msg = 'could not connect to jira'
	return HttpResponse(msg, content_type = 'application/json')

    t = Ticket.objects.all()
    i = 0
    jiraIssues = {}
    while i < len(t):
        ticket = t[i]
	if ticket.jira_issue:
	    key, value = ticket.netsuite_case_number, ticket.jira_issue
	    jiraIssues[key] = value
	i += 1
    
    jiraSearch = {}
    i = 0
    error = 'error'
    for key in jiraIssues:
	issue = str(jiraIssues[key])
	if issue[:4] == 'MOSO':
	    try:
	        jiraIssue = j.issue(issue)
  	        status = jiraIssue.fields.status.name
	        jiraSearch[key] = [issue, status]
		i += 1
	    except(JIRAError):
		thisError = 'error', i
		jiraSearch[thisError] = 'ya dun bunged up',i,'times'
		i += 1
    
    for key in jiraSearch:
	try:
	    thisUpdate = Ticket.objects.get(netsuite_case_number = key)
	    thisUpdate.jira_issue_status = jiraSearch[key][1]
	    thisUpdate.save()
	except:
	    print 'could not find ticket to update with key: ',key

    t = Ticket.objects.all() 
    js = json.dumps(jiraSearch,'json')
    t = serializers.serialize('json',list(t))
    js = js + t
    return HttpResponse(js, content_type='application/json')


@csrf_exempt
def flower(request, parent_id):
    template_name = 'app/flow.html'
    s = Parent.objects.get(id = parent_id)
    all_objects = list(Parent.objects.all()) +  list(Node_1.objects.all()) + list(Node_2.objects.all())+ list(Node_3.objects.all()) + list(Node_4.objects.all())
    data = serializers.serialize('json', all_objects)

    


    return render_to_response(template_name, {'s' : s, 'data' : data}, context_instance = RequestContext(request))
    
def node(request):
    all_objects = list(Parent.objects.all()) +  list(Node_1.objects.all()) + list(Node_2.objects.all())+ list(Node_3.objects.all()) + list(Node_4.objects.all())
    data = serializers.serialize('json', all_objects)
    
    
    return HttpResponse(data, content_type= 'application/json')


#Updates the PDF tab of the content area
def pdfsearch(request):
    if request.method == 'POST':
        raw = request.POST
        url = request.path
        
        #unpack raw json into data variable
        for key in raw:
            data = simplejson.loads(key)

        #unpack data to assign tier, node, and parent variables
        i=0
        while i in range(len(data)):
            if data[i]['name'] == 'tier':
                tier = data[i]['value']
                i += 1
            elif data[i]['name'] == 'node':
                node = data[i]['value']
                i += 1
            elif data[i]['name'] == 'parent':
                parent = data[i]['value']
                i += 1
            else: i += 1

        #identify the model from the selected tier
        if tier == 'node_1':
            model = Node_1
        elif tier == 'node_2':
            model = Node_2
        elif tier == 'node_3':
            model = Node_3
        elif tier == 'node_4':
            model = Node_4
        elif tier == 'node_5':
            model = Node_5
        else: pass
    
        parent = Parent.objects.get(id = parent)

        # from the model, create specific node variable that node's PDF path variable
        node = model.objects.get(node_name__contains = node[:4])
        try :
            path = node.pdf_path #pdf path in model should be the page(s) pertinent to that node
        except: 
            msg = 'No PDF content to display'
            return HttpResponse(msg, mimetype = 'application/text')
    
        #get the actual content of the PDF
        content = 'penis'
        p = file(path, "rb")
        pdf = pyPdf.PdfFileReader(p)
        i=0
        while i in range(pdf.getNumPages()):
            content += pdf.getPage(i).extractText() + "\n"
            i += 1
            
        content = {"pdf" : str(content)}

        return HttpResponse(content, content_type = 'application/json')
    else: return 'fucked'





@csrf_exempt
def node_edit(request):
    #if POST, process
    if request.method == 'POST':
        raw = request.POST
        url = request.path
        
        for key in raw:
            data = simplejson.loads(key)

        

        i=0
        while i in range(len(data)):
            if data[i]['name'] == 'tier':
                tier = data[i]['value']
                i += 1
            elif data[i]['name'] == 'node':
                node = data[i]['value']
                i += 1
            elif data[i]['name'] == 'node-description':
                node_description = data[i]['value']
                i += 1
            elif data[i]['name'] == 'node-details':
                node_details = data[i]['value']
                i += 1
            else: i += 1

        if tier == 'node_1':
            model = Node_1
        elif tier == 'node_2':
            model = Node_2
        elif tier == 'node_3':
            model = Node_3
        elif tier == 'node_4':
            model = Node_4
        elif tier == 'node_5':
            model = Node_5
        else: pass

        this_model = model.objects.get(node_name__contains=node[:4])

        if node:
            this_model.node_name = node
        if node_description:
            this_model.node_description = node_description
        if node_details:
            this_model.details = node_details
        this_model.save()


        data = list(model.objects.all()) + list(msg)
        return HttpResponse(data)
    else:
        form = NodeEdit()
        msg = "GET petitions are not allowed for this view."

    return HttpResponse(msg, form)

@csrf_exempt
def nsjiraapi(request, jiraIssueKey):
    #nsToJira = RequestNStoJIRA()
    msg = 'Reached the Support Homestation server with ', jiraIssueKey
    return HttpResponse(msg)
        




class RequestNStoJIRA(object):
    def __init__(self):
        try:
            self.connectionOptions = {'server':'http://jira.motionsoft.com:8080'}
            self.jira = JIRA(self.connectionOptions, basic_auth = ('mwillis', '8Richard&'))
            self.issue = self.jira(object.jiraKey)
            self.issueStatus = self.issue.fields.status.raw['name']
            return issueStatus
        except:
            return 'false'
            
        









        #REQUEST OBJECT FOR TESTING
        #ns RESTlet protocol and domain = 'https://rest.netsuite.com'
class request(object):  
        def __init__(self):
            self.method = 'POST'
            self.POST = {u'[{"name":"tier","value":"node_2"},{"name":"node","value":"Membership Management"},{"name":"parent","value":"1"}]': [u'']}
            self.path = 'jibbly.html'
