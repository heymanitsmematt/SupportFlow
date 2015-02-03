from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
import datetime

#employee management models
class EmployeeMaster(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_ext = models.IntegerField(null = True)
    phone_cell = models.IntegerField(null = True)
    mosolegacy = models.CharField(max_length = 5, null=True)
    position = models.CharField(max_length=200, null=True)
    hiredate = models.DateTimeField('date hired', null=True)
    user = models.ForeignKey(User, null=True)
    netsuite_id = models.IntegerField(null = True)


    def get_full_name(self):
        return str(self.first_name) + ' ' + str(self.last_name)

    def __unicode__(self):
        return get_full_name()




class Skills(models.Model):
    description = models.CharField(max_length = 200)
    skill_score = models.FloatField(null = True)

    def high_scorer(self):
        return max(self.skill_score).emp.id

    def __unicode__(self):
        return str(self.description)


#root
class Parent(models.Model):
    parent_name = models.CharField(max_length = 100)
    parent_description = models.CharField(max_length = 200)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)
    
    class Meta:
        unique_together = (('id', 'parent_name'))

    def __unicode__(self):
        return self.parent_name

    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class ParentManager(models.Manager):
    def get_by_natural_key(self, id, parent_name):
        return self.get(id = id, parent_name = parent_name)

#tier-1 sub-nodes
class Node_1(models.Model):
    parent = models.ManyToManyField(Parent)
    node_name = models.CharField(max_length =100)
    node_description = models.CharField(max_length = 200)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)

    class Meta:
        unique_together = (('id', 'node_name'))

    def __unicode__(self):
        return self.node_name
    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class Node_1Manager(models.Manager):
    def get_by_natural_id(self, id, node_name):
        return self.get(id = id, node_name = node_name)

#tier 2 sub-nodes
class Node_2(models.Model):
    parent = models.ManyToManyField(Node_1)
    node_name = models.CharField(max_length = 100)
    node_description = models.CharField(max_length = 100)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)

    
    class Meta:
        unique_together = (('id', 'node_name'))

    def __unicode__(self):
        return self.node_name
    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class Node_2Manager(models.Manager):
    def get_by_natural_key(self, id, node_name):
        return self.get(id=id, node_name=node_name)

 #tier 3 sub-nodes
class Node_3(models.Model):
    parent = models.ManyToManyField(Node_2)
    node_name = models.CharField(max_length = 100)
    node_description = models.CharField(max_length = 100)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)

    
    class Meta:
        unique_together = (('id', 'node_name'))

    def __unicode__(self):
        return self.node_name
    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class Node_3Manager(models.Manager):
    def get_by_natural_key(self, id, node_name):
        return self.get(id=id, node_name=node_name)

 #tier 4 sub-nodes
class Node_4(models.Model):
    parent = models.ManyToManyField(Node_3)
    node_name = models.CharField(max_length = 100)
    node_description = models.CharField(max_length = 100)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)

    
    class Meta:
        unique_together = (('id', 'node_name'))

    def __unicode__(self):
        return self.node_name
    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class Node_4Manager(models.Manager):
    def get_by_natural_key(self, id, node_name):
        return self.get(id=id, node_name=node_name)

 #tier 5 sub-nodes
class Node_5(models.Model):
    parent = models.ManyToManyField(Node_3)
    node_name = models.CharField(max_length = 100)
    node_description = models.CharField(max_length = 100)
    image_folder = models.FilePathField(allow_folders = True, null = True)
    details = models.CharField(max_length = 10000, null = True)
    pdf_path = models.FilePathField(allow_folders = True, null = True)

    
    class Meta:
        unique_together = (('id', 'node_name'))

    def __unicode__(self):
        return self.node_name
    #create function for each node to auto-create content folder upon creation
    def content_folder(self):
        folder_name = self.image_folder
        new_folder = PROJECT_ROOT + "static/app/content/node_content/" +self.parent_name

class Node_5Manager(models.Manager):
    def get_by_natural_key(self, id, node_name):
        return self.get(id=id, node_name=node_name)


#email troller class
class EmailTrollerModel(models.Model):
    last_ticket_received = models.CharField(max_length = 500, null = True)


#ticket class
class Ticket(models.Model):
    netsuite_id = models.IntegerField(null = True)
    customer = models.CharField(max_length = 100, null = True)
    client_id = models.CharField(max_length = 100, null = True)
    caller = models.CharField(max_length = 100, null = True)
    callback_phone = models.CharField(max_length = 100, null = True)
    netsuite_case_number = models.IntegerField(null = True)
    case_type = models.CharField(max_length = 100, null = True)
    case_origin = models.CharField(max_length = 100, null = True)
    product = models.CharField(max_length = 100, null = True)
    module = models.CharField(max_length = 100, null = True)
    short_description = models.CharField(max_length = 5000, null = True)
    status = models.CharField(max_length = 100, null = True)
    severity = models.CharField(max_length = 25, null = True)
    priority = models.CharField(max_length = 20, null = True)
    assigned_to = models.CharField(max_length = 100, null = True)
    escalated_to = models.CharField(max_length = 100, null = True)
    open_date = models.CharField(max_length = 100, null = True)
    opened_by = models.CharField(max_length = 100, null = True)
    first_call_resolution = models.BinaryField(null = True)
    last_updated = models.CharField(max_length = 100, null = True)
    jira_issue = models.CharField(max_length = 100, null = True)
    jira_issue_status = models.CharField(max_length = 100, null = True)
    most_recent_comment = models.CharField(max_length = 10000, null = True)
    
class JiraTicket(models.Model):
    netsuite_key = models.ManyToManyField(Ticket, null=True)
    jira_issue = models.CharField(max_length = 100, null=True)
    status = models.CharField(max_length = 100, null=True)
    description = models.CharField(max_length = 10000, null= True)
    netsuite_case_number_from_jira = models.CharField(max_length = 100, null = True)
    assignee = models.CharField(max_length = 50, null = True)
    reporter = models.CharField(max_length = 50, null = True)
    summary = models.CharField(max_length = 10000, null = True)
    created_date = models.CharField(max_length = 100, null = True)
    last_viewed = models.CharField(max_length = 100, null = True) 










