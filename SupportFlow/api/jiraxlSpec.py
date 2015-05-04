import requests
import simplejson
from api.NetsuiteUpdate import *
from app.models import *
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import xlsxwriter
import datetime
from jira.client import JIRA
from app.views import jira_username, jira_password
import sys
import datetime

class MasterJiraSyncFile:
    def __init__(self):
        self.errs = list()
	self.errs1 = ''
        #self.output = output
    def jCon(self):
        try:
            #initial instantion of book and page object
            f = '/root/Dropbox/MasterJiraSyncFile_%s.xlsx' % datetime.date.today()
            self.book = xlsxwriter.Workbook(f)
            self.page = self.book.add_worksheet()

            #jira connection object instantiation and allJiraClosed tuple creation. Queryset limited to 50 results unless max_results param specified
            jiraConOpts = {'server':'http://jira.motionsoft.com:8080'}
            self.jCon = JIRA(jiraConOpts, basic_auth = (jira_username, jira_password))
            self.allJiraClosed = self.jCon.search_issues("key in ('MOSO-6733',\
                    'MOSO-5792',\
                    'MOSO-9122',\
                    'MOSO-9059',\
                    'MOSO-10091',\
                    'MOSO-7627',\
                    'MOSO-7701',\
                    'MOSO-7939',\
                    'MOSO-7136',\
                    'MOSO-5998',\
                    'MOSO-5982',\
                    'MOSO-9628',\
                    'MOSO-8562',\
                    'MOSO-9411',\
                    'MOSO-6748',\
                    'MOSO-5530',\
                    'MOSO-7785',\
                    'MOSO-10945',\
                    'MOSO-10898',\
                    'MOSO-10850',\
                    'MOSO-11319',\
                    'MOSO-7702',\
                    'MOSO-7757',\
                    'MOSO-6749',\
                    'MOSO-5682',\
                    'MOSO-7814',\
                    'MOSO-1473',\
                    'MOSO-11238',\
                    'MOSO-6712',\
                    'MOSO-7517',\
                    'MOSO-3492',\
                    'MOSO-2741',\
                    'MOSO-2013',\
                    'MOSO-9296',\
                    'MOSO-7137',\
                    'MOSO-8505',\
                    'MOSO-8310',\
                    'MOSO-8142',\
                    'MOSO-9101',\
                    'MOSO-707',\
                    'MOSO-7731',\
                    'MOSO-9174',\
                    'MOSO-8798',\
                    'MOSO-7721',\
                    'MOSO-8568',\
                    'MOSO-9437',\
                    'MOSO-9399',\
                    'MOSO-8908',\
                    'MOSO-9414',\
                    'MOSO-9329',\
                    'MOSO-7547',\
                    'MOSO-8634',\
                    'MOSO-7921',\
                    'MOSO-11094',\
                    'MOSO-10937',\
                    'MOSO-10743',\
                    'MOSO-7027',\
                    'MOSO-6917',\
                    'MOSO-6777',\
                    'MOSO-6751',\
                    'MOSO-6561',\
                    'MOSO-6416',\
                    'MOSO-6323',\
                    'MOSO-6079',\
                    'MOSO-5896',\
                    'MOSO-5760',\
                    'MOSO-4879',\
                    'MOSO-2443',\
                    'MOSO-8757',\
                    'MOSO-9678',\
                    'MOSO-9258',\
                    'MOSO-9913',\
                    'MOSO-8695',\
                    'MOSO-8443',\
                    'MOSO-8034',\
                    'MOSO-8442',\
                    'MOSO-7134',\
                    'MOSO-9584',\
                    'MOSO-9213',\
                    'MOSO-7783',\
                    'MOSO-11118',\
                    'MOSO-10564',\
                    'MOSO-10373',\
                    'MOSO-6390',\
                    'MOSO-4390',\
                    'MOSO-2826',\
                    'MOSO-2251',\
                    'MOSO-9058',\
                    'MOSO-10906',\
                    'MOSO-8927',\
                    'MOSO-3494',\
                    'MOSO-6515',\
                    'MOSO-7799',\
                    'MOSO-8652',\
                    'MOSO-6730',\
                    'MOSO-6442',\
                    'MOSO-7736',\
                    'MOSO-8857',\
                    'MOSO-8729',\
                    'MOSO-9681',\
                    'MOSO-6742',\
                    'MOSO-5873',\
                    'MOSO-5848',\
                    'MOSO-4128',\
                    'MOSO-2587')")
            self.nsFromJiraDict = {k.key:k.fields.customfield_10080 for k in self.allJiraClosed}
            nsFromJiraDict = self.nsFromJiraDict
        except: pass    
        
    def flatten(self):
        #build final list of jira issues with flattened netsuite tickets
        self.problemos = list()
        for issue in self.nsFromJiraDict:
            try:
                tickets = self.nsFromJiraDict[issue].split(',')
                for tic in tickets:
                    try:
                        t = Ticket.objects.all().filter(netsuite_case_number=tic)[0]
                        self.problemos.append((issue,'Y','', t.netsuite_case_number, t.opened_by, t.open_date, t.status, t.assigned_to))
                    except: pass
            except:
                try:
                    t = Ticket.objects.all().filter(netsuite_case_number=self.nsFromJiraDict[issue])[0]
                    self.problemos.append((issue, 'N','',t.opened_by, t.open_date, t.status, t.assigned_to))
                except:
                    self.errs1 += 'problemoserr' + str(sys.exc_info()[0])

    def construct(self):
        try:
            #letters in a list for column organization
            graphemes = 'A B C D E F G H I J K L M N O P Q R S T U V W Q X Y Z'
            graphemes = graphemes.split()

            #headers for the table to be used in construction iterator
            headers = 'From Priority Key ReferredInMultipleNetsuiteTickets Enhancement Summary Status Resolution Updated Assignee Reporter FixVersion(s) Components Created Resolved Customer Sprint Netsuite#(fromjira) Case#(fromns) OpenedBy OpenDate NetsuiteStatus NetsuiteAssignee'
            #note: fixVersion, customfield_10082 return a list
            #note: sprint = customfield_10070, which returns a list of strings.
            #note: netsuite # = customfield_10080, returns a string (hopefully sep by commas)
            #these will be used in an iterator to run queries against jiraresults in exec()
            seekers = 'fields.issuetype.name fields.priority.name key MULTNSTICS ENHANCEMENT fields.summary fields.status.name fields.resolution.name fields.updated fields.assignee.displayName fields.reporter.displayName fields.fixVersions fields.components fields.created fields.resolutiondate fields.customfield_10082 fields.customfield_10070 fields.customfield_10080 CASE OPENEDBY OPENDATE NSSTATUS NSASSIGNEE'
            headers = headers.split()
            seekers = seekers.split()

            #begin document creation

            #format variables
            bold = self.book.add_format({'bold':True})
            hyperlink = 'http://jira.motionsoft.com:8080/browse/%s'
            linkFormat = self.book.add_format({'font_color':'blue', 'underline':1})
            tip = 'click to view jira ticket'

            #begin header construction
            i=0
            while i<len(headers):
                cellFocus = graphemes[i] + '1'
                self.page.write(cellFocus, headers[i], bold)
                i += 1

            issueStub = "issue = [j for j in self.allJiraClosed if j.key=='%s']"
            dataStub = "data = issue[0].%s"


            try:
                r = 2
                i = 0
                while i<len(self.problemos):
                    c = 0
                    ns = 1
                    issueQuery = issueStub % self.problemos[i][0]
                    exec(issueQuery)
                    while c<len(seekers):
                        try:
                            targetCell = graphemes[c] + str(r)
                            dataQuery = dataStub % seekers[c]
                            try:
                                exec(dataQuery)
                            except:
                                if seekers[c] in 'MULTNSTICS ENHANCEMENT OPENEDBY OPENDATE NSSTATUS NSASSIGNEE CASE'.split():
                                    data = self.problemos[i][ns]
                                    ns += 1
                                else:
                                    data = 'err with ' + seekers[c] +' and '+self.problemos[i][0]
                            if seekers[c] in 'fields.fixVersions fields.components'.split():
                                dat = ''
                                for d in data:
                                    dat += d.name
                                data = dat
                            if seekers[c] == 'fields.customfield_10082':
                                dat = ''
                                for d in data:
                                    dat += d.value
                                data = dat
                            if seekers[c] == 'fields.customfield_10070':
                                dat = ''
                                try:
                                    for d in data:
                                        bit = d[d.find('name')+5:]
                                        bit = bit[:bit.find(',')]
                                        dat += str(bit)
                                except:
                                    dat = '' 
                                data = dat
                            if seekers[c] == 'key':
                                self.page.write(targetCell, hyperlink % data, linkFormat, data, tip)
                            else:    
                                self.page.write(targetCell, data)
                        except:
                            self.errs.append(sys.exc_info())
                        c += 1
                    r += 1
                    i += 1
                self.book.close()
            except:
                err = sys.exc_info()
                self.errs.append(err)
                #return HttpResponse(err)
        except:
            err = sys.exc_info()
            self.errs.append(err)
            #return HttpResponse(err)

        return self.errs 
m = MasterJiraSyncFile()
print 'generating file as of %s' % datetime.date.today()
m.jCon()
print 'organizing data'
m.flatten()
print 'constructing file'
m.construct()
print 'file constructed successfully!!'

