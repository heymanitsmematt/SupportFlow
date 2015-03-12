from app.models import *
from django_tables2_reports.tables import TableReport 

class TicketTable(TableReport):
    class Meta:
	model = Ticket
	exclude_from_report = ('id') 
	attr = {"class":"paleblue"}

