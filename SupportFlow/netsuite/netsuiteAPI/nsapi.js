///<reference path="MfsNsIntelliSense.min.js"/>
s is the main page for handling ticket interaction
			 																     ---------- */
			 																
//start by including jquery
function OnPageInit() {
	AddJavascript('//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js', 'head');
	setTimeout(onLoad, 1000);
	
	function onLoad() {
		//'global' scope variables
		currentEscalations = [];
		escto = false;
		ticket = new caseTicket();
		
		//interactive function managers
		//creates custom jQuery plugins
		jQueryExtends();
		
		//updates the escalation history fields on the support form
	    updateEscalationHistory();
	    //addEscalationHistory();
	    
	    
		$('#escalateto_addedit').on('click', escalateEvent);
		
		$("tr[id^=escalateto_row_]").each(function() {
			currentEscalations.push($(this).children().first());
		});
		
		//manage a deescalation event
		$('#deescalateall').on('click', deEscalateEvent);
				
		//manage the escalated assigned to field and drop-down
		checkAddEscalatedAssignedToSelect(ticket);
		
		$('#btn_multibutton_submitter').on('click', ticket.functions.preSave);
		

		ticket.functions.eventHandlers();
		
		ticket.functions.finalLoad();
		//ticket.functions.caseTimer();
		
	}
};

//function to add jquery to suitescript environemnt
function AddJavascript(jsname, pos) {
	var tag = document.getElementsByTagName(pos)[0];
	var addScript = document.createElement('script');
	addScript.setAttribute('type', 'text/javascript');
	addScript.setAttribute('src', jsname);
	tag.appendChild(addScript);
};

function caseTicket(){
	self = this;
	
	//fields
	self.fields = new Object();
	self.fields.id = nlapiGetRecordId();
	self.fields.customer = nlapiGetFieldTextOrValue('custevent1');
	self.fields.customer = self.fields.customer.toString().replace(/,/g,'`').replace(/:/g,'~');
	self.fields.callbackPhone = nlapiGetFieldTextOrValue('phone');
	self.fields.caseNumber = nlapiGetFieldTextOrValue('casenumber');
	self.fields.caseType = nlapiGetFieldTextOrValue('inpt_category');
	self.fields.caseOrigin = nlapiGetFieldTextOrValue('inpt_origin');
	self.fields.product = nlapiGetFieldTextOrValue('product');
	self.fields.module = nlapiGetFieldTextOrValue('module');
	self.fields.shortDescription = nlapiGetFieldTextOrValue('title');
	self.fields.shortDescription = self.fields.shortDescription.toString().replace(/,/g,'`').replace(/:/g,'~');
	self.fields.clientID = nlapiGetFieldTextOrValue('company_display').toString().replace(/:/g,'~');
	self.fields.status = nlapiGetFieldTextOrValue('status');
	self.fields.severity = nlapiGetFieldTextOrValue('inpt_custevent29');
	self.fields.priority = nlapiGetFieldTextOrValue('priority');
	self.fields.assignedTo = nlapiGetFieldTextOrValue('inpt_assigned');
	self.fields.escalatedTo = nlapiGetFieldTextOrValue('custeventescalatedto');
	self.fields.openDate = nlapiGetFieldTextOrValue('startdate');
	self.fields.openedBy = nlapiGetFieldTextOrValue('inpt_custeventcase_created_user');
	self.fields.firstCallResolution = nlapiGetFieldTextOrValue('custevent10_send');	
	self.fields.lastUpdated = nlapiGetFieldTextOrValue('lastmodified_fs');
	self.fields.jiraIssue = nlapiGetFieldTextOrValue('custeventsn_case_number');
	self.fields.jiraIssue = self.fields.jiraIssue.toString().replace(/,/g,'`');
	
	//because of custom email parsing, all commas and colons must be escaped with another charcter. see caseTicket.constants
	self.fields.mostRecentComment = $('iframe')[1];
	self.fields.mostRecentComment = $(self.fields.mostRecentComment).contents().find('body').text().replace(/,/g,'`').replace(/:/g,'~');
	
	//states
	self.statusHandlerBound = false;
	
	//cached objects
	self.cache = new Object();
	self.cache.currentProduct = 'newLoad';
	self.cache.escalatedAssignedTo = 'newLoad';
	
	//functions
	self.functions = new Object();
	/**
	self.functions.caseTimer = function() {
		curTime = nlapiGetFieldValue('custeventescalatedtime1');//CREATE CUSTOM TIMER FIELD
		if (curTime == ''){
			curTime = 0.0;
		};
		start = new Date().getTime()+curTime;
		elapsed = '0.0';
		intervalTrigger = window.setInterval(function(){
				time = new Date().getTime() - start;
				elapsed = Math.floor(time/100)/10;
				if (Math.round(elapsed)==elapsed){
					elapsed += '.0';
					nlapiSetFieldValue('custeventescalatedtime1', elapsed);
				};
			}, 100);
	};
	**/
	self.functions.eventHandlers = function() {
		$('#custeventescalatedto_fs > input').on('click', function() {
			$('#escalatedassignedtoselect').show();
		});
		$('#escalatedassignedtoselect').on('blur', function() {
			$('#escalatedassignedtoselect').hide();
		});
	};
	self.functions.supportKBEmail = function(ticketIn, source) {
		ticket.JSON = JSON.stringify(ticketIn.fields);
		nlapiSendEmail('486461', '486461', source, ticket.JSON);
		console.log('email sent to api@motionsfot.net for ticket' + ticketIn.fields.id);
	};
	self.functions.preSave = function() {
		source = 'preSave';
		tf = new caseTicket();
		notifyEscalateAssignedToOwner();
		ticket.functions.supportKBEmail(tf, source);
		window.clearInterval(intervalTrigger);
	};
	self.functions.finalLoad = function() {
		source = 'finalLoad';
		ticket.functions.supportKBEmail(ticket, source);
		
		//fix the stupidly sized communications field
		//resizeInternalNotes();
		return;
	};
	
	self.constants = new Object();
	self.constants.escapes = new Object();
	self.constants.escapes.comma = 'comma is replaced with ` ';
	self.constants.escapes.colon = 'colon is replaced with ~';
	return self;
};


