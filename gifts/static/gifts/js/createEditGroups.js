function select_icon(item, icon){
    $('#current-icon').removeClass().addClass(icon).addClass("xl-group-icon purple-text");
    $('#icon-options i').each(function(){
        $(this).removeClass("selected-icon").addClass("purple-text");

    });
    item.classList.add("selected-icon");
    item.classList.remove("purple-text");
    $("#id_icon").val(icon)
}