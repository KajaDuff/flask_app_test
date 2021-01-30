//other table

$(document).ready(function () {

    //filtration buttons
    $('#category_buttons').on("click", 'button', function () {

        var category_value = $(this).attr('category_value')
        window.location.href = '/user/browse/aggregatedBy' + category_value
    })



    //setup DataTable
    var table = $('#browse_cases_aggregated').DataTable({
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
        scrollY: 300,
        scrollX: '100%',
        dom: "t<'#bottom.row'<'col-xs-4'l><'col-xs-4'i><'col-xs-4'p>>",
        columnDefs: [
            { "width": "50%", "targets": 0 },
            { "width": "30%", "targets": 1 },
            {
                "targets": [2],
                "width": "20%",
                "orderable": false,
                "render": function (data) {
                    return ('<button type="button" class="btn btn-outline-primary" id="show_category" type="button" title="Zobrazit kategorii případů">Zobrazit</button>')
                } //this solution required to keep status_id value hidden below button
            }]
    });



    $("#browse_cases_aggregated").on("click", '#show_category', function (event) {
        var row_data = table.row($(this).parents('tr')).data();
        subcategory = row_data[0]
        state_id = row_data[2]
        if (state_id == "" && subcategory) {

            url = document.URL + '/' + subcategory
        }
        else {
            url = document.URL + '/' + state_id
        }
        window.location.href = url
    });




});



