function refresh_gifts_ajax(group_id){
    $.ajax({
        type: 'GET',
        url: `/ajax/refresh_gifts/${group_id}/`,
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


function ajax_post_comment(group_id) {
    let data = new FormData(document.getElementById('comment_form'));
    data.append('group_id', group_id)
    $.ajax({
        type: 'POST',
        url: `/ajax/post_group_comment/${group_id}/`,
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            $("#comment_list").empty().append(resp.comments_component)
            $('#id_content').val('');
        },
        error: function(resp){
            alert("There was an error posting you comment, please refresh the page or try again later")
        }
    })
}

function refresh_comments(group_id) {
    $.ajax({
        type: 'GET',
        url: `/ajax/get_group_comments/${group_id}/`,
        beforeSend: function(){
            $("#comments-refresh").hide()
            $("#comments-loading").show()
        },
        complete: setTimeout(function(){
            $("#comments-loading").hide()
            $("#comments-refresh").show()
        }, 1000),
        success: function(resp){
            $("#comment_list").empty().append(resp.comments_component)
        },
    })
}

$("#comment_form").submit(function(event) {
        event.preventDefault();
})