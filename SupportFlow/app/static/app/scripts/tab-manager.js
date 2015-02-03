
function init_tabs() {
    if (!$('ul.tabs').length) { //if there are no tabs found, return
        return;
    }
    else {
        $('#tabs').find('a:first').addClass('current')
        $('.tab_content').filter(':first').hide()
    }

    $('#content-frame').each(function () {
        $(this).find('.tab_content:first').show()
    });

    $('ul.tabs a').click(function () {
        if (!$(this).hasClass('current')) {
            $(this).addClass('current').parent('li')
                .siblings('li').find('a.current').removeClass('current');
          
            $($(this).attr('href')).show().siblings('div.tab_content').hide()
        }
        this.blur();
        return false;
    });

    //tabs AJAX handler for node topics
    $node_set = $('#nodes a')
    $node_set.each(function () { //update data for 'node_focus' when focus shifts
        $(this).click(function () {
            $(document).data('node_focus', $(this).text())
            //******create ajax function here************
            pdfajax()
        })
    })

    function pdfajax() {
        if (key == 'node_focus') {
            data = $(document).data()['node_focus']
            
            //callback for success
            callback = function (dataReceived) {
                alert(dataReceived)
                pdf = dataReceived['pdf']
                $('#tab_content_primary_02').html(pdf)
            }

            //callback for error
            error = function (xhr, textStatus, errorThrown) {
                alert('An error occurred! ' + (errorThrown ? errorThrown : xhr.status))
            }

            $.ajax({
                type: 'POST',
                url: '/pdfsearch.html/',
                data: data,
                success: callback,
                error: error
            })
        }
        else {
            alert(key, value)
        }
    }
};