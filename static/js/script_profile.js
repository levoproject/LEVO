$(document).ready(function() {
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

    $('.outer > h1').click(function() {
        if ($(this).next().is(":hidden") && parseInt($(this).attr("data-count")) != 0) {
            $(this).next().show(150);
        } else {
            $(this).next().hide(150);
        }
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

});