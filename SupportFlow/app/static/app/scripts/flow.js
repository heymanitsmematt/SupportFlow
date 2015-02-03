$(document).ready(function () {

    glob_data = ''
    obj = ''
    updated = false
    $active_node_id = $('#software_name').id
    $active_node_name = ''
    timerStarted = 'false'

    //load the node structure JSON object
    function loadJSON() {
        $.getJSON(/nodeshift/, function (data) {
            glob_data = data;
        });
    };

   

    //animate node structure
  
    $("#menu-menu a").on("click", function (e) {
        var $target = $('#node_details')
        obj = this.id
        updateField();
    });


   

    //update $target on node click
    function updateField() {
        //update general text field
        for (var i = 0; i < glob_data.length; i++) {
            try {
                var this_node_key = glob_data[i].pk + '.' + glob_data[i].fields.node_name
                if (this_node_key == obj) {
                    $('#node_details .description').text(glob_data[i].fields.node_description)
                    $('#node_details .details').text(glob_data[i].fields.details)
                    $('.node-name-details').text(glob_data[i].fields.node_name)
                    $active_node_name = glob_data[i].fields.node_name
                }
                else { }
            }
            catch (err) {
                console.log(err)
            }
        }
        updatePicture()

        function updatePicture() { }
        // update picture set for slides
        var $target_slides = $('.slide img')

        for (var j = 0; j < $target_slides.length; j++) {
            $thisslide = $target_slides[j]
            $thisslide.src = "\\static\\app\\content\\node_content\\" + $active_node_name + "images\\" + (j + 1).toString() + ".jpg"

        }
    }


    //slider functions and variables
    $('.slide-viewer').each(function () {
        var $this = $(this)
        var $group = $this.find('.slide-group')
        var $slides = $this.find('.slide')
        var buttonArray = []
        var currentIndex = 0
        var timeout

        function move(newIndex) {
            var animateLeft, slideLeft;

            advance()

            if ($group.is(':animated') || currentIndex === newIndex) {
                return;
            }

            buttonArray[currentIndex].removeClass('active');
            buttonArray[newIndex].addClass('active');

            if (newIndex > currentIndex) {
                slideLeft = '100%';
                animateLeft = '-100%';
            }
            else {
                slideLeft = '-100%';
                animateLeft = '100%';
            }

            $slides.eq(newIndex).css({ left: slideLeft, display: 'block' });
            $group.animate({ left: animateLeft }, function () {
                $slides.eq(currentIndex).css({ display: 'none' });
                $slides.eq(newIndex).css({ left: 0 });
                $group.css({ left: 0 });
                currentIndex = newIndex;
            });
        }

        /*Clears timer on click and moves when timer expires*/
        function advance() {
            clearTimeout(timeout);

            timeout = setTimeout(function () {
                if (currentIndex < ($slides.length - 1)) {
                    move(currentIndex + 1);
                }
                else {
                    move(0);
                }
            }, 400000);
        }

        /* Create a button for each slide and bind event handler to each on index */
        $.each($slides, function (index) {
            var $button = $('<button type ="button" class="slide-btn">&bull;</button>');
	    if (index === currentIndex) {
		$button.addClass('active')
            }
            $button.on('click', function () {
                move(index);
            }).appendTo('.slide-buttons');
            buttonArray.push($button);
        });

        advance()
    })

    /*Modal manager*/
    var $content = $('#edit-modal').detach();
    

    $('#edit').on('click', function () {
        modal.open({ content: $content, width: $(window).width(), height: $(window).height() });
        }
    );

    /*Content size manager*/
    function resizeWindow() {
        $window = $(window)
        $softwareName = $('#software_name')
        $nodeDetails = $('#node_details')
        var width = $window.width() - 285
        var margin = (($window.width() / 2) - ($softwareName.width() /2))

        $nodeDetails.css({
            width : width
        });1

        $($softwareName).css({
            'margin-left' : margin
        })
    };

    //Window size management
    $('ul.tabs a').click(function () { //resize on content material change
        resizeWindow()
    })

    $(window).on('resize', resizeWindow); //resize on window resize
    

    $(document).ready(function () {
        $('.menu').navgoco({
            accordion : true,
        });
        resizeWindow(); //size content frame
        loadJSON(); //load glob_data JSON
        init_tabs(); //begin the tabification of content area
    });


    /*Click handler for menu-toggle button*/
    $('#menu-toggle-hide').on('click', function menuToggle() {
        $nodes = $('#nodes')
        $nodeGuts = $('#nodes').children()
        $details = $('#node_details')
        $menuToggleHide = $('#menu-toggle-hide') /*store button in variable locally so it can be replaced on reverse*/
        $menuToggleShow = $('#menu-toggle-show')
        $width = $(window).width() - 285

        $nodes.animate({
            width: '0px'
        }, 'slow')
        $nodeGuts.fadeOut('slow', function () {
            $details.animate({
                width: '97%'
            })
        })
        $menuToggleHide.fadeOut('slow', function () {
            $menuToggleShow.fadeIn('slow')
        })
        /*bind click handler to 'menu-toggle-show' button*/
        $menuToggleShow.on('click', function () {
            $nodeGuts.fadeIn('slow', function () {
                $nodes.animate({
                    width: '250px'
                }, 'slow')
            })
            $details.animate({
                width: $width
            }, 'slow')
            $menuToggleShow.fadeOut('slow', function () {
                $menuToggleHide.fadeIn('slow')
            })
        })
    })


    $('#start-timer').next().hide() //grab start timer and hide 
            .next().hide()         //the next two components (timer and pause-timer)
                .end()
        .end().on('click', function () {
            $timer = $('#timer')
            $(this).fadeOut('slow', function () {
                $timer.fadeIn('slow', function () {
                    $('#pause-timer').fadeIn('slow', function() {
                        $(document).data('paused', 'false')
                        startTimer()
                    })
                })
            })
        })

    //pause-timer click-event handler. hides pause, shows start. 
    $('#pause-timer').on('click', function () {
        $(this).fadeOut('slow', function () {
            $('#start-timer').fadeIn('slow')
        })
        $(document).data('paused', 'true')
    })

    $(document).bind('setData', function (event, key, value) {
        if (key == 'timer') {
            $('#timer').html(value);
        }
    });

    
    //if it's been paused, get that time, if not, time is 0
    function startTimer() {
        if ($(document).data('pause-time')) {
            $curTime = $(document).data('pause-time')
        }
        else {
            $curTime = 0
        }

        i = $curTime

        setInterval(function () {
            if ($(document).data('paused') == 'false') {
                i++
                secondsToTime(i)
                $('#time').html(time.toString())
            }
            else {
                $(document).data('pause-time', i)
                $('#time').html('paused')
            }
        }, 1000);
    }

    function secondsToTime(s) {
        var h = Math.floor(s / 3600); //Get whole hours
        s -= h * 3600;
        var m = Math.floor(s / 60); //Get remaining minutes
        s -= m * 60;
        time = h + ":" + (m < 10 ? '0' + m : m) + ":" + (s < 10 ? '0' + s : s); //zero padding on minutes and seconds

        return time
    }
           
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken",
                                     $("#csrfmiddlewaretoken").val());
            }
        }
    });

});





