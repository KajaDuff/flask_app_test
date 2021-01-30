$(document).ready(function () {

    var table = $('#unclassified_table').DataTable({
        language: {
            lengthMenu: "Zobrazit _MENU_ řádků",
            info: "Zobrazeno _START_ až _END_ z celkových _TOTAL_ položek.",
            emptyTable: "Žádné data k zobrazení.",
            infoEmpty: "Zobrazeno 0 z celkových 0 položek.",
            loadingRecords: "Načítám...",
            zeroRecords: "Nebyly nalezeny žádné výsledky.",
            infoFiltered: "(Vyfiltrováno z celkových _MAX_ položek.)",
            paginate: {
                first: "První",
                last: "Poslední",
                next: "Nasledující",
                previous: "Předchozí"
            },
        },
        orderCellsTop: true,
        fixedHeader: false,
        paging: true,
        searching: true,
        order: [[6, "desc"]],
        scrollX: '100%',
        scrollY: 300,
        dom: "t<'#bottom.row'<'col-xs-4'l><'col-xs-4'i><'col-xs-4'p>>",
        columnDefs: [
            {
                "targets": [1],
                "visible": false
            },
            {
                "targets": [8],
                "visible": false
            },
            {
                "targets": [9],
                "visible": false
            },
            {
                "targets": [10],
                "visible": false
            },
            {
                "targets": [11],
                "visible": false
            },
            {
                "targets": [12],
                "visible": false
            },
            {
                "targets": [13],
                "visible": false
            },
            {
                "targets": [14],
                "visible": false
            },
            {
                "targets": [-1],
                "orderable": false,
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-outline-primary" id="display" type="button" title="Zobrazit položku">Zobrazit</button>'
            }
        ],
        initComplete: function () {
            //ids of columns where select filter needs to be applied
            this.api().columns([2]).every(function () {
                var column = this;
                var select = $('<select class="form-control"><option value=""></option></select>')
                    .appendTo($(".select-filter-" + String(column.index())).empty())
                    .on('change', function () {
                        var val = $.fn.dataTable.util.escapeRegex(
                            $(this).val()
                        );
                        column
                            .search(val ? '^' + val + '$' : '', true, false)
                            .draw();
                    });
                column.data().unique().sort().each(function (d, j) {
                    select.append('<option value="' + d + '">' + d + '</option>')
                });
            });
        }
    });

    $(".input-filter-unclassified").each(function (i) {
        $('input', this).on('keyup change', function () {
            console.log("table.column(i)", table.column(i).index())
            if (table.column(i).index() == 0) {
                console.log('A')
                a = 0
            }
            else if (table.column(i).index() == 1) {
                console.log('B')
                a = 3
            }
            else if (table.column(i).index() == 2) {
                console.log('C')
                a = 4
            }
            else if (table.column(i).index() == 3) {
                console.log('D')
                a = 5
            }
            else if (table.column(i).index() == 4) {
                console.log('E')
                a = 6
            }
            if (table.column(a).search() !== this.value) {
                table
                    .column(a)
                    .search(this.value)
                    .draw();
            }
        });
    });

    $("#unclassified_table tbody").on("click", '#display', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        email_id = row_data[0]
        window.location.href = '/user/display/email_id_' + email_id 
    });


})