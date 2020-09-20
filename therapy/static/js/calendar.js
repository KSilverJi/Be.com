document.addEventListener("DOMContentLoaded", function() {
     buildCalendar();
});

var today = new Date(); 
var date = new Date(); 

//html로 보낼 변수
var datenumber;

 
function prevCalendar() {
     this.today = new Date(today.getFullYear(), today.getMonth() - 1, today.getDate());
     buildCalendar();    // 전월 캘린더 출력 요청
}

 function nextCalendar() {
     this.today = new Date(today.getFullYear(), today.getMonth() + 1, today.getDate());
     buildCalendar();    // 명월 캘린더 출력 요청
 }

 function buildCalendar() {

     let doMonth = new Date(today.getFullYear(), today.getMonth(), 1);
     let lastDate = new Date(today.getFullYear(), today.getMonth() + 1, 0);

     let tbCalendar = document.querySelector(".scriptCalendar > tbody");


     document.getElementById("calYear").innerText = today.getFullYear();
     document.getElementById("calMonth").innerText = autoLeftPad((today.getMonth() + 1), 2);


     //이전 캘린더의 출력결과가 남아있다면, 이전 캘린더를 삭제한다.
     while(tbCalendar.rows.length > 0) {
         tbCalendar.deleteRow(tbCalendar.rows.length - 1);
     }


     let row = tbCalendar.insertRow();

     let dom = 1;

     let daysLength = (Math.ceil((doMonth.getDay() + lastDate.getDate()) / 7) * 7) - doMonth.getDay();

     for(let day = 1 - doMonth.getDay(); daysLength >= day; day++) {

         let column = row.insertCell();

         if(Math.sign(day) == 1 && lastDate.getDate() >= day) {
             column.innerText = autoLeftPad(day, 2);
             if(dom % 7 == 0) {
                 row = tbCalendar.insertRow();
             }

         }

         else {
             let exceptDay = new Date(doMonth.getFullYear(), doMonth.getMonth(), day);
             column.innerText = autoLeftPad(exceptDay.getDate(), 2);
             column.style.color = "#ffffff";
         }

         if(today.getFullYear() == date.getFullYear()) {

             if(today.getMonth() == date.getMonth()) {

                 //현재일보다 이후이면서 현재월에 포함되는 일인경우
                 if(date.getDate() < day && lastDate.getDate() >= day) {
                     column.style.backgroundColor = "#FFFFFF";
                     column.style.cursor = "pointer";
                     column.onclick = function(){ calendarChoiceDay(this); }
                 }

                 //현재일인 경우
                 else if(date.getDate() == day) {
                     column.style.backgroundColor = "#FFFFFF";
                     column.style.cursor = "pointer";
                     column.onclick = function(){ calendarChoiceDay(this); }
                 }

             // 현재월보다 이전인경우
             } else if(today.getMonth() < date.getMonth()) {
                 if(Math.sign(day) == 1 && day <= lastDate.getDate()) {
                     column.style.backgroundColor = "#FFFFFF";
                 }
             }

             // 현재월보다 이후인경우
             else {
                 if(Math.sign(day) == 1 && day <= lastDate.getDate()) {
                     column.style.backgroundColor = "#FFFFFF";
                     column.style.cursor = "pointer";
                     column.onclick = function(){ calendarChoiceDay(this); }
                 }
             }
         }

         // 선택한년도가 현재년도보다 작은경우
         else if(today.getFullYear() < date.getFullYear()) {
             if(Math.sign(day) == 1 && day <= lastDate.getDate()) {
                 column.style.backgroundColor = "#FFFFFF";
             }
         }

         //선택한년도가 현재년도보다 큰경우
         else {
             if(Math.sign(day) == 1 && day <= lastDate.getDate()) {
                 column.style.backgroundColor = "#FFFFFF";
                 column.style.cursor = "pointer";
                 column.onclick = function(){ calendarChoiceDay(this); }
             }
         }
         dom++;
     }
 }

 function calendarChoiceDay(column) {

     // 기존에 선택한 게 있으면 없애기
     if(document.getElementsByClassName("choiceDay")[0]) {
         document.getElementsByClassName("choiceDay")[0].style.backgroundColor = "#FFFFFF";
         document.getElementsByClassName("choiceDay")[0].classList.remove("choiceDay");

     }

     column.style.backgroundColor = "#F99B0D";

     //선택한 날짜에 클래스 지정해서 css 설정
     column.classList.add("choiceDay");
    
     //선택한 날짜 받아서 html로 넘기기
     datenumber = document.getElementsByClassName("choiceDay")[0];
     document.getElementById("date-pick").value = datenumber.innerHTML;

 }


 function autoLeftPad(num, digit) {

     if(String(num).length < digit) {
         num = new Array(digit - String(num).length + 1).join(" ") + num;
     }
     return num;

 }

