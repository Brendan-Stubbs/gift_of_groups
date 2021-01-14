function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}


function vote_for_gift_ajax(idea_id) {
    let data = {
        id: idea_id
    }

    $.ajax({
        type: 'GET',
        url: '/ajax/vote_for_gift/' + idea_id + '/',
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function (resp) {
            update_votes(resp, idea_id)
        },
    });
}

function invite_to_gift_ajax(gift_id) {
    let data = new FormData(document.getElementById('non-group-form'));
    data.append('gift_id', gift_id)

    $.ajax({
        type: 'POST',
        url: `/ajax/invite_to_gift/${gift_id}/`,
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function (resp) {
            $("#invite_message").text(resp.message).show()
            $('#non-group-form').trigger("reset");
        },
    });
}


function update_votes(resp, idea_id) {
    $(`#vote_counter${idea_id}`).text(resp.total_votes)
    $(`#vote_button${idea_id}`).removeClass("clickable white-text").addClass("grey-text")
}

function add_suggestion_ajax(gift_id, user_id) {
    $('#suggestion-messages').text('')
    let data = new FormData(document.getElementById('suggestionForm'));
    data.append('user_id', user_id)
    data.append('gift_id', gift_id)
    $.ajax({
        type: 'POST',
        url: '/ajax/add_gift_suggestion/',
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function (resp) {
            $('#giftSuggestions').empty().append(resp.gift_suggestion_component)
            $('#suggestion-messages').attr('class', 'green-text').text(resp.message)
            $('input', '#suggestionForm').val('');
            $('textarea', '#suggestionForm').val('');
        },
        error: function (resp) {
            alert(resp.message)
            $('#suggestion-messages').attr('class', 'red-text').text("There was an error please ensure you are logged in");
        }
    })
}

function clearForm(form_id) {
    $('input', '#suggestionForm').val('');
    $('textarea', '#suggestionForm').val('');
}


function mark_gift_complete(gift_id) {
    window.location.replace(`/mark_gift_complete/${gift_id}`);
}


function mark_as_paid() {
    $('#id_has_made_payment').prop("checked", true).trigger('change')
}


function ajax_update_user_gift_form(gift_relation_id) {
    $('#user_gift_detail_success').attr('class', 'hidden-message green-text')
    let data = new FormData(document.getElementById('user_gift_detail_form'));
    data.append('gift_relation_id', gift_relation_id)
    $.ajax({
        type: 'POST',
        url: `/ajax/update_user_gift_relation/`,
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        beforeSend: function () {
            $('#participation_spinner').removeClass('fas fa-check').addClass('fas fa-circle-notch fa-spin').css('display', 'inline-block');
            $('#contribution_spinner').removeClass('fas fa-check').addClass('fas fa-circle-notch fa-spin').css('display', 'inline-block');
            $('#receiver_message_spinner').removeClass('fas fa-check').addClass('fas fa-circle-notch fa-spin').css('display', 'inline-block');


        },
        success: function (resp) {
            $('#user_gift_detail_success').removeClass('hidden-message')
            $('#target-details').empty().append(resp.gift_progress_component)
            $('#participation_spinner').removeClass('fas fa-circle-notch fa-spin').addClass('fas fa-check').css('display', 'inline-block');
            $('#contribution_spinner').removeClass('fas fa-circle-notch fa-spin').addClass('fas fa-check').css('display', 'inline-block');
            if (resp.has_made_payment) {
                $('#notify-button').attr('disabled', true);
            }
        },
        error: function (resp) {
            alert("There was an error saving your changes, please refresh the page and try again")
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
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function (resp) {
            $("#comment_list").empty().append(resp.comments_component)
            $('#id_content').val('');
        },
        error: function (resp) {
            alert("There was an error posting you comment, please refresh the page or try again later")
        }
    })
}

function refresh_comments(gift_id) {
    $.ajax({
        type: 'GET',
        url: `/ajax/get_comments/${gift_id}/`,
        beforeSend: function () {
            $("#comments-refresh").hide()
            $("#comments-loading").show()
        },
        complete: setTimeout(function () {
            $("#comments-loading").hide()
            $("#comments-refresh").show()
        }, 1000),
        success: function (resp) {
            $("#comment_list").empty().append(resp.comments_component)
        },
    })
}

function ajax_confirm_payment(relation_id) {
    $.ajax({
        type: 'GET',
        url: `/ajax/captain_confirm_payment/${relation_id}/`,
        success: function (resp) {
            $("#captain_management_component").empty().append(resp.captain_management_component)
            $('#target-details').empty().append(resp.gift_progress_component)
        },
    })
}

function ajax_update_email_notifications(relation_id) {
    let data = new FormData(document.getElementById('comment_form'))
    $.ajax({
        type: 'POST',
        url: `/ajax/update_email_notifications/${relation_id}/`,
        dataType: 'json',
        data: data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function (resp) {
            // do something
        }
    })
}

$(document).ready(function () {
    let invite_link = $('#inviteLink')

    $('select').formSelect();
    $("#suggestionForm").submit(function (event) {
        event.preventDefault();
    })
    $("#user_gift_detail_form").submit(function (event) {
        event.preventDefault();
    })
    $("#comment_form").submit(function (event) {
        event.preventDefault();
    })
    $("#non-group-form").submit(function (event) {
        event.preventDefault();
    })
    $('#inviteLinkBtn').click(function (event) {
        invite_link.css('display', 'block');
        document.querySelector("#inviteLink").select();
        let copied = document.execCommand("copy");
        invite_link.css('display', 'none');

        if (copied) {
            alert("Link copied to clipboard")
        }
    });
});