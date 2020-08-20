function change_profile_pic(item, pic_id){
    $.ajax({
        type: 'GET',
        url: `/ajax/update_profile_pic/${pic_id}`,
        success: function(resp){
            $("#profilePicSelect").modal('close')
            $('#selectedImage').attr("src",resp.new_image);
        },
    });
}