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

class MasterJiraSyncFile:
    def __init__(self):
        self.errs = list()
	self.errs1 = ''
        #self.output = output
    def jCon(self):
        try:
            #initial instantion of book and page object
            f = '/dbx/MasterJiraSyncFile.xlsx'
            self.book = xlsxwriter.Workbook(f)
            self.page = self.book.add_worksheet()

            #jira connection object instantiation and allJiraClosed tuple creation. Queryset limited to 50 results unless max_results param specified
            jiraConOpts = {'server':'http://jira.motionsoft.com:8080'}
            self.jCon = JIRA(jiraConOpts, basic_auth = (jira_username, jira_password))
            self.allJiraClosed = self.jCon.search_issues('status=Closed and "Netsuite #" is not empty', maxResults=1000)
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
            graphemes = 'A B C D E F G H I J K L M N O P Q R S T U V W Q X Y Z'.split()

            #headers for the table to be used in construction iterator
            headers = 'From Priority Key ReferredInMultipleNetsuiteTickets Enhancement Summary Status Resolution Updated Assignee Reporter FixVersion(s) Components Created Resolved Customer Sprint Netsuite#(fromjira) Case#(fromns) OpenedBy OpenDate NetsuiteStatus NetsuiteAssignee'.split()
            #note: fixVersion, customfield_10082 return a list
            #note: sprint = customfield_10070, which returns a list of strings.
            #note: netsuite # = customfield_10080, returns a string (hopefully sep by commas)
            #these will be used in an iterator to run queries against jiraresults in exec()
            seekers = 'fields.issuetype.name fields.priority.name key MULTNSTICS ENHANCEMENT fields.summary fields.status.name fields.resolution.name fields.updated fields.assignee.displayName fields.reporter.displayName fields.fixVersions fields.components fields.created fields.resolutiondate fields.customfield_10082 fields.customfield_10070 fields.customfield_10080 CASE OPENEDBY OPENDATE NSSTATUS NSASSIGNEE'.split()

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
    
