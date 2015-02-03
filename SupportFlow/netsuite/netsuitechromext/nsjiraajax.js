/*
***** will not work as content script!!! 
     content script must pass data in message to ext script for cross domain XHR*****
*/

$(function () {
    //var port = chrome.runtime.connect({ name: "shortDescription" });
    var $shortDesc = $('#title')

    var port = chrome.runtime.connect({ name: "shortDescription" });
    port.postMessage({ type: "short_description", content: "exposed" })

    //postMessage function to pass shortDescription to jirasearch API in jirasearch.js
    $shortDesc.bind("blur", function() {
        port.postMessage({ type: "short_description", content: $shortDesc.value });
        alert('sent: ' + $shortDesc.value)
    });

    //listen for onConnect event and message posted from 
    chrome.runtime.onConnect.addListener(function (port) {
        //Listen for results 
        port.onMessage.addListener(function(msg) {
            if (msg.type == "jira_results") {
                console.log(msg.content)
            };
        });
    });

});



//fields.status.name