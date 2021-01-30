
//filenameplaceholder:

$('#file').on('change', function () {
    //get the file name
    var fileName = $(this).val();
    //replace the "Choose a file" label
    $(this).next('.custom-file-label').html(fileName);
})

$('#Toggle_navbar').on('mouseenter', function(){
    $("#toggle_nav").toggle()
    $("#main_menu").toggle()
})

