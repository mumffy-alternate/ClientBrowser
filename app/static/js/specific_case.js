$(document).ready(function () {
    $("#exampleTable").DataTable({
        "lengthMenu": [[2, 3, 5, -1], [2, 3, 5, "All"]],
        "processing": true,
        "serverSide": true,
        "order" : [[2, "desc"]],
        "ajax": "/api/table/clients",
        "columns": [
            {"data": "role", "orderable": false},
            {"data": "first_name"},
            {"data": "last_name"},
            {"data": "case_name", "orderable": false},  //how to do server-side sorting with joins?
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