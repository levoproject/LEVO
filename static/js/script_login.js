$(document).ready(function() {
    $('#register_form').hide();
    $('#login_form').show();
    if ( $('#error_msg').text().length == 0 ) {
        $('#error_msg').hide();
    }
    $('#switch_forms_btn').click(function(){
        $('#register_form').show();
        $('#login_form').hide();
    });
});
