(function(){
    var backcolor_f = function(onoff, operating) {
        if (onoff === "on") {
            switch (operating) {
                case 'cool':
                    $("body").css("background-color", "#CEECF5");
                    break
                case 'warm':
                    $("body").css("background-color", "#F6CECE");
                    break
                case 'auto':
                    $("body").css("background-color", "#E6E6E6");
                    break
                case 'dry':
                    $("body").css("background-color", "#D8F6CE");
                    break
            }
        } else {
            $("body").css("background-color", "#fff");
        }
    };

    var onoffMode = $('#onoffMode').attr('title');
    var operatingMode = $('#operatingMode').attr('title');
    backcolor_f(onoffMode, operatingMode);

}());
