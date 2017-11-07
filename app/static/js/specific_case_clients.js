$(document).ready(function () {

    $("#clientsTable").DataTable({
        "paging": false,
        "searching": false,
        "info": false,
        "order": [[2, "asc"]],
        "columns": [
            {"data": "role", "orderable": false},
            {"data": "first_name"},
            {"data": "last_name"},
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