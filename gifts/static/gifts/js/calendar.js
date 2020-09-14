let current_displayed_month = new Date().getMonth()
let months_from_now = 0;
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
var dayPerMonth = ["31", ""+FebNumberOfDays+"","31","30","31","30","31","31","30","31","30","31"];

function increment_month() {
    if (months_from_now < 11) {
        $('#monthName').text(monthNames[++current_displayed_month%12]);
        months_from_now ++;
        check_buttons()
    }
}

function decrement_month() {
    if (months_from_now >= 0){
        $('#monthName').text(monthNames[--current_displayed_month%12]);
        months_from_now --;
        check_buttons();
    }
}

function disable_button(id) {
    $(`#${id}`).prop('disabled', true)
}

function enable_button(id) {
    $(`#${id}`).prop('disabled', false)
}

function check_buttons() {
    if (months_from_now <= 0){
        disable_button('left-button');
    } else if (months_from_now >= 11){
        disable_button('right-button')
    } else {
        enable_button('left-button')
        enable_button('right-button')
    }
}

$(document).ready(function () {
    $('#monthName').text(monthNames[current_displayed_month])
    $("#right-button").click(increment_month)
    $("#left-button").click(decrement_month)
    check_buttons()
});