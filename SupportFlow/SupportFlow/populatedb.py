from app.models import *

#build EmployeeMaster values
firstnames = ['Matthew', 'Brandon', 'Ahmad', 'Kevin','Sean']
lastnames = ['Willis', 'Duduk', 'Abdel', 'Hunt','Cartwright']
emails = ['mwillis@motionsoft.net', 'bduduk@motionsoft.net','aabdel@motionsoft.ent','khunt@motionsfot.net','scartwright@motionsoft.net']
ml = ['ml','l','ml','l','m']

#populate EmployeeMaster model
i = 0
while i < len(firstnames) :
    EmployeeMaster.objects.create(first_name = firstnames[i], last_name = lastnames[i], email = emails[i], mosolegacy=ml[i])
    i += 1

#build skills list
skills = ['Python Developer','SQL Competent','Eclub Knowledge','Cx Knowledge','MOSO Knowledge','Sharepoint Developer','None']

#populate Skills model
i = 0
while i < len(skills):
    thisskill = Skills()
    thisskill.description = skills[i]
    thisskill.save()
    i += 1

empskills = []
empskills.append((1,2,3,4,5))
empskills.append((3,4,6))
empskills.append((3,5,4,6))
empskills.append((2,3,4))
empskills.append((4,7))

for emp in EmployeeMaster.objects.all():
    try:
        for n in empskills[emp.id-1]:
          emp.skills_set.add(n)
    except: pass




#populate topics list
topics = ['Support','Job Request','Development Issue']
descriptions = ['A general support task','An implimentation or special job','A development issue']

#populate WorkflowTopic
i = 0
while i<len(topics):
    WorkflowTopic.objects.create(topic = topics[i], description = descriptions[i])
    i += 1

#connect Software with workflowtopics
conexion = SoftwareMaster.objects.get(software_name__contains = 'Conexion')

for n in range(1,len(topics)+1):
    conexion.workflowtopic_set.add(n)



#populate WorkflowSubjects list
subjects = ['Password Reset', 'Account Unlock', 'Receipt Printer Issue']
descriptions = ['Reset the password for a verified Conexion client','Unlock the account for a verified Conexion User','The receipt printer is not printing receipts']

#populate WorkflowSubject model
i = 0
while i<len(subjects):
    thissubject = WorkflowSubject()
    thissubject.subject = subjects[i]
    thissubject.description = descriptions[i]
    thissubject.save()
    i += 1

#link topics with related subjects
support_subjects = []
for subj in WorkflowSubject.objects.all():
    support_subjects.append(subj.id)
    ##link 
support_topic = WorkflowTopic.objects.get(topic__contains = 'support')
for n in support_subjects:
    support_topic.workflowsubject_set.add(n)

# populate troubleshooting master with printer issues
print_hware_topics = ['Map Printer as LPT','COM port error in POS','Receipts from wrong printer']
print_hware_descripts = ['Steps to map a serial or USB printer as an LPT printer in the windows environement','The user is receiving a COM port error in POS when attempting to print','The receipts are either printing from the document printer or the wrong printer']

i=0
while i < len(print_hware_topics):
    newhware = HardwareTroubleshootMast()
    newhware.troubleshoot_topic = print_hware_topics[i]
    newhware.troubleshoot_description = print_hware_descripts[i]
    newhware.save() 
    i += 1




#build software list
softwares = ['Conexion','Eclub','MOSO']
software_descriptions = ['Conexion Hosted', 'Eclub Deployed', 'MOSO Cloud']
versions = ['6.1','3.68','2.01']

#populate SoftwareMaster model
i = 0
while i < len(softwares):
    new_software = SoftwareMaster()
    new_software.software_name = softwares[i]
    new_software.software_description = software_descriptions[i]
    new_software.version = versions[i]
    new_software.save()
    i += 1

#build modules list
modules = ['Membership Management','Check In', 'Point of Sale','Agreement Writer','Account Link']
module_descriptions = ['Main module for member management and billing','Main module for check in and usage reporting','Main module for Pont of Sale tenders and related reports','Main module for initiating new contracts or renewing contracts for existing members','Module for exporting financial information to third party applications such as Quickbooks']

#populate modules model
i=0
while i < len(modules):
    new_module = Modules()
    new_module.module_name = modules[i]
    new_module.module_description = module_descriptions[i]
    new_module.save()
    i += 1

#create conexion software object
conexion = SoftwareMaster.objects.get(software_name__contains = 'conexion')

#populate conexion.modules_set
i=0
while i < Modules.objects.count():
    conexion.modules_set.add(i)
    i += 1

#create membership management object
membership_management = Modules.objects.get(module_name__contains = 'membership')

#build reports lists
reports = ['Billing Module Reports', 'Membership Lists','Special Reports','Silver Sneakers Report']
report_descriptions = ['Billing and Payments reports run from the billing ultility','Member reports filtered by criteria and report style','Custom reports','A how-to in customizing conexion to collect Silver Sneakers data and report on that data']

#populate Reports model
i=0
while i<len(reports):
    new_report = Reports()
    new_report.report_name = reports[i]
    new_report.report_description = report_descriptions[i]
    new_report.save()
    i += 1

#link membership_management object with reports
i = 0
while i < Reports.objects.count():
     membership_management.reports_set.add(i)
     i += 1











 #add conexion to parents list
