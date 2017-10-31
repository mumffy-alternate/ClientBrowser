$(document).ready(function () {
    $("#exampleTable").DataTable({
        "lengthMenu": [2, 3, 5, -1],
        "processing": true,
        "serverSide": true,
        "ajax": "/api/table/clients",
        "columns": [
            {"data": "role"},
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "case_name"},
        ]
    });
    $("#date_opened").datepicker({dateFormat: 'yy-mm-dd'});
    $("#date_closed").datepicker({dateFormat: 'yy-mm-dd'});
    $("#editformtoggle").click(function () {
        var isFormDisabled = $('fieldset').prop('disabled');
        $('fieldset').prop('disabled', !isFormDisabled);
        $('#savebutton').prop('disabled', !isFormDisabled);
    });
});