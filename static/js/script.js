$(document).ready(function() {
    $('#current_user').hide();
    $('#questions_2').hide();
    $('#questions_3').hide();
    $('#h2_q2').hide();
    $('#h2_q3').hide();
    $('#previous').attr("disabled", true);
    $('#previous').addClass("disabled");
    if ( $('#result_check').text().length == 0 ) {
        $('.swiper-container').hide();
        $('#label').hide();
    } else {
        $('#questions').hide();
        swiper.slideTo($('#center_slide').index(),0,false);
        var element = document.getElementById("progress_bar");
        var width = 0;
        var identity = setInterval(scene_2, 10);
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
    } else {
        $('#logout').hide();
    }
    var i = 1
    $('#next').click(function(){

        if (i == 1) {
            i = 2
            $('#h2_q1').hide(200);
            $('#h2_q2').show(200);
            $('#questions_1').hide(200);
            $('#questions_2').show(200);
            $('#previous').attr("disabled", false);
            $('#previous').removeClass("disabled");
            var element = document.getElementById("progress_bar");
            var width = 0;
            var identity = setInterval(scene_1, 10);
            function scene_1() {
                if (width >= 33) {
                    clearInterval(identity);
                } else {
                    width++;
                    element.style.width = width + '%';
                };
            }


        } else if (i == 2) {
            i = 3
            $('#h2_q2').hide(200);
            $('#h2_q3').show(200);
            $('#questions_2').hide(200);
            $('#questions_3').show(200);
            $('#next').hide(200);
            var element = document.getElementById("progress_bar");
            var width = 33;
            var identity = setInterval(scene_2, 10);
            function scene_2() {
                if (width >= 66) {
                    clearInterval(identity);
                } else {
                    width++;
                    element.style.width = width + '%';
                };
            }


        } else {
            $('#h2_q3"').hide(200);
            $('#questions_3').hide(200);
        }
    });

    $('#previous').click(function(){

        if (i == 2) {
            i = 1
            $('#h2_q1').show(200);
            $('#h2_q2').hide(200);
            $('#questions_1').show(200);
            $('#questions_2').hide(200);
            $('#previous').attr("disabled", true);
            $('#previous').addClass("disabled");
            var element = document.getElementById("progress_bar");
            var width = 33;
            var identity = setInterval(scene_1, 10);
            function scene_1() {
                if (width <= 0) {
                    clearInterval(identity);
                } else {
                    width--;
                    element.style.width = width + '%';
                };
            }
            
        } else if (i == 3) {
            i = 2
            $('#h2_q2').show(200);
            $('#h2_q3').hide(200);
            $('#questions_2').show(200);
            $('#questions_3').hide(200);
            $('#next').show(200);
            var element = document.getElementById("progress_bar");
            var width = 66;
            var identity = setInterval(scene_1, 10);
            function scene_1() {
                if (width <= 33) {
                    clearInterval(identity);
                } else {
                    width--;
                    element.style.width = width + '%';
                };
            }
        }
            
    });

    $('#submit').click(function(){
        $('#swiper-container').show();
        $('#label').show();
    });
});

/*
$(document).ready(function(){
    // Add smooth scrolling to all links
    $("a").on('click', function(event) {
    
        
        if (this.hash !== "") {
        
        event.preventDefault();
    
        // Store hash
        var hash = this.hash;
    
        // Using jQuery's animate() method to add smooth page scroll
        // The optional number (800) specifies the number of milliseconds it takes to scroll to the specified area
        $('html, body').animate({
            scrollTop: $(hash).offset().top
        }, 800, function(){
    
            // Add hash (#) to URL when done scrolling (default click behavior)
            window.location.hash = hash;
        });
        } // End if
    });
    });
*/