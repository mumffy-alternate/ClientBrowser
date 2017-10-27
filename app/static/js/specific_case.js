$(document).ready(function() {
    $("#exampleTable").DataTable();
    $("#date_opened").datepicker({ dateFormat: 'yy-mm-dd'});
    $("#date_closed").datepicker({ dateFormat: 'yy-mm-dd'});
    $("#editformtoggle").click(function(){
        var isFormDisabled = $('fieldset').prop('disabled');
        $('fieldset').prop('disabled', !isFormDisabled);
        $('#savebutton').prop('disabled', !isFormDisabled);
    });
});