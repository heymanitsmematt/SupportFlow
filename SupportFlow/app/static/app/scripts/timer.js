
$.fn.timerUpdate = function (options) {
    var opts = $.extend({}, $.fn.timerUpdate.defaults, options);

    return this.each(function () {
        $('#timer').html(opts.time + 1)
    })

    //Default timer options (on first call)
    $.fn.timerUpdate.defaults = {
        time: -1,
        updates: 0
    };
}