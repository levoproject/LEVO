$(document).ready(function() {
    $('#register_form').hide();
    $('#login_form').show();

    $('#switch_forms_btn').click(function(){
        $('#register_form').show();
        $('#login_form').hide();
    });
});
