document.addEventListener("DOMContentLoaded", function() {
     buildCalendar();
});

var today = new Date(); 
var date = new Date(); 

 
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
             // 평일 날짜 데이터 삽입
             column.innerText = autoLeftPad(day, 2);
             // 일요일인 경우
             if(dom % 7 == 1) {
                 column.style.color = "#FF4D4D";
             }
             if(dom % 7 == 0) {
                 column.style.color = "#4D4DFF";
                 row = tbCalendar.insertRow();   // 토요일이 지나면 다시 가로 행을 한줄 추가한다.
             }

         }

         // 평일 전월일과 익월일의 데이터 날짜변경
         else {
             let exceptDay = new Date(doMonth.getFullYear(), doMonth.getMonth(), day);
             column.innerText = autoLeftPad(exceptDay.getDate(), 2);
             column.style.color = "#A9A9A9";
         }

         // 전월, 명월 음영처리
         // 현재년과 선택 년도가 같은경우
         if(today.getFullYear() == date.getFullYear()) {

             // 현재월과 선택월이 같은경우
             if(today.getMonth() == date.getMonth()) {


                 // 현재일보다 이후이면서 현재월에 포함되는 일인경우
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

     // 기존 선택일이 존재하는 경우 기존 선택일의 표시형식을 초기화 한다.
     if(document.getElementsByClassName("choiceDay")[0]) {
         document.getElementsByClassName("choiceDay")[0].style.backgroundColor = "#FFFFFF";
         document.getElementsByClassName("choiceDay")[0].classList.remove("choiceDay");

         var datenum = document.getElementsByClassName("choiceday")[0];
     }

     // 선택일 체크 표시
     column.style.backgroundColor = "#F99B0D";

     // 선택일 클래스명 변경
     column.classList.add("choiceDay");

     if(datenum !==null) {
        document.getElementByID("date-pick") = datenum;
     }

 }

 function autoLeftPad(num, digit) {
     if(String(num).length < digit) {
         num = new Array(digit - String(num).length + 1).join(" ") + num;
     }
     return num;

 }