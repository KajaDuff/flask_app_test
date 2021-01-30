$(document).ready(function () {

    var table = $('#log_table').DataTable({
        language: {
            lengthMenu: "Zobrazit _MENU_ řádků",
            info: "Zobrazeno _START_ až _END_ z celkových _TOTAL_ položek.",
            emptyTable: "Žádné data k zobrazení.",
            infoEmpty: "Zobrazeno 0 z celkových 0 položek.",
            loadingRecords: "Načítám...",
            zeroRecords: "Nebyly nalezeny žádné výsledky.",
            paginate: {
                first: "První",
                last: "Poslední",
                next: "Nasledující",
                previous: "Předchozí"
            },
        },
        orderCellsTop: true,
        fixedHeader: true,
        paging: true,
        searching: true,
        processing: true,
        scrollX: '100%',
        scrollY: 300,
        dom: "t<'#bottom.row'<'col-xs-4'l><'col-xs-4'i><'col-xs-4'p>>",
        //ajax: '/user/get_item_logs',
        columns: [
            { "data": "datetime" },
            { "data": "username" },
            { "data": "level" },
            { "data": "text" }
        ]
    });

})