$(document).ready(function() {
    $('#current_form').hide();
    $('#register_form').hide();
    $('#forgot_form').hide();
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
        $('#reg_email').focus();
    });
    $('.switch_forms_btn_back').click(function(){
        $('#register_form').hide();
        $('#forgot_form').hide();
        $('#login_form').show();
        var name_input = $('#reg_username').val();
        $('#log_username').val(name_input);
        $('#reg_username').val("");
        $('#reg_password').val("");
        $('#current_form').text("1")
        $('#log_username').focus();
    });
    $('#switch_forms_btn_forgot').click(function(){
        $('#login_form').hide();
        $('#forgot_form').show();
        var name_input = $('#log_username').val();
        $('#forgot_email').val(name_input);
        $('#log_username').val("");
        $('#log_password').val("");
        $('#current_form').text("3")
        $('#forgot_email').focus();
    });
    
    if ($('#error_msg_login').text() == "There is no user with this username!") {
        $('#log_username').addClass("error_border")
    } else if ($('#error_msg_login').text() == "The password is incorrect!") {
        $('#log_password').addClass("error_border")
    }

    $('#reg_password').keyup(function() {
    /* Shows a message if password is more than 25 characters. */
        var pswd = $(this).val();
        if ( pswd.length > 25 ) {
            $('#pass_info').show(); 
        } else {    
            $('#pass_info').hide();
        }
    });

    $('#reg_username').keyup(function() {
    /* Shows a message if username is more than 25 characters. */
        var username = $(this).val();
        if ( username.length > 25 ) {
            $('#username_info').show(); 
        } else {    
            $('#username_info').hide();
        }
    });
});
