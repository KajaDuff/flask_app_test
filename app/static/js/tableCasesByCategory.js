
//DataTables:
$(document).ready(function () {


    var table = $('#browse_cases_subcategory').DataTable({

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
        fixedHeader: true,
        paging: true,
        searching: true,
        processing: true,
        order: [[0, "desc"]],
        scrollX: '100%',
        scrollY: 300,
        dom: "rt<'#bottom.row'<'col-xs-4'l><'col-xs-4'i><'col-xs-4'p>>",
        "columnDefs": [
            {
                "targets": [2],
                "visible": true
            },
            {
                "targets": [-3],
                "orderable": false,
                "render": function () {
                    return ('<button type="button" class="btn btn-outline-primary" id="display" type="button" title="Zobrazit položky případu">Zobrazit</button>')
                }
            },
            {
                "targets": [-2],
                "orderable": false,
                "render": function (data, type, full) {
                    return buttons(data)
                }
            },
            {
                "targets": [-1],
                "orderable": false,
                "render": function () {
                    return ("<button id='info_button_cases' type='button' class='btn btn-outline-secondary' title='Zobrazit historii změn případu'>" +
                        "<a href=#CaseInfo><span class='glyphicon glyphicon-info-sign'></span></a>" +
                        "</button>")
                }


            }],
        initComplete: function () {
            this.api().columns([2, 3, 4]).every(function () {
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

    //render options for 'close case' and 'delete case' buttons
    function buttons(data) {
        var new_data = data.slice(1,-1).split(',')
        if (new_data[1].trim() == '130') {
            return ("<button id='c1' type='button' class='btn btn-secondary' disabled style='width: 60px'>Uzavřeno</button>" +
                " " +
                "<button id='c2' type='button' class='btn btn-outline-danger' style='width: 60px'>Odstranit</button>")

        }
        else if (new_data[1].trim() == '140') {
            return ("<button id='c1' type='button' class='btn btn-outline-secondary' disabled style='width: 60px' title='*Finální krok* Uzavření případu.'>Uzavřít</button>" +
                " " +
                "<button id='c2' type='button' class='btn btn-outline-secondary' disabled style='width: 60px' title='*Finální krok* Odstranění nežádoucího případu.'>Odstranit</button>")

        }
        else {
            return ("<button id='c1' type='button' class='btn btn-outline-primary' style='width: 60px' title='*Finální krok* Uzavření případu.'>Uzavřít</button>" +
                " " +
                "<button id='c2' type='button' class='btn btn-outline-danger' style='width: 60px' title='*Finální krok* Odstranění nežádoucího případu.'>Odstranit</button>")
        }

    }

    //input filtration
    $(".input-filter").each(function (i) {
        $('input', this).on('keyup change', function () {
            console.log("table.column(i)", table.column(i).index())
            if (table.column(i).index() == 0) {
                console.log('A')
                i = 0
            }
            else if (table.column(i).index() == 1) {
                console.log('B')
                i = 1
            }
            else if (table.column(i).index() == 2) {
                console.log('C')
                i = 5
            }
            else if (table.column(i).index() == 3) {
                console.log('D')
                i = 6
            }
            if (table.column(i).search() !== this.value) {
                table
                    .column(i)
                    .search(this.value)
                    .draw();
            }
        });
    });

    $("#browse_cases_subcategory tbody").on("click", '#display', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        case_id = row_data[0]
        state_id = row_data[2]
        //alert( 'You clicked on '+ row_data[0]+'\'s row' + case_id + state_id);
        window.location.href = '/user/browse/case_id_' + case_id + '?state_id=' + state_id;
    });


    //click event for "show logs" button
    $("#browse_cases_subcategory tbody").on("click", '#info_button_cases', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        case_id = row_data[0]
        state_id = row_data[2]

        //alert( 'You clicked on '+ row_data['caseID']+'\'s row' + case_id + state_id);
        window.location.href = '/user/display/case_id_' + case_id + '/logs?state_id=' + state_id;
    })


});







