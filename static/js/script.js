$(document).ready(function() {
    $('#questions_2').hide();
    $('#questions_3').hide();
    var i = 1
    $('#next').click(function(){

        if (i == 1) {
            i = 2
            $('#questions_1').hide(300);
            $('#questions_2').show(300);
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
            $('#questions_2').hide(300);
            $('#questions_3').show(300);
            $('#next').hide(300);
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
            $('#questions_3').hide(300);
        }
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