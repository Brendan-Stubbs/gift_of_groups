function refresh_gifts_ajax(group_id){

    $.ajax({
        type: 'GET',
        url: `/ajax/refresh_gifts/${group_id}`,
        beforeSend: function(){
            $("#gift-refresh").hide()
            $("#gift-collection-loading").show()
        },
        complete: setTimeout(function(){
            $("#gift-collection-loading").hide()
            $("#gift-refresh").show()
        }, 300),
        success: function(resp){
            $('#gifts-collection').empty().append(resp.group_gifts_component)
        },
    });
}