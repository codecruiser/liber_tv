var libertv = {

    create_accord_item: function (parent, classname, i, id, name) {
        console.log(i+":"+name);
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
        var div_edit_icon = $("<div/>");
        div_edit_icon.addClass("d-inline ltv_edit_"+classname);
        div_edit_icon.attr("data-"+classname+"-id", id);
        div_edit_icon.attr("data-"+classname+"-name", name);
        div_edit_icon.html('<i class="fa fa-pencil-square-o fa-fw" aria-hidden="true"></i>');
        div_card_header.append(div_edit_icon);
        if(classname=="series") {
            var div_add_sibl_icon = $("<div/>");
            div_add_sibl_icon.addClass("d-inline ltv_add_sibl_"+classname);
            div_add_sibl_icon.attr("data-"+classname+"-id", id);
            div_add_sibl_icon.attr("data-"+classname+"-name", name);
            div_edit_icon.html('<i class="fa fa-plus-square fa-fw" aria-hidden="true"></i>');
            div_card_header.append(div_add_sibl_icon);

            var div_add_icon = $("<div/>");
            div_add_icon.addClass("d-inline ltv_add_"+classname);
            div_add_icon.attr("data-"+classname+"-id", id);
            div_add_icon.attr("data-"+classname+"-name", name);
            div_edit_icon.html('<i class="fa fa-plus-circle fa-fw" aria-hidden="true"></i>');
            div_card_header.append(div_add_icon);
        };
        div_card.append(div_card_header);

        //body
        var div_card_body_wrapper = $("<div/>");
        div_card_body_wrapper.addClass("collapse");
        if(i==0) {
            div_card_body_wrapper.addClass("show");
        }
        if(classname=="series") {
            var div_card_body = $("<div/>");
            div_card_body.addClass("card-body");
            div_card_body_wrapper.append(div_card_body);
            div_card.append(div_card_body_wrapper);
        }
        parent.append(div_card);
    },
    init: function () {
        $('.ltv_list_subcategory').click(function(){
            $('#accordion2').empty();
            $.ajax({url: "/series/"+$(this).data('category-id'), success: function(result){
                for(var i in result.series) {
                    libertv.create_accord_item(
                        $('#accordion2'), 'series', i, result.series[i]["id"], result.series[i]["name"],
                        result.series[i]["children"]
                    );
                };
            }});
            $.ajax({url: "/items/"+$(this).data('category-id'), success: function(result){
                for(var i in result.items) {
                    libertv.create_accord_item(
                        $('#accordion2'), 'items', i, result.items[i]["id"], result.items[i]["title"]
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