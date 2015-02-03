; (function ($) {
    $.fn.submitForm = function (event) {
        event.preventDefault()
        $form = $(event.target) //store ref to form
        node_name = $form.find('#node-select :selected').html()  //grab form data
        tier = $form.find('#tier-select :selected').val()
        node_description = $form.find('#node_description').val()
        node_details = $form.find('#text-details').val()
        elems = $form.find('.select, textarea')
        var url = $form.attr('action')
        

        var callback = function(dataReceived) {
            modal.close()
            alert('Saved Successfully!')
        }

        var typeOfDataToReceive = 'JSON'

        //build data object with form values
        data = $.map(elems, function (value, i) {
            val = $(value).val()
            name = $(value).attr('name')
            chunk = [{ 'name': name, 'value': val }]
            return chunk
        })
        //prepare data in json form
        data = JSON.stringify(data)

        //ajax call and callback
        $.ajax({
            data: data,
            type: 'POST',
            url: url,
            success: callback
        })
    }
})($)