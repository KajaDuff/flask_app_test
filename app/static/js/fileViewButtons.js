$(document).ready(function () {

    //function to retrieve params from URL path
    var urlPath = window.location.pathname
    if (urlPath.split('/')[3]) {
        case_id = (urlPath.split('/')[3]).split('_')[2]
    }
    if (urlPath.split('/')[4]) {
        item_id = (urlPath.split('/')[4]).split('_')[2]
    }

    

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
 
    type = vars['type']
    contact_type = vars['contact']
    state_id = vars['state_id']
 

    $('#c7').on('click', function () {

        var text = "Odstranění položky"
        var data = {
            case_id: case_id,
            item_id: item_id,
            state_id: vars['state_id'],
            text: text
        }
        var new_state_id

        function setNewStateID(value) {
            new_state_id = value
        }
        var url = "http://" + window.location.host + "/user/remove_case_item"
        var url_log = "http://" + window.location.host + "/user/create_case_item_log"

        if (confirm("Opravdu si přejete odstranit položku" + item_id + " ?")) {

            console.log('confirmed')
            $.ajax({
                type: "PUT",
                url: url,
                data: data
            }).done(function (result) {
                setNewStateID(result['newStateID'])
                window.location.href = '/user/browse'
            }).fail(function (jqXHR, textStatus, errorThrown) {
                // needs to implement if it fails
            });
            $.ajax({
                type: "PUT",
                url: url_log,
                data: data
            });
        }
        else {
            console.log('rejected')
        }

    });

    $('#download_button').on('click', function (e) {
        var filepath = document.getElementById('download_button').value
        var category_value = $(this).attr('value')
        var url = "http://" + window.location.host + "/download_attachement/" + filepath
        window.location.href = url

    });



    $("#delete_email_button").on("click", function () {
        var email_id = document.getElementById('delete_email_button').value
        var url = "http://" + window.location.host + "/change_email_state"
        var data = {
            email_id: email_id,
            state_id: 100 //always 100 => "smazán"
        }
        if (confirm("Opravdu si přejete email " + email_id + " smazat?")) {
            console.log("confirmed")
            $.ajax({
                type: "PUT",
                url: url,
                data: data,
            }).done(function(){
                window.location.href = "http://" + window.location.host + "/user/browse/unclassified"
            })
        }
        
    });

    $("#forward_button").on("click", function () {
        $("#forward_form").toggle()
    });

    $("#forward_input_button").on("click", function (event) {
        event.preventDefault();
        var email = document.getElementById('forward_input_field').value
        var email_id =  $("#forward_input_field").attr('email_id')
        var url = "http://" + window.location.host + "/change_email_state"
        var data = {
           email_id: email_id,
           state_id: 15 //always 15 => "k přeposlání"
        }
        console.log(email)
        if (email) {
            if (email.endsWith('@gmail.com')){
                $("#warning_forward").hide()
                console.log('1',email, email_id)
            }
            else if (!email.includes('@')){
                $("#warning_forward").hide()
                email = email + '@gmail.com'
                console.log('2',email)
            }
            else {
                $("#warning_forward").show()
            }
        }
        else {
            $("#warning_forward").show()
        }

    });

    $("#classify_button").on("click", function () {
        $("#classify_form").toggle()
    });

    $("#classify_input_button").on("click", function(event){
        event.preventDefault();
        var case_id = document.getElementById('classify_input_field').value
        var email_id =  $("#classify_input_field").attr('email_id')
        var contact = document.getElementById('classify_select_field').value
        var case_id_int = parseInt(case_id)
        if (Number.isInteger(case_id_int) && email_id && contact) {
            $("#warning").hide()
            var url = "http://" + window.location.host + "/classify_email_" + email_id
            var data = {
                case_id: case_id,
                email_id: email_id,
                contact: contact
            }
            if (confirm("Opravdu si přejete email " + email_id + " přiradit k případu " + case_id +" ?")) {
                console.log("confirmed")
                $.ajax({
                    type: "PUT",
                    url: url,
                    data: data,
                })
                .done(function(result){
                    if (result != 'ERROR'){
                        var state_id = result['stateID']
                        var case_id = result['caseID']
                        var item_id = result['itemID']
                        window.location.href = "http://" + window.location.host + "/user/browse/case_id_" + case_id + "?state_id=" + state_id
                    }
                    else {
                        //window.location.reload
                        $("#warning").show()
                    }
                })
            }
        }
        else {
            $("#warning").show()
        }

    })

})


