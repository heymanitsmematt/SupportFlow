import requests
from api.NetsuiteUpdate import *
from app.models import *
import xlsxwriter
import datetime
from jira.client import JIRA
from app.views import jira_username, jira_password
import sys


class MasterNSSyncFile():
    def __init__(self, search='all'):
        self.specialTics = ['98974',
                '100772',
                '100901',
                '101432',
                '101652',
                '101941',
                '101975',
                '101975',
                '102119',
                '102124',
                '102320',
                '102383',
                '103630',
                '103905',
                '104117',
                '105052',
                '105503',
                '105638',
                '105716',
                '105933',
                '105950',
                '105950',
                '106025',
                '106064',
                '106151',
                '106226',
                '106227',
                '106307',
                '106372',
                '106386',
                '106498',
                '106529',
                '106533',
                '106560',
                '106563',
                '106584',
                '106597',
                '106627',
                '106727',
                '106746',
                '106846',
                '106873',
                '106916',
                '106927',
                '106931',
                '106933',
                '106938',
                '106971',
                '106977',
                '106991',
                '106996',
        '106996',
        '107064',
        '107106',
        '107106',
        '107112',
        '107139',
        '107170',
        '107184',
        '107186',
        '107199',
        '107212',
        '107221',
        '107276',
        '107726',
        '107727',
        '107755',
        '107841',
        '107846',
        '108010',
        '108023',
        '108028',
        '108028',
        '108033',
        '108038',
        '108084',
        '108105',
        '108105',
        '108174',
        '108174',
        '108182',
        '108228',
        '108232',
        '108232',
        '108326',
        '108339',
        '108405',
        '108463',
        '108474',
        '108478',
        '108538',
        '108568',
        '108576',
        '108699',
        '108700',
        '108724',
        '108728',
        '108949',
        '108992',
        '109122',
        '109153',
        '109210',
        '109216',
        '109268',
        '109344',
        '109442',
        '109445',
        '109481',
        '109555',
        '109559',
        '109565',
        '109574',
        '109633',
        '109717',
        '109717',
        '109740',
        '109801',
        '109876',
        '109877',
        '109897',
        '110111',
        '110115',
        '110479',
        '110487',
        '110494',
        '110563',
        '110612',
        '110634',
        '110720',
        '110819',
        '110819',
        '110888',
        '111010',
        '111041',
        '111069',
        '111069',
        '111132',
        '111547',
        '111750',
        '111767',
        '111782',
        '111799',
        '111835',
        '111911',
        '111922',
        '111962',
        '111977',
        '112040',
        '112225',
        '112245',
        '112451',
        '112521',
        '112733']
        self.nsTrackedDict = {}
        self.massNs = MassNetsuiteGet(search)
        self.massNs.post()

        self.jCon = JIRA({'server':'http://jira.motionsoft.com:8080'}, basic_auth = (jira_username, jira_password))
        
        #build list of keys to search by to build big dict of data for table and filter to only tracked
        self.nsKeys = 'status,name product,name casenumber title startdate company,name message assigned,name createddate'.split()
        for tic in self.massNs.tickets:
            keyDict = {}
            for searchKey in self.nsKeys:
                if searchKey.find(',')!= -1:
                    try:
                        qstr = "tic['columns']['%s']['name']" % searchKey.split(',')[0]
                        val = eval(qstr)
                        keyDict[searchKey.split(',')[0]] = val
                    except:
                        keyDict[searchKey.split(',')[0]] = '%s not found' % searchKey.split(',')[0]
                else:
                    qstr = "tic['columns']['%s']" % searchKey
                    try:
                        qstr = "tic['columns']['%s']" % searchKey
                        val = eval(qstr)
                    except:
                        val = ''
                    keyDict[searchKey] = val
            try:
                val = tic['columns']['custeventsn_case_number']
                #print val
                keyDict['jiraIssues'] = val
            except:
                val = ''
                keyDict['jiraIssues'] = val
            self.nsTrackedDict[tic['columns']['casenumber']] = keyDict

    def flatten(self):
        #if ohere are multiple jira tickets linked, create an entr in the master dict for each of tose statuses. else grab the status of the lone issue and get it's details into the dict as well. 

        jiraColumns = 'From Priority Key Summary Status Resolution Updated Assignee Reporter FixVersion Component Created Resolved Customer Sprint Netsuite#(s)(fromjira)'.split()
        jiraSearchKeys = 'fields.issuetype.name fields.priority.name key fields.summary fields.status.name fields.resolution.name fields.updated fields.assignee.displayName fields.reporter.displayName fields.fixVersions fields.components fields.created fields.resolutiondate fields.customfield_10082 fields.customfield_10070 fields.customfield_10080'.split()

        for tic in self.nsTrackedDict:
            tick = self.nsTrackedDict[tic]
            issuesDict = {}
            if tick['jiraIssues'].find(',') != -1:
                issues = tick['jiraIssues'].split(',')
                for issue in issues:
                    thisIssue = {}
                    try:
                        i = self.jCon.issue(issue.strip())
                        c = 0                       
                        while c<len(jiraColumns):
                            try:
                                thisKey = jiraColumns[c]
                                str = 'i.%s' % jiraSearchKeys[c]
                                thisVal = eval(str)
                                thisIssue[thisKey] = thisVal
                                c += 1
                            except:
                                #5 = Resolution
                                if c == 5:
                                    thisIssue[thisKey] = 'Unresolved'
                                    c += 1
                                #7 = Assigned
                                elif c == 7:
                                    thisIssue[thisKey] = 'Unassigned'
                                    c += 1
                                elif c == 13:
                                    thisIssue[thisKey] = 'No Sprint'
                                    c += 1
                                # anything else is boo boo
                                else:
                                    thisIssue[thisKey] = str(c) 
                                    print 'e1 in mult issues', tic, issue, jiraSearchKeys[c]
                                    c += 1
                    except:
                        #thisIssue[thisKey] = tick['jiraIssues']
                        print 'e1', tic, issue, sys.exc_info()                        
                    issuesDict[issue] = thisIssue 
            else:
                issue = tick['jiraIssues']
                thisIssue = {}
                issue = issue.strip()
                try:
                    i = self.jCon.issue(issue)
                except:
                    print 'no issue for',tic, issue
                    #MOSO-11510 IS NO ISSUE DEAD CASE FOR EMPTY TESTING
                    i = self.jCon.issue('MOSO-11510')
                c = 0
                try:
                    c=0
                    while c < len(jiraColumns):
                        try:
                            #if issue is no-issue filler - blank values
                            thisKey = jiraColumns[c]
                            qstr = 'i.%s' % jiraSearchKeys[c]
                            thisVal = eval(qstr)
                            thisIssue[thisKey] = thisVal
                            if i.key == 'MOSO-11510':
                                pass
                                #thisIssue[thisKey] = ''
                            c += 1
                        except:
                            # resolution
                            if c == 5:
                                thisIssue[thisKey] = 'Unresolved'
                                c += 1
                            # assigned to
                            elif c == 7:
                                thisIssue[thisKey] = 'Unassigned'
                                c += 1
                            # 13 = sprint
                            elif c == 13:
                                thisIssue[thisKey] = 'No Sprint'
                                c += 1
                            # boo boo
                            else:
                                thisKey = jiraColumns[c]
                                thisIssue[thisKey] = 'e2'
                                print 'error IN the c loop, found jira issue, error inside single object', issue,c, sys.exc_info()[0]
                                c += 1
                    try:
                        issuesDict[issue] = thisIssue
                    except:
                        print 'error writing issuesDict', issue, sys.exc_info()[0]
                except:
                    print "error in high loop?", tic, issue, sys.exc_info()[0] 
            tick['jiraIssues'] = issuesDict
         

    def construct(self):
        f = '/root/Dropbox/MasterNSSyncFile_%s.xlsx' % datetime.date.today()
        self.book = xlsxwriter.Workbook(f)
        self.sheet = self.book.add_worksheet()
        bold = self.book.add_format({'bold':True})
        blue = self.book.add_format({'bg_color':'#95B3D7'})
        
        headers = 'casenumber company status assigned title createddate startdate jiraIssues Netsuite#(s)(fromjira) Key From Status Resolved Sprint FixVersion Component Customer Created Updated Reporter Assignee Summary'.split()

        graphemes = 'A B C D E F G H I J K L M N O P Q R S T U V W Q X Y Z'.split()
        
        i = 0
        while i<len(headers):
            targetCell = graphemes[i] + str(1)
            self.sheet.write(targetCell, headers[i], bold)
            i += 1

        counter = 0
        for ticket in self.nsTrackedDict:
            counter += len(self.nsTrackedDict[ticket]['jiraIssues'])

        r = 2
        #dics cannot be sorted. select all keys into a list, sort it, and write from there
        tics = [t for t in self.nsTrackedDict]
        tics.sort()
        for tic in tics:
            if tic in self.specialTics:
                c = 0
                t = self.nsTrackedDict[tic]
                mergeLen = len(t['jiraIssues'])
                #print 'mergeLen = %s' % mergeLen
                #write out ns data in a merged cell the height of the length of its jiraIssues
                while c<8:
                    targetNSCell = graphemes[c] + str(r)
                    if c<7:
                        qstr = "t['%s']" % headers[c]
                        data = eval(qstr)
                    elif c == 8:
                        try:
                            data = str(t['jiraIssues'].keys())
                        except:
                            data = [t['jiraIssues']]

                    mergeRange = graphemes[c] + str(r) + ":" + graphemes[c] + str(r+(mergeLen-1)) 
                    if mergeLen > 1:
                        try:
                            self.sheet.merge_range(mergeRange, data)
                        except:
                            if headers[c] == 'jiraIssues':
                                self.sheet.merge_range(mergeRange, str(data))
                            #print mergeRange
                            else:
                                print 'exc1 writing ticket with ', c, tic, sys.exc_info()[0]
                                pass
                    else:
                        try:
                            self.sheet.write(targetNSCell, data)
                        except:
                            #print targetNSCell
                            print 'exc2 writing ticket with ', headers[c], tic, sys.exc_info()[0]
                            pass
                    # for each issue, write out the jira ticket data
                    c += 1
                while c in range(8,len(headers)):
                    rNow = r
                    for issue in t['jiraIssues']:
                        targetCell = graphemes[c] + str(rNow)
                        try:
                            isu = t['jiraIssues'][issue]
                            qstr = "isu['%s']" % headers[c]
                            data = eval(qstr)
                            #12 = Sprint 
                            if c == 13:
                                dat = ''
                                for sprint in data:
                                    stub = sprint[sprint.find('name')+5:]
                                    stub = stub[:stub.find(',')]
                                    dat += stub
                                data = str(dat)
                            #13 = FixVersion, 14=Component
                            elif c in (14,15):
                                dat = ''
                                for fv in data:
                                    dat += fv.name
                                data = dat
                            #15 = Customer
                            elif c == 16:
                                dat = ''
                                for fv in data:
                                    dat += fv.value
                                data = str(dat)
                        except:
                            data = 'None'
                            #print 'exc3 writin ticket with', headers[c], tic, issue, sys.exc_info()[0]
                        try:
                            self.sheet.write(targetCell, str(data))
                        except:
                            print 'error writing issue cell wile rNow=', rNow, 'and c=',c, sys.exc_info()[0]
                            pass
                        rNow += 1
                    c += 1
                r += mergeLen

            self.book.close()
                        
nsSearch = raw_input("Search 'all' or 'WOW'? ")
m = MasterNSSyncFile(nsSearch)
m.flatten()
m.construct()
print 'go move dat file you handsome devil you!!'


