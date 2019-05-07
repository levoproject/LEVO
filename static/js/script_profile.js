$(document).ready(function() {

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