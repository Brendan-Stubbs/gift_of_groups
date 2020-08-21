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

function invite_to_gift_ajax(gift_id){
    let data = new FormData(document.getElementById('non-group-form'));
    data.append('gift_id', gift_id)

    $.ajax({
        type: 'POST',
        url: `/ajax/invite_to_gift/${gift_id}/`,
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            $("#invite_message").text(resp.message).show()
            $('#non-group-form').trigger("reset");
        },
    });
}


function update_votes(resp, idea_id){
    $(`#vote_counter${idea_id}`).text(resp.total_votes)
    $(`#vote_button${idea_id}`).removeClass("clickable white-text").addClass("grey-text")
}

function add_suggestion_ajax(gift_id, user_id){
    $('#suggestion-messages').text('')
    let data = new FormData(document.getElementById('suggestionForm'));
    data.append('user_id', user_id)
    data.append('gift_id', gift_id)
    $.ajax({
        type: 'POST',
        url: '/ajax/add_gift_suggestion/',
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            $('#giftSuggestions').empty().append(resp.gift_suggestion_component)
            $('#suggestion-messages').attr('class', 'green-text').text(resp.message)
            $('input', '#suggestionForm').val('');
            $('textarea', '#suggestionForm').val('');
        },
        error: function(resp){
            alert(resp.message)
            $('#suggestion-messages').attr('class', 'red-text').text("There was an error please ensure you are logged in");
        }
    })
}

function clearForm(form_id){
    $('input', '#suggestionForm').val('');
    $('textarea', '#suggestionForm').val('');
}


function mark_gift_complete(gift_id){
    window.location.replace(`/mark_gift_complete/${gift_id}`);
}


function mark_as_paid(){
    $('#id_has_made_payment').prop("checked", true).trigger('change')
}


function ajax_update_user_gift_form(gift_relation_id){
    $('#user_gift_detail_success').attr('class', 'hidden-message green-text')
    let data = new FormData(document.getElementById('user_gift_detail_form'));
    data.append('gift_relation_id', gift_relation_id)
    $.ajax({
        type: 'POST',
        url: `/ajax/update_user_gift_relation/`,
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            $('#user_gift_detail_success').removeClass('hidden-message')
            $('#target-details').empty().append(resp.gift_progress_component)
        },
        error: function(resp){
            alert("There was an error saving your changes, please refresh the page")
        }
    })
}


function ajax_post_comment(gift_id) {
    let data = new FormData(document.getElementById('comment_form'));
    data.append('gift_id', gift_id)
    $.ajax({
        type: 'POST',
        url: `/ajax/post_gift_comment/${gift_id}/`,
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            update_comments(resp.comments)
            $('#id_content').val('');
        },
        error: function(resp){
            alert("There was an error posting you comment, please refresh the page or try again later")
        }
    })
}

function refresh_comments(gift_id) {
    $.ajax({
        type: 'GET',
        url: `/ajax/get_comments/${gift_id}/`,
        beforeSend: function(){
            $("#comments-refresh").hide()
            $("#comments-loading").show()
        },
        complete: setTimeout(function(){
            $("#comments-loading").hide()
            $("#comments-refresh").show()
        }, 1000),
        success: function(resp){
            update_comments(resp.comments)
        },
    })
}

function update_comments(comments){
    let existing_comments = []
    $('#comment-list li').each(function(){
        existing_comments.push(this.id);
    })

    comments.forEach(function(comment){
        if (!existing_comments.includes(`comment${comment.id}`)){
            let options = { year: 'numeric', month: 'short', day: 'numeric', hour: "2-digit", minute:"2-digit" };
            comment.formatted_date = new Date(comment.created_at).toLocaleDateString("en-us", options)
            $("#comment-list").prepend(
                `
                <li id="comment${comment.id}"class="collection-item avatar">
                    <img src="/static/gifts/images/avatar_placeholder.png" alt="" class="circle">
                    <p>${comment.content}.</p>
                    <small>${comment.first_name} ${comment.last_name} ${comment.formatted_date}</small>
                </li>
                `
            )
        }
    })
}

$(document).ready(function() { 
    $('select').formSelect();
    $("#suggestionForm").submit(function(event) { 
        event.preventDefault();
    })
    $("#user_gift_detail_form").submit(function(event) { 
        event.preventDefault();
    })
    $("#comment_form").submit(function(event) {
        event.preventDefault();
    })
    $("#non-group-form").submit(function(event) {
        event.preventDefault();
    })
});
