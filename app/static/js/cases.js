$(document).ready(function () {
    $("#casesTable").DataTable({
        "lengthMenu": [[15, 25, 50], [15, 25, 50]],
        "processing": true,
        "serverSide": true,
        "order": [[0, "asc"]],
        "ajax": "/api/table/cases",
        "columns": [
            {"data": "case_name"},
            {"data": "case_status", "orderable": false},
            {"data": "court_name"},
            {"data": "court_case_number"},
            {"data": "date_opened"},
            {"data": "date_updated"},
            {"data": "date_closed"},
        ]
    });

    $("#date_opened").datepicker({dateFormat: 'yy-mm-dd'});
    $("#date_closed").datepicker({dateFormat: 'yy-mm-dd'});
    $("#date_updated").datepicker({dateFormat: 'yy-mm-dd'});
});