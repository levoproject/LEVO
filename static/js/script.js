$(document).ready(function() {
    // Initially hides forms and buttons from index page.
    $('#current_user').hide();
    $('#questions_2').hide();
    $('#questions_3').hide();
    $('#h2_q2').hide();
    $('#h2_q3').hide();
    $('#previous').hide();

    // Tests if page loaded has results from clicking "Give me recipes, please". If there are no results to show the result-elements are hidden.
    if ( $('#result_check').text().length == 0 ) {
        $('#submit_again').hide();
        $('#label').hide();
        $('.swiper-container').hide();
    // If there are generated results the question forms are hidden instead.
    } else {
        $('.form_1').hide();
        $('form').removeClass("form");
        $('#questions').removeAttr('id');
        swiper.slideTo($('#center_slide').index(),0,false);
        var element = document.getElementById("progress_bar");
        var width = 0;
        var identity = setInterval(scene_2, 5);
        function scene_2() {
            if (width >= 100) {
                clearInterval(identity);
            } else {
                width++;
                element.style.width = width + '%';
            };
        }
    };
    if ( $('#current_user').text().length != 0 ) {
        $('#login').hide();
        $('#profile_icon_online').show();
        $('#profile_icon').hide();
        $('#current_user').show();
    } else {
        $('#profile').hide();
        $('#logout').hide();
        $('.star').hide();
        $('#profile_icon_online').hide();
        $('#profile_icon').show();
    }

    $('#next').click(function(){
        $('#h2_q1').hide(200);
        $('#h2_q2').show(200);
        $('#questions_1').hide(200);
        $('#questions_2').show(200);
        $('#previous').show(200);
        $('#next').hide(200);
        var element = document.getElementById("progress_bar");
        var width = 0;
        var identity = setInterval(scene_1, 5);
        function scene_1() {
            if (width >= 50) {
                clearInterval(identity);
            } else {
                width++;
                element.style.width = width + '%';
            };
        }
    });

    $('#previous').click(function(){
        $('#h2_q1').show(200);
        $('#h2_q2').hide(200);
        $('#questions_1').show(200);
        $('#questions_2').hide(200);
        $('#previous').hide(200);
        $('#next').show(200);
        var element = document.getElementById("progress_bar");
        var width = 50;
        var identity = setInterval(scene_1, 5);
        function scene_1() {
            if (width <= 0) {
                clearInterval(identity);
            } else {
                width--;
                element.style.width = width + '%';
            };
        }  
    });

    $('#submit').click(function(){
        $('#swiper-container').show();
        $('#label').show();
    });

    
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

    $(":checkbox").on("change", function() {
        /* Changes the color of the label and checkbox field when checked  */
        var that = this;
        $(this).parent().parent().css("background-color", function() {
            return that.checked ? "#4B8153" : "";
        });
    });

    document.addEventListener("keydown", function(e){
        if(e.keyCode == 37) {
            swiper.slidePrev(); 
            //Left arrow pressed
        }
        if(e.keyCode == 39) {
            swiper.slideNext();
            //Right arrow pressed
        }   
        if(e.keyCode == 13) {
            $(".text-tag").trigger('click');
            //
        }   
    });

    $(document).keypress(function(e) {
        if (e.which == 13) {
            alert('Enter key pressed');
            $('.text-tag').trigger('click');
        }
    });

    $('.main_class').click( function() {
        closeNav();
    });

});
