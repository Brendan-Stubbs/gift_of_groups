function reject_invite(invite_id){
    let data = {id:invite_id}

    $.ajax({
        type: 'GET',
        url: 'reject_invite/' + invite_id + '/',
        dataType: 'json',
        data:data,
        contentType: false,
        processData: false,
        enctype: 'multipart/form-data',
        success: function(resp){
            hide_rejected_invitation(invite_id)
        },
    });
}


function hide_rejected_invitation(invite_id){
    $(`#invitationItem${invite_id}`).hide();
    $(`#invitationItemMobile${invite_id}`).hide(); 
    $("#invitationCounter").text($("#invitationCounter").text() -1);
}