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
            self.allJiraClosed = self.jCon.search_issues("key in ('MOSO-2856',
                    'MOSO-11238',
                    'MOSO-2236',
                    'MOSO-1311',
                    'MOSO-2051',
                    'MOSO-2923',
                    'MOSO-145 ',
                    'MOSO-11179',
                    'MOSO-2285',
                    'MOSO-11153',
                    'MOSO-11209',
                    'MOSO-2741 ',
                    'MOSO-2841',
                    'MOSO-2440 ',
                    'MOSO-11098',
                    'MOSO-11206',
                    'MOSO-11249',
                    'MOSO-2757',
                    'MOSO-2804',
                    'MOSO-11088',
                    'MOSO-3109',
                    'MOSO-11143 ',
                    'MOSO-3157',
                    'MOSO-10616',
                    'MOSO-11068',
                    'MOSO-10408',
                    'MOSO-10987',
                    'MOSO-3250',
                    'MOSO-3397',
                    'MOSO-10945',
                    'MOSO-11047',
                    'MOSO-8903',
                    'MOSO-10949',
                    'MOSO-3483 ',
                    'MOSO-10934',
                    'MOSO-11118',
                    'MOSO-11071',
                    'MOSO-3492',
                    'MOSO-3471',
                    'MOSO-10923',
                    'MOSO-3494',
                    'MOSO-3546',
                    'MOSO-4390  ',
                    'MOSO-6097',
                    'MOSO-4724',
                    'MOSO-5843',
                    'MOSO-10170',
                    'MOSO-10712',
                    'MOSO-5675',
                    'MOSO-7517 ',
                    'MOSO-5682',
                    'MOSO-5053',
                    'MOSO-5830',
                    'MOSO-10837',
                    'MOSO-10499',
                    'MOSO-10950',
                    'MOSO-10868',
                    'MOSO-5838',
                    'MOSO-6016',
                    'MOSO-5848',
                    'MOSO-6047 ',
                    'MOSO-9805',
                    'MOSO-10858',
                    'MOSO-10265',
                    'MOSO-10516',
                    'MOSO-7793',
                    'MOSO-4993',
                    'MOSO-10777',
                    'MOSO-6097 ',
                    'MOSO-10755',
                    'MOSO-9250',
                    'MOSO-5792',
                    'MOSO-5762',
                    'MOSO-6012',
                    'MOSO-10704',
                    'MOSO-9549',
                    'MOSO-10598',
                    'MOSO-6020',
                    'MOSO-6013',
                    'MOSO-6117',
                    'MOSO-10702',
                    'MOSO-2251',
                    'MOSO-10842',
                    'MOSO-10524',
                    'MOSO-6318',
                    'MOSO-8517',
                    'MOSO-10489',
                    'MOSO-7566',
                    'MOSO-10466',
                    'MOSO-10452',
                    'MOSO-4661',
                    'MOSO-10442',
                    'MOSO-10612',
                    'MOSO-6712 ',
                    'MOSO-10382',
                    'MOSO-8729',
                    'MOSO-6822',
                    'MOSO-4128 ',
                    'MOSO-7388 ',
                    'MOSO-6712',
                    'MOSO-7814',
                    'MOSO-6442',
                    'MOSO-7540',
                    'MOSO-7222',
                    'MOSO-67',
                    'MOSO-10225',
                    'MOSO-9808',
                    'MOSO-9745',
                    'MOSO-6730 ',
                    'MOSO-10368',
                    'MOSO-10279',
                    'MOSO-9098',
                    'MOSO-6778 ',
                    'MOSO-6816',
                    'MOSO-570',
                    'MOSO-7297',
                    'MOSO-10091',
                    'MOSO-10231',
                    'MOSO-10037',
                    'MOSO-2013',
                    'MOSO-6973',
                    'MOSO-4879',
                    'MOSO-6416',
                    'MOSO-9962',
                    'MOSO-9985',
                    'MOSO-10051',
                    'MOSO-9834',
                    'MOSO-9913 ',
                    'MOSO-8027',
                    'MOSO-9394',
                    'MOSO-9861',
                    'MOSO-7375',
                    'MOSO-9856',
                    'MOSO-7320',
                    'MOSO-6319',
                    'MOSO-7360',
                    'MOSO-6515',
                    'MOSO-9835',
                    'MOSO-8407',
                    'MOSO-9721',
                    'MOSO-8439',
                    'MOSO-9743',
                    'MOSO-9867',
                    'MOSO-9695',
                    'MOSO-9643',
                    'MOSO-9626',
                    'MOSO-9677',
                    'MOSO-9753',
                    'MOSO-9700',
                    'MOSO-9625',
                    'MOSO-9702',
                    'MOSO-9585',
                    'MOSO-9584',
                    'MOSO-6748',
                    'MOSO-9678 ',
                    'MOSO-7539',
                    'MOSO-9563',
                    'MOSO-9561',
                    'MOSO-8870',
                    'MOSO-9681',
                    'MOSO-10805',
                    'MOSO-8217',
                    'MOSO-9691',
                    'MOSO-7477',
                    'MOSO-7799',
                    'MOSO-7605',
                    'MOSO-7612',
                    'MOSO-7777',
                    'MOSO-7595',
                    'MOSO-9332',
                    'MOSO-7357',
                    'MOSO-2222',
                    'MOSO-9338',
                    'MOSO-8896',
                    'MOSO-9314',
                    'MOSO-9553',
                    'MOSO-1221',
                    'MOSO-9316',
                    'MOSO-9309',
                    'MOSO-5896',
                    'MOSO-9246',
                    'MOSO-7940',
                    'MOSO-7746',
                    'MOSO-9258',
                    'MOSO-9213 ',
                    'MOSO-7702 ',
                    'MOSO-2512',
                    'MOSO-9244',
                    'MOSO-7627',
                    'MOSO-9130',
                    'MOSO-7742',
                    'MOSO-7783',
                    'MOSO-9268',
                    'MOSO-8196',
                    'MOSO-9058',
                    'MOSO-7747',
                    'MOSO-9131',
                    'MOSO-9025',
                    'MOSO-8082',
                    'MOSO-8030',
                    'MOSO-9074 ',
                    'MOSO-9076',
                    'MOSO-8433',
                    'MOSO-7779',
                    'MOSO-3917',
                    'MOSO-8083',
                    'MOSO-8561',
                    'MOSO-8927',
                    'MOSO-8032',
                    'MOSO-8526',
                    'MOSO-8857',
                    'MOSO-8848',
                    'MOSO-8866',
                    'MOSO-8396',
                    'MOSO-8652',
                    'MOSO-8427',
                    'MOSO-8519',
                    'MOSO-2826 ',
                    'MOSO-9315',
                    'MOSO-8757 ',
                    'MOSO-8799',
                    'MOSO-8716 ',
                    'MOSO-8521',
                    'MOSO-8695',
                    'MOSO-8589',
                    'MOSO-8741',
                    'MOSO-9014',
                    'MOSO-7736',
                    'MOSO-8483',
                    'MOSO-5050',
                    'MOSO-8869',
                    'MOSO-8587',
                    'MOSO-9213',
                    'MOSO-8791',
                    'MOSO-2587',
                    'MOSO-6132',
                    'MOSO-676 ',
                    'MOSO-10262',
                    'MOSO-7604',
                    'MOSO-8567',
                    'MOSO-1811',
                    'MOSO-10790',
                    'MOSO-10597',
                    'MOSO-7050',
                    'MOSO-6742',
                    'MOSO-9189',
                    'MOSO-7316 ',
                    'MOSO-9963',
                    'MOSO-9716',
                    'MOSO-9345',
                    'MOSO-8908',
                    'MOSO-10000',
                    'MOSO-8777')")
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
    
