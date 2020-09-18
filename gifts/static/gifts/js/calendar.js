let current_displayed_month = new Date().getMonth()
let months_from_now = 0;
const monthNames = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
let dayPerMonth = ["31", get_feb_number_of_days(),"31","30","31","30","31","31","30","31","30","31"];

function increment_month() {
    if (months_from_now < 11) {
        $('#monthName').text(monthNames[++current_displayed_month%12]);
        months_from_now ++;
        check_buttons()
        populate_calendar_with_month(current_displayed_month);
    }
}

function decrement_month() {
    if (months_from_now >= 0){
        $('#monthName').text(monthNames[--current_displayed_month%12]);
        months_from_now --;
        check_buttons();
        populate_calendar_with_month(current_displayed_month);
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
    let current_weekday = new Date(year_to_display, month, 1).getDay()
    let current_day = 1
    let calendarContent = "<tr><td>S</td><td>M</td><td>T</td><td>W</td><td>T</td><td>F</td><td>S</td></tr>"
    let day_countdown = current_weekday;

    while(day_countdown-- > 0){
        calendarContent += '<td class="empty-day"></td>'
    };

    while(current_day <= total_days){
        if(current_weekday > 6){
            current_weekday = 0;
        };

        
        if (current_weekday===0 && current_day < total_days+1 && current_day !== 1){
            calendarContent += "<tr>";
        };

        let date_string = `${year_to_display}-${month+1}-${current_day}`
        if (birthdays.includes(date_string)){
            calendarContent += `<td class="birthday calendar-day"><a href="#bdayModal${date_string}" class="modal-trigger anchor-black">${current_day}</a></td>`;
        }else {
            calendarContent += `<td class="calendar-day">${current_day}</td>`;
        }

        current_day++;
        current_weekday++;
    };

    if (current_day!=0){
        calendarContent += '</tr>'
    };
    $('#calendarBody').empty();
    $('#calendarBody').append(calendarContent);
}

$(document).ready(function () {
    $('#monthName').text(monthNames[current_displayed_month])
    $("#right-button").click(increment_month)
    $("#left-button").click(decrement_month)
    check_buttons()

    populate_calendar_with_month(new Date().getMonth())
});