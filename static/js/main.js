function userMessage(text) {
    $('#message').html(text);
}

$(document).ready(function() {
    var frameApp = new FrameApp({
        hash: $("#app").val(),
        fileName: $("#url").val()
    });

    frameApp.bind(FrameApp.EVENT_ERROR, function(error) {
        if (error.code == 57) {
            userMessage("Instance starting. Sit tight.");
        } else if (undefined === error.code) {
            userMessage("Try another URL because the required application was not found. :(");
        } else {
            userMessage("Frame error:" + error.code + ". " + error.message);
        }
    });

    frameApp.bind(FrameApp.EVENT_READY, function() {
        userMessage("Starting your session!<br/>This may take up to 3 minutes.");

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
