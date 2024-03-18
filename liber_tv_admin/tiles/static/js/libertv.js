var libertv = {

    create_accord_item: function (parent, classname, i, id, name) {
        var div_card = $("<div/>");
        div_card.addClass("card");
        div_card.addClass("card_"+classname);
        div_card.attr("id", "series"+id);

        // header
        var div_card_header = $("<div/>");
        div_card_header.addClass("card-header");
        var div_card_header_button = $("<button/>");
        div_card_header_button.addClass("d-inline btn btn-link w-80 ltv_list_series");
        div_card_header_button.html(name);
        div_card_header.append(div_card_header_button);
        div_card.append(div_card_header);

        //body
        var div_card_body_wrapper = $("<div/>");
        div_card_body_wrapper.addClass("collapse");
        if(i==0) {
            div_card_body_wrapper.addClass("show");
        }
        var div_card_body = $("<div/>");
        div_card_body.addClass("card-body");
        div_card_body_wrapper.append(div_card_body);
        div_card.append(div_card_body_wrapper);

        parent.append(div_card);

    },
    init: function () {
        $('.ltv_list_subcategory').click(function(){
            $('#accordion2').empty();
            $.ajax({url: "/series/"+$(this).data('category-id'), success: function(result){
                for(var i in result.series) {
                    libertv.create_accord_item(
                        $('#accordion2'), 'series', i, result.series[i]["id"], result.series[i]["name"]
                    );
                };
            }});
            $.ajax({url: "/items/"+$(this).data('category-id'), success: function(result){
                for(var i in result.series) {
                    libertv.create_accord_item(
                        $('#accordion2'), 'items', i, result.series[i]["id"], result.series[i]["name"]
                    );
                };
            }});
        });
        $('.ltv_edit_subcategory').click(function() {
            alert($(this).data('category-chld'));
        });
        $('.ltv_add_subcategory').click(function() {
            $('.accordion-collapse').removeClass('show');
            $('#category_form_header').addClass('show');
            $('#category_parent').html($(this).data('category-name'));
            $('#id_parent').val($(this).data('category-id'));
            $('#id_position').val($(this).data('category-chld'));
            $('#id_name').val("");
        });
        $('.ltv_add_series').click(function() {
            $('.accordion-collapse').removeClass('show');
            $('#series_form_header').addClass('show');
            $('#series_category').html($(this).data('category-name'));
            $('#items_form #id_category').val($(this).data('category-id'));
        });
        $('.ltv_add_item').click(function() {
            $('.accordion-collapse').removeClass('show');
            $('#items_form_header').addClass('show');
            $('#items_form #id_category').val($(this).data('category-id'));
        });
        $('#series_form_submit').click(function(){
            fields = {}
            $('#series_form input').each(function(){
                if($(this).val()) {
                    fields[$(this).attr("name")] = $(this).val();
                }
            });
            $.ajax({
                url: "/series/", type: "POST",
                dataType: "json", data: fields,
                success: function(result){
                    alert(result.items);
                },
                error: function(result) {
                    alert(result.error);
                }
            });
            console.log(fields);
        });
        $('#items_form_submit').click(function(){
            fields = {}
            $('#items_form input').each(function(){
                if($(this).val()) {
                    fields[$(this).attr("name")] = $(this).val();
                }
            });
            $.ajax({
                url: "/items/", type: "POST",
                dataType: "json", data: fields,
                //contentType: "application/json",
                success: function(result){
                    alert(result.items);
                },
                error: function(result) {
                    alert(result.error);
                }
            });
            console.log(fields);
        });
    }
};

$(document).ready(function(){
    libertv.init();
});