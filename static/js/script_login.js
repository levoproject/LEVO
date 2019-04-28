$(document).ready(function() {
    $('#register_form').hide();
    $('#login_form').show();
    if ( $('#error_msg').text().length == 0 ) {
        $('#error_msg').hide();
    }
    $('#switch_forms_btn').click(function(){
        $('#register_form').show();
        $('#login_form').hide();
        var name_input = $('#username').val();
        $('#reg_username').val(name_input);
    });
    $('#switch_forms_btn_back').click(function(){
        $('#register_form').hide();
        $('#login_form').show();
        var name_input = $('#reg_username').val();
        $('#username').val(name_input);
    });
});