//function to manage grabbing existing history data and put it in the associated field
function updateEscalationHistory() {
	//add check-return if my_history_fields.length == existing_history_fields.length*	
	
	$root = '#escalatehistrow';
	histloop = 'True';
	i=0;
		
	while (histloop == 'True') {
		if ($($root+i).length != 0) {
			$thisHist = $($root + i);
			
			//set datetime, event
			var date = $($thisHist.children()[0]).text();
			var targetDate = 'custeventescalatehistory' + (i+1);
			nlapiSetFieldValue(targetDate, date); 

			var event = $($thisHist.children()[1]).text() + ' ' + $($thisHist.children()[2]).text();
			var targetEvent = 'custeventescalatehistory' + (i+1) + 'e';
			nlapiSetFieldValue(targetEvent, event); //action and user
			
			//increment i to check if there is any more history data to be gathered
			i++;
		}
		else {
			histloop = 'False';
		};
	};
};


//a function to add new escalation events to the escalation history fields
function addEscalationHistory() {
	var $addEscalateButton = $('#escalateto_addedit');
	
	$($addEscalateButton).on('click', function(e) {
	    findEmpty = 'False';
        targetField = [];
        
        //Gather all input fields to find empty
    	var allFields = [];
		$("input[id^=custeventescalate]").each(function() {
			if (this.type != 'hidden') {
				allFields.push(this);
			}
    	}); 
        
        //need object with 2 attributes for event datetime and event
        newHistData = {};
        newHistData.datetime = new Date();
        newHistData.event = $('#escalateto_escalatee_display').text();
        
	    while (findEmpty == 'False') {
	        for (var i=1; i < $(allFields).length; i++) {
	            thisField = $(allFields[i]);
	            if ($(thisField).text().length > 0) {
	                i++;
	            }
	            else {
	                targetField = allFields[i];
	                findEmpty = 'True';
	            };
	        };
	    $(targetField).val(newHistData.event);
	    findEmpty = 'False';
	    
	    //perform original click handling function
		return true; 
	    };
	});
};



