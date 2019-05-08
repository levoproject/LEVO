$(document).ready(function() {
    $('#current_form').hide();
    $('#register_form').hide();
    $('#login_form').show();
    if ( $('#error_msg_login').text().length == 0 ) {
        $('#error_msg_login').hide();
    }
    if ( $('#error_msg_reg').text().length == 0 ) {
        $('#error_msg_reg').hide();
    }
    if ( $('#current_form').text() == "2" ) {
        $('#register_form').show();
        $('#login_form').hide();
        $('#reg_username').focus();
    }
    $('#switch_forms_btn').click(function(){
        $('#register_form').show();
        $('#login_form').hide();
        var name_input = $('#log_username').val();
        $('#reg_username').val(name_input);
        $('#log_username').val("");
        $('#log_password').val("");
        $('#current_form').text("2")
        $('#reg_username').focus();
    });
    $('#switch_forms_btn_back').click(function(){
        $('#register_form').hide();
        $('#login_form').show();
        var name_input = $('#reg_username').val();
        $('#log_username').val(name_input);
        $('#reg_username').val("");
        $('#reg_password').val("");
        $('#current_form').text("1")
        $('#log_username').focus();
    });
    
    $('input[type=password]').keyup(function() {
        var pswd = $(this).val();
        if ( pswd.length > 25 ) {
            $('#pass_info').show(); 
        } else {    
            $('#pass_info').hide();
        }
    });
});
