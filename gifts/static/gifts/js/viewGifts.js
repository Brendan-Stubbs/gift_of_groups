function vote_for_gift_ajax(idea_id){
    let data = {id:idea_id}

    $.ajax({
        type: 'GET',
        url: '/ajax/vote_for_gift/' + idea_id + '/',
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            update_votes(resp, idea_id)
        },
    });
}


function update_votes(resp, idea_id){
    $(`#vote_counter${idea_id}`).text(resp.total_votes)
    $(`#vote_button${idea_id}`).removeClass("clickable white-text").addClass("grey-text")
}