function escalateEvent(event) {
	event.preventDefault();
	self = this;
	self.eventDetails =  $("tr[id^=escalateto_row_").last().text().substring(1, 12);
	self.eventDate = new Date();
	self.numTimesEscalatedField = $("#custeventnumtimesesclated");
	self.numTimesEscalated = function() {
		if ($(self.numTimesEscalatedField).val().length == 0) {
			return 0;
		}
		else {
			newval = parseFloatOrZero(nlapiGetFieldTextOrValue('custeventnumtimesesclated'));
			return newval;
		};
	};
	
	//exit if this isn't a Tier 2 Moso event, we don't care about the data, perform original click handling function
	if (self.eventDetails != 'Moso Tier 2') {
		$(currentEscalations).empty();
		$("tr[id^=escalateto_row_]").each(function() {
			currentEscalations.push($(this).children().first());
		});
		checkAddEscalatedAssignedToSelect(currentEscalations);
		return true;
	}
	
	//create target field array to later use $.findFirsteEmpty() and/or $.findLastFilled()
	allTargetFields = [];
	$("input[id^=custeventescalation]").each(function() {
		if (this.type != 'hidden') {
			allTargetFields.push(this);
		}
	});
	
	//write values into first two empty event and date fields and increment numTimesEscalated
	self.recordEvent = function() { 
		$(allTargetFields).findFirstEmpty().val(self.eventDetails + ' ' + self.eventDate);
		nlapiSetFieldValue('custeventnumtimesesclated', self.numTimesEscalated() + 1);
	};
	
    //perform original click handling function
	self.recordEvent();
	$(currentEscalations).empty();
	$("tr[id^=escalateto_row_]").each(function() {
		currentEscalations.push($(this).children().first());
	});
	checkAddEscalatedAssignedToSelect(currentEscalations);
	return true;
};

function deEscalateEvent(event, currentEscalations) {
	self = this;
	self.eventDate = new Date;
	self.numTimesEscalated = $('#custeventnumtimesesclated').val();
	self.timeEscalatedField = '#custeventescalatedtime' + self.numTimesEscalated;
	self.timeEscalatedField = $(self.timeEscalatedField);
	
	//if not a Tier 2 de-escalation, return with normal function
	self.proceed = false;

	self.currentEscalations = currentEscalations;
	$(self.currentEscalations).each(function() {
		if ($(this).text().substring(1, 12) == 'Moso Tier 2') {
			self.proceed = true;
		}
	});
	if (self.proceed == false) {
		return true;
	}
	
	//get the Moso Tier 2 escalation event for deescalation
	self.eventDetails =  $(self.currentEscalations).each(function() {
		if ($(this).text().substring(1, 12) == 'Moso Tier 2') {
			return this;
		}
	});
	
	//get the original escalation date
	self.escalationDate = $(self.eventDetails).substring(12, self.eventDetails.length);
	
	
	//get the date diff (time spent escalated)
	self.timeEscalated = self.escalationdate - self.eventDate;
	
	
	allTargetFields = [];
	$("input[id^=custeventescalation]").each(function() {
		if (this.type != 'hidden') {
			allTargetFields.push(this);
		}
	});
	
	//use $.findLastFilled to calculate time in Moso Tier 2 escalated status
	self.targetField = $(allTargetFields).findLastFilled();
	self.targetField.val($(self.targetField).text() + ' ' + self.eventDetails() + ' ' + self.eventDate); 
}

function resizeInternalNotes() {
	targets = [];
	targets.push($('#ext-gen14'));
	targets.push($('#exthtmlfield-outgoingmessage_fs'));
	targets.push($('#html-editor-container-outgoingmessage'));
	targets.push($('#ext-gen16'));
	targets.push($('iframe')[1]);
	targets.push($('#ext-comp-1007'));
	targets.push($('#ext-gen11'));
	targets.push($('#ext-gen12'));
	targets.push($('#exthtmlfield-outgoingmessage_fs'));
		
	width = $(window).width() - $('#incomingmessage').width() - 95;
	
	$(targets).each(function(){
		resize(this, width);
	});
	
	function resize(obj, width) {
		$obj = $(obj);
		$obj.css('width', width);
	};
	
	cells = $('.x-toolbar-cell');
	$(cells).each(function() {
		$(this).removeClass('x-hide-display');
	});
	$('#ext-gen56').addClass('x-hide-display');
	
};

