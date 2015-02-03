var modal = (function () {
    var $startButtons = $('#edit-modal button')
    var $window = $(window);
    var $modal = $('<div class="modal" />');
    var $content = $('<div class="modal-content" />')
    var $close = $('<button role="button" class="modal-close">close</button>');
    var $modalContent = $('.modal-content');
    var $editform = $('#edit-form').detach()
    var $newForm = $('#new-form').detach()
    var $thismodal = ''
    var $glob_data = ''

    function loadJSON() {
        $.getJSON(/nodeshift/, function (data) {
            $glob_data = data;
        });
    };


    $modal.append($content, $close)
    ;
    $('#edit_node').on('click', function (e) {
        editNode(e)
    })

    $close.on('click', function (e) {
        closePrep(e)
    })
    function closePrep(e) {
        e.preventDefault();

        if ($('#edit-form')) {
            $('#edit-form').detach()
        }
        else if ($('#new-form')) {
            $('#new-form').detach()
        }
        //append start content to modal to return to beginning appearance
        $startButtons.appendTo($thismodal)
        $('#edit_node').on('click', function (e) {
            editNode(e)
        })

        /*add section to handle create node button*/

        modal.close();
    };


    /* FOR EDITING EXISTING NODES */

    function editNode(e) {
        e.preventDefault()
        $thismodal = $('#edit-modal')
        $thismodal.empty()
        $editform.appendTo($thismodal)
        nodeSelectHandler()
        editDetails()
        submit()

        //handle submit action
        function submit() {
            $('#edit-form').submit(function (event) {
                event.preventDefault()
                //clear modal of forms to prevent resubmission
                if ($('#edit-form')) {
                    $('#edit-form').detach()
                }
                else if ($('#new-form')) {
                    $('#new-form').detach()
                }

                //append start content to modal to return to beginning appearance
                $startButtons.appendTo($thismodal)

                /*add section to handle create node button*/

                $(this).submitForm(event)
            })
        }
    };

    
    /* Select node */

    /* Populate node selector based on tier choice */
    function nodeSelectHandler() {
        $('#tier-select').on('change', function () {
            var $tier = $('#tier-select option:selected').html()
            var $nodeSet = []
            var $options = ['<option value="">Select a topic</option>']
            /* populate $nodeSet based on selection */
            if ($tier == 'Tier1') {
                for (var i = 0; i < glob_data.length; i++) { 
                    if (glob_data[i].model == 'app.node_1') {
                        $nodeSet.push(glob_data[i].fields.node_name)
                    }
                    else {
                    }
                }
            }
            else if ($tier == 'Tier2') {
                for (var i = 0; i < glob_data.length; i++) {
                    if (glob_data[i].model == 'app.node_2') {
                        $nodeSet.push(glob_data[i].fields.node_name)
                    }
                    else {
                    }
                }
            }
            else if ($tier == 'Tier3') {
                for (var i = 0; i < glob_data.length; i++) {
                    if (glob_data[i].model == 'app.node_3') {
                        $nodeSet.push(glob_data[i].fields.node_name)
                    }
                    else {
                    }
                }
            }
            else if ($tier == 'Tier4') {
                for (var i = 0; i < glob_data.length; i++) {
                    if (glob_data[i].model == 'app.node_4') {
                        $nodeSet.push(glob_data[i].fields.node_name)
                    }
                    else {
                    }
                }
            }
            if ($tier == 'Tier5') {
                for (var i = 0; i < glob_data.length; i++) {
                    if (glob_data[i].model == 'app.node_5') {
                        $nodeSet.push(glob_data[i].fields.node_name)
                    }
                    else {
                    }
                }
            }

            /* build html for node-select */
            for (var j = 0; j < $nodeSet.length; j++) {
                option = '<option value="' + $nodeSet[j] + '">' + $nodeSet[j] + '</option>'
                $options.push(option)
            }
            /* display new field options */
            $('#node-select').empty().html($options)
        }

    )};
  
    //update fields in edit modal
    function editDetails() {
        $('#node-select').on('change', function() {
            var $this_node = $('#node-select option:selected').html()

            for (var i = 0; i < glob_data.length; i++) {
                if (glob_data[i].fields.node_name == $this_node) {
                    $('#text-details').val(glob_data[i].fields.details)
                    $('#node_description').val(glob_data[i].fields.node_description)
                }
                else {
                }
            }
        })
    }



    /*FOR ADDING NEW NODES*/
    
    $('#create_node').on('click', function () {
        $thismodal = $('#edit-modal')
        $thismodal.empty()
        $newForm.appendTo($thismodal)
    })


    //methods made visible for calling from outside of the plugin
    return {
        center: function () {
            var top = Math.max($window.height() - $modal.outerHeight(), 0) / 2;
            var left = Math.max($window.width() - $modal.outerWidth(), 0) / 2;
            var width = $window.width()
            var height = $window.height()

            $modal.css({
                top: top + $window.scrollTop(),
                left: left + $window.scrollLeft()
            });
            $modal.css({
                width: width,
                height: height
            });
        },

        open: function (settings) {
            $content.empty().append(settings.content);

            $modal.css({
                width: settings.width || 'auto',
                height: settings.height || 'auto',
                'margin-top': settings.top || 'auto'
            }).prependTo('body');

            modal.center();
            $window.on('resize', modal.center);
        },

        close: function () {
            $content.empty();
            $modal.detach();
            $(window).off('resize', modal.center);
        }
    };
}());