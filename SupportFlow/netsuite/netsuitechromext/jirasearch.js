/* 

Context setup for Netsuite to Jira Search Chrome Plugin

*/

// Set up context menu at install time.
chrome.runtime.onInstalled.addListener(function () {
    //limit context to selection only
    var context = "selection";

    //Create Parent Item
    chrome.contextMenus.create({
        "title": "Jira Search",
        "contexts": [context],
        "id": "parent"
    });

    //create raw search 
    chrome.contextMenus.create({
        "title": "Raw Selection Search",
        "parentId": "parent",
        "contexts": [context],
        "id": "raw"
    });

    //create custom search  ***Right now just Chris' recommendation --> will build into optinos page/jira auth ***
    chrome.contextMenus.create({
        "title": "Custom Selection Search",
        "parentId": "parent",
        "contexts": [context],
        "id": "custom"
    });
    //jump directly to jira ticket of highlighted text
    chrome.contextMenus.create({
        "title": "Ticket Number",
        "parentId": "parent",
        "contexts": [context],
        "id": "direct"
    });

});
//master click handler binding
chrome.contextMenus.onClicked.addListener(onClickHandler);

// The onClicked callback function.
function onClickHandler(info, tab) {
    var sText = info.selectionText;

    //if raw selectionText search
    if (info.menuItemId == "raw") {
        var url = 'http://jira.motionsoft.com:8080/issues/?jql=text%20~%20"' + encodeURIComponent(sText) + '"';
        window.open(url, '_blank');
    }
        //if custom selctionText search **chris' parameters
    else if (info.menuItemId == "custom") {
        var url = 'http://jira.motionsoft.com:8080/issues/?jql=text%20~%20"' + encodeURIComponent(sText) + '"%20ORDER%20BY%20created%20DESC';
        window.open(url, '_blank');
    }
        //if jumping directly to selected JIRA ticket number
    else if (info.menuItemId == "direct") {
        //if only the JIRA case number is highligted
        if (!isNaN(sText)) {
            var url = 'http://jira.motionsoft.com:8080/browse/MOSO-' + sText
            window.open(url, '_blank');
        }
        else {
            //if the MOSO-n is also selected, take just the numeric portion
            var url = 'http://jira.motionsoft.com:8080/browse/' + sText
            window.open(url, '_blank');
        }
    }
};


