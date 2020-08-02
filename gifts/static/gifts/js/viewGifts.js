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
            add_new_suggestion_to_list(resp);
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

function add_new_suggestion_to_list(resp){
    $('#ideas-collection').append(`
        <li class="collection-item idea-item avatar blue lighten-1">
            <span class="title">${resp.title}</span>
            <span class="amber-text">R${resp.price}</span>
            <p class="idea-description">${resp.description}</p>
            <div class="secondary-content">
              <i id="vote_button${resp.id}" onclick="vote_for_gift_ajax('${resp.id}');" class="material-icons white-text clickable">thumb_up</i>
              <span id="vote_counter${resp.id}"class="white-text">0</span>
            </div>
        </li>
        `
    )
}

function clearForm(form_id){
    $('input', '#suggestionForm').val('');
    $('textarea', '#suggestionForm').val('');
}

$(document).ready(function() { 
    $('select').formSelect();
    $("#suggestionForm").submit(function(event) { 
        event.preventDefault();
    })
});
