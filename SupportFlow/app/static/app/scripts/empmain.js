


$(document).ready(function() {
    emp = new Employee();
    emp.onLoad();
    ticketData = new Object;
    emp.updateTrackedTicketStatus();
    ticketData.nsTicketsWithJiraIssues = function() {
					    escs = [];
					    $(ticketData.raw).each(function() {
					        if (this.fields.jira_issue){
						    escs.push(this);
						};
					    });
					    return escs;
					};
    
    function Employee() {
        self.this;
	self.onLoad = function(){
            $('#masterJiraSyncFile').click(function() {
                $.get('/masterJiraSyncFile', function (data){
                    alert(data)
                });
            });
			$('#getTicketsToday').click(function(){
			    $.get('/getTicketsToday', function (data){
				alert(data);
			    });
			});
			widgets = new Array();
			widgetButtons = new Array();
			widgetButtons[0] = $('#jira_widget_button')
			widgetButtons[1] = $('#active_widget_button')
			widgetButtons[2] = $('#tickets_today_widget_button')
			widgets[0] = $('#tracked_ticket_table')
			widgets[1] = $('#open_ticket_table')
			widgets[2] = $('#tickets_today_table')
			$(widgets).each(function() {
			    $(this).hide()
			});
			$(widgetButtons).each(function() {
			    $(this).on('click', function() {
			        switch($(this).text()) {
				    case widgetButtons[0].text():
					tgt = 0
					break
				    case widgetButtons[1].text():
					tgt = 1
					break
				    case widgetButtons[2].text():
					tgt = 2
					break
				}
				tgtw = widgets[tgt]
				/*
				widgets.pop(tgt)
				$(widgets).each(function() {
				    $(this).hide()
				})
				*/
				$(tgtw).toggle('slow');
				widgets[tgt] = tgtw
			    });		
		        })
		    };
	
	self.rawData = [];
	self.updateTrackedTicketStatus = function() {
		        $.getJSON('/updateTrackedTickets/', function(data) {
			    ticketData.trackedTicketStatus = data;
			    var i = 1, str = ''; escNSCaseNumbers = [];
     			    try{
				delete data.error;
			    }
			    catch(e){
  				conesole.log(e);
			    };
			    for (nsCase in data) {
				escNSCaseNumbers.push(nsCase);	
				try{
				    for (var j=0; j<ticketData.raw.length; j++){
				    	thisTicket = ticketData.raw[i];
					if (data[nsCase][0] == thisTicket.fields.jira_issue){
					    thisTicket.jira_issue_status = data[nsCase][1];
					    console.log('match!: ', ticketData.raw[i], nsCase);
					    j++;
					}
					else{
					    j++;
				    	};
				    ;}
				    str += "<tr>";
				    str += "<td id='"+i+"'> NetSuite Case Number: "+ nsCase+"</td>";
				    str += "<td id='"+i+"'> Linked Jira Issue: " + data[nsCase][0] + "</td>";
				    str += "<td id='"+i+"'> Jira Status: " + data[nsCase][1] + "</td>";
				    str += "</tr>";
				    i ++; 
			        }
				catch(e) {
				    console.log(e);
			    	};
			    };
			    $('#jira_status_table').prepend(str);
			    return data;
			}); 
		    };
        self.JSON = $.getJSON('/ticket/', function(data) {
			ticketData.raw = data
		        return data;
    		    });
        self.recentTickets = function(datain) {
				    var tickets = datain.responseJSON, str = '';
				    for (var i=0; i<10; i++){
		        	        ticket = tickets[i];
			    	        str += '<tr>';
					str += '<td>Netsuite Case Number: ' + ticket.fields.netsuite_case_number;+ "</td>";
					str += "<td>NetsuiteJiraIssue: " + ticket.fields.jira_issue + "</td>";
					str += "</tr>";
			            };    
				$('#ticket_outline_table').prepend(str);
			    };
	self.functions = new Object;
	self.functions.findTicketByNSCase = function(arrayIn) {
			    			$(arrayIn).each(function(){
						    for (var i=1; i<ticketData.raw.length; i++){
						        thisTicket = ticketData.raw[i];
							if (thisTicket.fields.netsuite_case_number == this){
							    return thisTicket;
							}
							else {
							    i++
							};
						    };
						});
			    		};
	self.functions.getTicketsToday = function() {
					    $.get('/getTicketsToday', function(data) {
					        return data;
					    });
					};
	self.widgets = new Object;
	self.widgets.nsJiraQuickView = function(qvData){
					    str = "";
					    i=1;
					    for (var j=0;j< qvData().length; j++) {
						tick = qvData()[j];
						str += "<tr id='jira_netsuite_quickview_row"+i+"'>";
					        str += "<td id='quickview_row_"+i+"_ns_case_number'>Netsuite Case Number: " + tick.fields.netsuite_case_number + "</td>";
						str += "<td id='quickview_row_"+i+"_status'>Netsuite Case Status: " + tick.fields.status + "</td>";
						str += "<td id='quickview_row_"+i+"_jira_issue'>Jira Issue: " + tick.fields.jira_issue + "</td>";
						str += "<td id='quickview_row_"+i+"_jira_issue_status'>Jira Issue Status: "+ tick.fields.jira_issue_status + "</td>";
					        str += "</tr>";
					    };
					    $('#jira_netsuite_quickview_widget_table').prepend(str);
					};
	
    return self;
    };
});

