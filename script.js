
// CONFIG
var DATA_SCRIPT = "data.js";

var INTERVAL_TIME = 4000;
var UPDATE_TIME   = 2000;

// GLOBALS
data = [];

$(document).ready(function() {

    // Load data
    $.getScript(DATA_SCRIPT);

    var i = 0;
    var disp_img = function() {
        console.log("loop: " + i);
        console.log(data);
        $("#container").css("background-image", "url(img/photobooth/" + data[i % data.length] + ")");
        i++;
    }

    var loop = setInterval(disp_img, INTERVAL_TIME);

    var update = function() {
        old = data.length;
        $.getScript(DATA_SCRIPT, function() {

            if(old != data.length) {
                console.log("UPDATE!!!!!")
                clearInterval(loop);
                var j = i;
                i = 0;
                disp_img();
                i = j;
                loop = setInterval(disp_img, INTERVAL_TIME);
            }

        });
    }

    var update = setInterval(update, UPDATE_TIME);
});
