import requests
import simplejson
from api.NetsuiteUpdate import *
from app.models import *
from django.views.decorators.csrf import csrf_exempt
import sys

def getTicketsToday(request):
    m = MassNetsuiteGet() 
    m.post()
    for ticket in m.tickets:
	thisTicket = Ticket.objects.get_or_create(netsuite_id = ticket['id'])[0]
	thisTicket.customer = ticket['columns']['company']['name']
	thisTicket.caller = ticket['columns']['caller']['name']
	thisTicket.netsuite_case_number = ticket['columns']['casenumber']
	thisTicket.case_type = ticket['columns']['category']['name']
	thisTicket.status = ticket['columns']['status']['name']
	thisTicket.assigned_to = ticket['columns']['assigned']['name']
	thisTicket.save()
    return HttpRequest('done')   

class Tickets:
    def __init__(self):
    self.filein = open('/SupportFlow/SupportFlow/nsn.txt', 'r+')
    self.fileout = open('/SupportFlow/SupportFlow/nsnout.txt', 'rw')
	
def owners():
    for line in filein:
	line = line[:line.find(';')]
	if line.find(',') != -1:
	    try:
		payload = [] 
	        cases = line.split(',')
		for case in cases:
		    try:
		        thisTicket = Ticket.objects.all().filter(netsuite_case_number = case)[0]
			payload = payload, thisTicket.opened_by
		    except:
			print 'err on multi ticket with ', case
		strout = strout + payload
	    except:
		print 'err splitting multi with ',cases
	else:
	    try:
	        thisTicket = Ticket.objects.all().filter(netsuite_case_number = line)[0]
	        string = thisTicket.opened_by 
		strout = strout + string
	    except:
	        print 'failed on single with ',line
    fileout.write(strout)

@csrf_exempt
def getTicketInfo():
    thisfile = open('/SupportFlow/SupportFlow/nsn.txt', 'r+')
    lines = []
    nsCases = []
    dataOut = []
    lines = [line for line in thisfile]
    lines.pop()
    for line in lines:
	length = len(line.split(';'))
	l = line.split(';')[:length-1]
	nsCases.append(l)
    for line in nsCases:
	thisPayload = []
	ln = line[0]
	if ln.find(',') != -1:
	    owners = []
	    theseCases = ln.split(',')
	    for case in theseCases:
	        try:
	            thisCase = Ticket.objects.all().filter(netsuite_case_number = case)[0]
		    owners.append((case, thisCase.opened_by))
		    #print 'multi success with ', case
		except: pass
		    #print case, sys.exc_info()[0]
	    dataOut.append(owners)
	else:
	    try:
		ln = line[0]
		thisCase = Ticket.objects.all.filter(netsuite_case_number = ln)[0]
		dataOut.append((ln, thisCase.opened_by))
		#print 'single success with ', ln
	    except: pass
		#print ln, sys.exc_info()[0]
    strout = ''

    return dataOut

