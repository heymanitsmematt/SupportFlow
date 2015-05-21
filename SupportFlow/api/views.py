import requests
import simplejson
from api.NetsuiteUpdate import *
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.views.static import serve
from django.http import HttpResponse
from django.utils.encoding import smart_str
import xlsxwriter
import datetime
from jira.client import JIRA
#from app.views import jira_username, jira_password
import sys
from api.jiraxl import MasterJiraSyncFile
import pdb
from api.NetsuiteUpdate import MassNetsuiteGet

jira_username = 'mwillis'
jira_password = 'Richard*&'

def getTicketsToday(request):
    m = MassNetsuiteGet('all') 
    m.post()
    for ticket in m.tickets:
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
    return HttpResponse(m.tickets)   

#two functions for master reports needed to integrate the two systems
def masterJiraSyncFile(request):
    try:
       

        fl = MasterJiraSyncFile()
        fl.jCon()
        fl.flatten()
        output = fl.construct().seek(0)

        dout = HttpResponse(output.read(), content_type='application/mnd.openxmlformats-officedocument.spreadsheetml.sheet')
        dout['Content-Disposition'] = 'attachment; filename=%s' % smart_str('/dbx/MasterJiraSyncFile.xlsx')
        #dout['X-Sendfile'] = smart_str('/dbx/MasterJiraSyncFile')

    except:
        dout = HttpResponse(sys.exc_info()[0])
    return dout

def masterNetsuiteSyncFile(request):
    pass

@csrf_exempt
def getTicketInfo(request):
    thisfile = open('/SupportFlow/SupportFlow/nsn.txt', 'r+')
    lines = []
    nsCases = []
    dataOut = []
    #lines = [line for line in thisfile]
    for line in thisfile:
	lines.append(line)
    for line in lines:
	length = len(line.split(';'))
	l = line.split(';')[:length-1]
	nsCases.append(l)
    for line in nsCases:
	thisPayload = []
	if line.find(',') == True:
	    owners = []
	    theseCases = line.split(',')
	    for case in theseCases:
	        try:
	            thisCase = Ticket.objects.get(netsuite_case_number = case)
		    owners.append((case, 'ass.to '+thisCase.assigned_to, 'esc.to'+thisCase.escalated_to))
		except:
		    print case
	    dataOut.append(owners)
	else:
	    try:
		thisCase = Ticket.objects.get(netsuite_case_number = line)
		dataOut.append(line, 'ass.to '+thisCase.assigned_to, 'esc.to'+thisCase.escalated_to)
	    except:
		print line
    return HttpResponse(dataOut)


def syncNetsuiteJira(request):
    try:
        m = MassNetsuiteGet('all', True)
        m.post()
        m.updateTrackedStatus()
        m.save()
        response = success
    except:
        response = sys.exc_info()
        pdb.set_trace()

    return HttpResponse(response)

