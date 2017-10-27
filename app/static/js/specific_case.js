$(document).ready(function() {
    $("#exampleTable").DataTable({
        "processing":true,
        "serverSide":true,
        "ajax":"/api/table/clients"
    });
    $("#date_opened").datepicker({ dateFormat: 'yy-mm-dd'});
    $("#date_closed").datepicker({ dateFormat: 'yy-mm-dd'});
    $("#editformtoggle").click(function(){
        var isFormDisabled = $('fieldset').prop('disabled');
        $('fieldset').prop('disabled', !isFormDisabled);
        $('#savebutton').prop('disabled', !isFormDisabled);
    });
});