$(document).ready(function() {
    $('.profile-buttons').hide(150);

    $('.outer > h1').each(function() {
        $(this).next().hide();
    });
    
    $("h2").each(function() {
        if ( $(this).text().length >= 40 ) {
            $(this).text($(this).text().slice(0,40) + "...");
        };
    });

    $(".outer > h1").each(function() {
        if (parseInt($(this).attr("data-count")) == 0) {
            $(this).css("cursor", "initial");
        }
    });

    $('#hide_all_inner').click(function() {    
        $('.outer > h1').next().each(function() {
            $(this).hide(150);
        });
    });

    $('.outer > h1').click(function() {
        if ($(this).next().is(":hidden") && parseInt($(this).attr("data-count")) != 0) {
            $(this).next().show(150);
            $('html, body').animate({scrollTop: $(this).offset().top}, 400);
        } else {
            $(this).next().hide(150);
        }
    });

    $('#cog').click( function() {
        if ($('#settings > .outer > .inner').is(":hidden")) {
            $('.profile-buttons').show(150);
            $('#settings > .outer > .inner').show(150);
            $('html, body').animate({scrollTop: $('.profile-pic').offset().top}, 400);
        } else {
            $('.profile-buttons').hide(150);
            $('#settings > .outer > .inner').hide(150);
        }
    });

    if ( $('#error_msg').text().length == 0 ) {
        $('#error_msg').hide();
    } else {
        $('#inner_profile').show();
        $('#email').focus();
        $('html, body').animate({scrollTop:$(document).height()}, 'slow');
    }

    $(".star").change(function() {
        if(this.checked) {
            $.getJSON($SCRIPT_ROOT + 'star_recipe', {
                recipe_id: $(this).attr("data-recipe_id"),
                title: $(this).attr("data-title"),
                source_url: $(this).attr("data-source_url"),
                image_url: $(this).attr("data-image_url"),
                category: $(this).attr("data-category")
            }, function(data) {
                $('#result').text(data.result); /* Should be removed or changed to a message to the user. */
            });
            return false;
        } else {
            $.getJSON($SCRIPT_ROOT + 'remove_star_recipe', {
                recipe_id: $(this).attr("data-recipe_id")
            }, function(data) {
                $('#result').text(data.result); /* Should be removed or changed to a message to the user. */
            });
        }
    });

    $('#new_pass').keyup(function() {
    /* Shows a message if password is more than 25 characters. */
        var pswd = $(this).val();
        if ( pswd.length > 25 ) {
            $('#pass_info').show(); 
        } else {    
            $('#pass_info').hide();
        }
    });

    $(document).click(function (event) {
        var clickover = $(event.target);
        var _opened = $(".navbar-collapse").hasClass("navbar-collapse in");
        if (_opened === true && !clickover.hasClass("navbar-toggle")) {
            $("button.navbar-toggle").click();
        }
    });

});