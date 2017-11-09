$(document).ready(function () {

    var ajaxUrl = "/api/table/clients/";
    if (caseId !== undefined) {
        ajaxUrl = "/api/table/case/" + caseId + "/clients/";
    }

    $("#exampleTable").DataTable({
        "lengthMenu": [[15, 25, -1], [15, 25, "All"]],
        "processing": true,
        "serverSide": true,
        "order": [[2, "desc"]],
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