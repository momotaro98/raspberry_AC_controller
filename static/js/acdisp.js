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
                case 'dry':
                    $("body").css("background-color", "#D8F6CE");
                    break
                case 'blast':
                    $("body").css("background-color", "#F2F2F2");
                    break
                case 'auto':
                    $("body").css("background-color", "#F5ECCE");
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