//check if the ticket is escalated and binds the event handler 
function checkAddEscalatedAssignedToSelect(ticket) {
	//if not bound, bind and append escalatedTo dropdown
	if (!ticket.statusHandlerBound) {
		$('#inpt_status12').on('select', checkAddEscalatedAssignedToSelect);
		ticket.statusHandlerBound = true;
		addEscalatedAssignedToField(ticket);
		return;
	}
	//if escalated or tracked and bound, add the field
	else if (nlapiGetFieldTextOrValue('status').substr(0,9) == 'Escalated'  | nlapiGetFieldTextOrValue('status') == 'Tracked') {

		addEscalatedAssignedToField(ticket);
		return;
	}
};


//adds the escalated assigned to box to the UI populated with escatee group's users, current assignee selected
function addEscalatedAssignedToField() {
	self = this;
	self.ticket = ticket;
	self.product = getProduct();
	self.groupMembers = new groupMembers(self.product);
	
	if (self.ticket.cache.currentProduct == self.product){
		return;
	}
	ticket.cache.currentProduct = self.product;
	
	
	//returns custom search string for product field.
	function getProduct() {
		prodOut = null;
		a = nlapiGetFieldTextOrValue('inpt_product');
		if (a.toString().substring(0,4) == "MoSo"){
			prodOut = "customsearchmosoproduct";
		}
		else if (a.toString().substring(0,8) == "Conexion") {
			prodOut = "customsearchconexionproduct";
		}
		else if (a.toString().substring(0,5) == "eClub") {
			prodOut = "customsearcheclubproduct";
		}
		else if (!prodOut) {
			console.log(a, prodOut);
		}
		return prodOut;
	};
	
	//perform custom search to return escalatedto group members array
	function groupMembers(product) {
		var thisSearch = this;
		var members = new Array();
		thisSearch.columns = new Array();
		thisSearch.columns[0] = new nlobjSearchColumn('firstname');
		thisSearch.columns[1] = new nlobjSearchColumn('lastname');
		thisSearch.columns[2] = new nlobjSearchColumn('email');

		try {
			var results = new nlapiSearchRecord(null, product, null, thisSearch.columns);
		}
		catch(e) {
			results = e;
			return;
		}
		
		for (var i = 0; i < results.length; i++) {
			thisResult = results[i];
			thisResult.name = results[i].getValue('firstname') + ' ' + results[i].getValue('lastname');
			thisResult.email = results[i].getValue('email');
			
			members.push(thisResult);
		};
		return members;
	};
	
	//build select dropdown if not already placed
	$('#escalatedassignedtoselect').detach();
	self.elementString = "<tr><td><select id='escalatedassignedtoselect' class='dropdownInput'>";
	self.elementString += "<option value='select'>Select an employee</option>";
	for (var i=0; i<self.groupMembers.length; i++) {
		thisGroupMember = self.groupMembers[i];
		thisOption = "<option value='" + thisGroupMember.name.toString() + "'>" + thisGroupMember.name.toString() +"</option>";
		self.elementString += thisOption;
	};
	self.elementString += "</select></td></tr>";	
	
	//find right element to append to and fix label
	$('#custeventescalatedto').parent()
		.parent()
			.parent()
				.parent().append(self.elementString);
	$('#escalatedassignedtoselect').on('change', updateEscalateToField).hide();
	while (currentEscalations.length){
		currentEscalations.pop();
	};
	
	if (!ticket.cache.productHandlerBound) {
		ticket.cache.productHandlerBound = true;
		bindProductHandler(ticket);
	}
	
	function bindProductHandler(ticket) {
		$('#inpt_product9').on('select', checkAddEscalatedAssignedToSelect);
	}
	
	
	function updateEscalateToField() {
		var source =  new $('#escalatedassignedtoselect');
		var target = new $('#custeventescalatedto');
		source.val = source.val();
		target.val = nlapiSetFieldValue('custeventescalatedto', source.val);
	};
	
};


