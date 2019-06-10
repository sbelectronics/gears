COLORS = ["red", "green", "blue", "white", "magenta", "yellow", "cyan",  "black", "orange"];

function gears() {
    onFreqChange = function() {
        console.log("FreqChange");
        freq = $("#slider-freq").slider("value");
        $("#freq-setPoint").text(freq);
        if (gears.postUI) {
            gears.sendFreq(freq);
        }
    }

    onFreqStartSlide = function() {
        console.log("startSlide");
        gears.freqSliding=true;
    }

    onFreqStopSlide = function() {
        console.log("stopSlide");
        gears.freqSliding=false;
    }

    onPowerOn = function() {
        var button_selector = "#power-on";
        var icon_selector = "#icon-power-on";
        console.log("PowerOn");
        $(".btn-power").removeClass("active");
        $(".icon-power").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show();
        if (gears.postUI) {
            gears.setPower(1);
        }
    }

    onPowerOff = function() {
        var button_selector = "#power-off";
        var icon_selector = "#icon-power-off";
        console.log("PowerOff");
        $(".btn-power").removeClass("active");
        $(".icon-power").hide();
        $(button_selector).addClass("active");
        $(icon_selector).show();
        if (gears.postUI) {
            gears.setPower(0);
        }
    }

    sendFreq = function(freq) {
        $.ajax({url: "/gears/setFreq?freq=" + freq});
        gears.ignoreOne = true;  // ignore the next getStatus as it might be stale
    }

    setPower = function(value) {
        $.ajax({url: "/gears/setEnable?value=" + value});
    }

    initButtons = function() {
        $("#slider-freq").slider({min: 1,
                                    max:4000,
                                    change: this.onFreqChange,
                                    start: this.onFreqStartSlide,
                                    stop: this.onFreqStopSlide});

        $("#power-on").click(function() { gears.onPowerOn(); });
        $("#power-off").click(function() { gears.onPowerOff(); });
    }

    parseSettings = function(settings) {
        //console.log(settings);
        this.postUI = false;
        try {
            if ((!gears.freqSliding) && (!gears.ignoreOne)) {
                $("#slider-freq").slider({value: settings.freq});
            }
            gears.ignoreOne = false;
            if (settings["enabled"]) {
                if (! $("#power-on").hasClass("active") ) {
                    $("#icon-power-on").click();
                }
            } else {
                if (! $("#power-off").hasClass("active") ) {
                    $("#icon-power-off").click();
                }
            }
        }
        finally {
            this.postUI = true;
        }
    }

    requestSettings = function() {
        $.ajax({
            url: "/gears/getStatus",
            dataType : 'json',
            type : 'GET',
            success: function(newData) {
                gears.parseSettings(newData);
                setTimeout("gears.requestSettings();", 1000);
            },
            error: function() {
                console.log("error retrieving settings");
                setTimeout("gears.requestSettings();", 5000);
            }
        });
    }

    start = function() {
         this.postUI = true;
         this.initButtons();
         this.requestSettings();
    }

    return this;
}

$(document).ready(function(){
    gears = gears()
    gears.start();
});

