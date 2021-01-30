//other table

$(document).ready(function () {

    //function to retrieve params from URL query
    var vars = [], hash;
    var q = document.URL.split('?')[1];
    if (q != undefined) {
        q = q.split('&');
        for (var i = 0; i < q.length; i++) {
            hash = q[i].split('=');
            vars.push(hash[1]);
            vars[hash[0]] = hash[1];
        }
    }

    //setup DataTable
    var table = $('#browse_case_items_table').DataTable({
        language: {
            lengthMenu: "Zobrazit _MENU_ řádků",
            info: "Zobrazeno _START_ až _END_ z celkových _TOTAL_ položek.",
            emptyTable: "Žádné data k zobrazení.",
            infoEmpty: "Zobrazeno 0 z celkových 0 položek.",
            loadingRecords: "Načítám...",
            zeroRecords: "Nebyly nalezeny žádné výsledky.",
            infoFiltered:   "(Vyfiltrováno z celkových _MAX_ položek.)",
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
        order: [[6, "desc"]],
        scrollX: '100%',
        scrollY: 300,
        dom: "t<'#bottom.row'<'col-xs-4'l><'col-xs-4'i><'col-xs-4'p>>",

        "columnDefs": [
            {
                "targets": [1],
                "visible": false
            },
            {
                "targets": [2],
                "render": function(data){
                    if (data == 1){
                        return 'žádost'
                    }
                    else if (data == 2){
                        return 'odpověď'
                    }
                    else return data
                }            },
            {
                "targets": [5],
                "visible": false
            },
            {
                "targets": [-2],
                "orderable": false,
                "data": null,
                "defaultContent": '<button type="button" class="btn btn-outline-primary" id="c5" type="button" title="Zobrazit položku">Zobrazit</button>'
            },
            {
                "targets": [-1],
                "orderable": false,
                "data": null,
                "defaultContent": "<button id='info_button_items' type='button' class='btn btn-outline-secondary' title='Zobrazit historii změn položky'>" +
                    "<span class='glyphicon glyphicon-info-sign'></span>" +
                    "</button>"

            }],
            initComplete: function () {
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
                        if (d == 1) {
                            select.append('<option value="' + 'žádost' + '">' + 'žádost' + '</option>')
                        }
                        else if (d == 2) {
                            select.append('<option value="' + 'odpověď' + '">' + 'odpověď' + '</option>')
                        }
                        else {
                            select.append('<option value="' + d + '">' + d + '</option>')
                        }
                    });
                });
            }
    });

    //input filtration
    $(".input-filter-items").each(function (i) {
        $('input', this).on('keyup change', function () {
            if (table.column(i).index() == 1){
                column = table.column(3)
                a=3
            }
            else if (table.column(i).index() == 2){
                column = table.column(4)
                a=4
            }
            else if (table.column(i).index() == 3){
                column = table.column(6)
                a=6
            }
            else if (table.column(i).index() == 0){
                column = table.column(0)
                a=0
            } 
            if (column.search() !== this.value) {
                table
                    .column(a)
                    .search(this.value)
                    .draw();
            }
        });
    });


    $("#browse_case_items_table tbody").on("click", '#c5', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        case_id = row_data[1]
        item_id = row_data[0]
        state_id = vars['state_id'],
        type = row_data[2]
        contact_type = row_data[5]
        window.location.href = '/user/display/case_id_' + case_id + '/item_id_' + item_id + "?state_id=" + state_id //+'&type=' + type + '&contact=' + contact_type;
    });


    $("#browse_case_items_table tbody").on("click", '#info_button_items', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        item_id = row_data[0]
        state_id = vars['state_id'],
        window.location.href = '/user/display/case_id_' + case_id + '/item_id_' + item_id + '/logs?state_id=' + state_id;
    });


});


