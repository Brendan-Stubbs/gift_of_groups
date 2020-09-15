let current_displayed_month = new Date().getMonth()
let months_from_now = 0;
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let dayPerMonth = ["31", get_feb_number_of_days(),"31","30","31","30","31","31","30","31","30","31"];

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

function get_feb_number_of_days(){
    today = new Date()
    year = today.getFullYear()
    if (today.getMonth() >= 1){
        year += 1;
    }
    if((year%100!=0) && (year%4==0) || (year%400==0)){
        return '29'
     }
     return '28'
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

function populate_calendar_with_month(month) {
    let year_to_display = new Date().getFullYear()
    if (month > 11){year_to_display ++;}
    month = month % 11
    let total_days = new Date(year_to_display, month + 1, 0).getDate()
    let starting_weekday = new Date(year_to_display, month, 1).getDay()
    let calendarContent = ""
}

$(document).ready(function () {
    $('#monthName').text(monthNames[current_displayed_month])
    $("#right-button").click(increment_month)
    $("#left-button").click(decrement_month)
    check_buttons()

    populate_calendar_with_month(new Date().getMonth())
});