//notifies the user in the escalated field on submit if there is a change to the case. receives asignee string 
function notifyEscalateAssignedToOwner(event) {
	//event.preventDefault();
	//exit if the ticket isn't escalated 
	if (nlapiGetFieldTextOrValue('inpt_status').substr(0,9) != "Escalated") {
		return;
	}
	//create objects for email 
	self = this;
	self.message = new Object();
	self.message.body = "An escalated case assigned to you has been updated! Case #" + nlapiGetFieldTextOrValue('casenumber').toString() + ' with a status of ' + nlapiGetFieldTextOrValue('status').toString();
	var assignee = new assign();
	self.senderID = null;
	
	//because of custom email parsing, all commas and colons must be escaped with another charcter. see caseTicket.constants
	mostRecentComment = $('iframe')[1];
	mostRecentComment = $(mostRecentComment).contents().find('body').text().replace(/,/g,'`').replace(/:/g,'~');
	self.message.body += mostRecentComment;
	
	self.filters = new Array();
	if (assignee.firstName == 'Ahmad') {
		nlapiSendEmail(36548, 'aabdel@motionsoft.net', 'Netsuite Case Update Alert', self.message.body );
		return;
	}
	self.filters[0] = new nlobjSearchFilter('lastname', null, 'startswith', assignee.lastName);
	
	self.columns = new Array();
	self.columns[0] = new nlobjSearchColumn('internalID');
	self.columns[1] = new nlobjSearchColumn('email');
	self.columns[2] = new nlobjSearchColumn('firstname');
	self.columns[3] = new nlobjSearchColumn('middlename');
	self.columns[4] = new nlobjSearchColumn('lastname');
	

	searchResults = nlapiSearchRecord('employee', null, self.filters, self.columns);//var results = nlapiLoadRecord('employee', searchResults[0].getId()); --a fastloading object with ALL attributes

	//loop through results. when results returned, use methods
	//on the nlobjSearchResult object to get values for specific fields.
	for (var i=0; searchResults != null && i < searchResults.length; i++) {
		var searchResult = searchResults[i];
		self.recipientId = searchResult.getId();
		self.recipientFirstName = searchResult.getValue('firstname');
		self.recipientLastName = searchResult.getValue('lastname');
		self.recipientEmail = searchResult.getValue('email');
		self.recipientMiddleName = searchResult.getValue('middlename');
	};
	
	nlapiSendEmail(self.recipientId, self.recipientEmail, 'Netsuite Case Update Alert', self.message.body );
		
	function assign() {
		var assigned = new Object;
		var raw = nlapiGetFieldValue('custeventescalatedto').split(' ');
	    assigned.firstName = raw[0];
	    assigned.lastName = raw[1];
	    return assigned;
	};	
};

function jQueryExtends() {
	//find the first empty field in an array passed
	jQuery.fn.findFirstEmpty = function() {
		//gather all empty fields to later sort and find lowest index
		emptyFieldArray = [];
		
		$(this).each(function() {
			if ($(this).text().length == 0) {
				emptyFieldArray.push($(this).attr('id').charAt($(this).attr('id').length -1));
			}
			else {
			}
		});
		emptyFieldArray.sort();
		var first = $(emptyFieldArray).first();
		var thisId = first[0].toString();
		var returnAttrId = '#' + $(this).first().attr('id').substring(0, $(this).attr('id').length-1) + thisId;
		
		return $(returnAttrId);
	};
	
	//find last filled field in an array
	jQuery.fn.findLastFilled = function() {
		$(this).each(function() {
			return
		});
	};
	
	//normalizes escalation group to custom search
	jQuery.fn.normalizeGroup = function() {
		var searchGroups = new Array(); 
		$(this).each(function() {
			if ($(this).text() == '.Moso Tier 2') {
				searchGroups.push("customsearchmosotier2");
			}
			else if ($(this).text() == '.MOSO Support') {
				searchGroups.push("customsearchmososupport");
			}			
		});
		return searchGroups;
	};
	
	//checks if a ticket is escalated
	jQuery.fn.isEscalated = function() {
		$(this).each(function() {
			if (nlapiGetFieldTextorValue('inpt_status').substr(0,9) == "Escalated") {
				return true;
			}
			else {
				return false;
			}
		});
	};
	
};



