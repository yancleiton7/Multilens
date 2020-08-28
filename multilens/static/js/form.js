$(document).ready(function () {
    var $width = $(window).width();

    if ($width < 800) {
        $(".togle-mobile").removeClass("is-grouped");
    } else {
        $(".togle-mobile").addClass("is-grouped");
    }

    $(window).resize(function () {
        var $width = $(window).width();

        if ($width < 800) {
            $(".togle-mobile").removeClass("is-grouped");
        } else {
            $(".togle-mobile").addClass("is-grouped");
        }
    }
    )
})