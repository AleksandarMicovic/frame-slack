function userMessage(text) {
    $('#message').html(text);
}

function getURLParameter(name) {
    var url = window.location.href;
    name = name.replace(/[\[\]]/g, "\\$&");
    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)");
    var results = regex.exec(url);

    if (!results) return null;
    if (!results[2]) return '';

    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

$(document).ready(function() {
    var frameApp = new FrameApp({
        hash: $("#app").val(),
        fileName: getURLParameter("url")
    });

    frameApp.bind(FrameApp.EVENT_ERROR, function(error) {
        if (error.code == 57) {
            userMessage("Starting up an instance. Sit tight.");
        } else if (undefined === error.code) {
            userMessage("Try another URL because the required application was not found. :(");
        } else {
            userMessage("Frame error:" + error.code + ". " + error.message);
        }
    });

    frameApp.bind(FrameApp.EVENT_READY, function() {
        userMessage("Starting up your session!<br/>This may take up to 3 minutes.");

        frameApp.startSession({
            connectOnStart: true,
            waitForInstance: true,
        }).then(function(){
        }).catch(function(error) {
            if (error.code == 57) {
                userMessage("Starting the application. This may take a few minutes.");
            } else {
                userMessage("Try again in a few minutes! :(");
            }
        });

        frameApp.bind(FrameApp.EVENT_LOADING_DONE, function() {
            console.log("FrameApp.EVENT_LOADING_DONE");
        });

        frameApp.bind(FrameApp.EVENT_BROADCAST_SESSION_ID, function() {
            console.log("FrameApp.EVENT_BROADCAST_SESSION_ID");
        });

        frameApp.bind(FrameApp.EVENT_TERMINAL_SHOWN, function() {
            console.log("FrameApp.EVENT_TERMINAL_SHOWN");
        });

        frameApp.bind(FrameApp.EVENT_CLOSED, function() {
            userMessage("Your session is over. You can now close this tab. :)");
            close(); // This won't do anything in most cases, but just in case.
        }); 
    });
});
