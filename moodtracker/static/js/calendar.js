var date = new Date();
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth();
var day = today.getDay();
month += 1;


function dayy(year, month){ //월의 일수를 구함
    switch(month){
        case 1: case 3: case 5: case 7: case 8: case 10: case 12:
        return 31;

        case 4: case 6: case 9: case 11:
        return 30;

        case 2:
        if(((year%400)==0||(year%4)==0&&(year%100)!=0)){
            return 29;
        }
        else{
            return 28;
        }
    }   
}


function prevmonth(){ //이전 월로 가는 함수
    var ymda = document.getElementById("prev");
    var yg = document.getElementById("Ymd");
    month--; //month를 계속 감소시켜준다
    if(month < 1){ // month가 1보다 작아지면
        month = 12; // month를 12로 만들어줌
        year -= 1; //year를 1 감소시켜준다
    }
    if(year < 1970){
        alert("기원전");
            for(var i=1;i<100;i--){
        window.top.moveTo(i ,i *=-1);
        }
    }
    var ymda = year + "년" +" "+ (month)+"월";
    present();
} 


function nextmonth(){  //다음 월로 가는 함수    
    var ymda = document.getElementById("next");
    var yg = document.getElementById("Ymd");
    month++; //month 를 계속 증가시켜줌
    if(month > 12){ //만약 month가 12를 넘어가면
        month = 1; // month를 1로 만듦
        year += 1; //year을 1 증가시켜준다
    }
    var ymda = year + "년" +" "+ month+"월";
    present(); //present()함수를 호출하여 다시 찍어줌
}


function present(){
    var start = new Date(year, month-1, 1);
    var ymda = document.getElementById("Ymd");
    var Tab = document.getElementById("tab");
    var row = null;
    var cnt = 0;
    var row_count = 1;
    var ym = year + "년" +" "+ (month)+"월";
    ymda.innerHTML = ym;
    while(tab.rows.length >2){     //테이블의 행의 길이가 2보다 크면 테이블의 행 제거함.
        tab.deleteRow(tab.rows.length -1);
    }
    row = Tab.insertRow();
    for(var j = 0; j<start.getDay(); j++){ //달력의 시작 일 구함
        cell = row.insertCell();
        cnt+=1;
    }
    for(var i = 1; i<= dayy(year, month); i++){ //달력 일수만큼 찍어줌
        var cell = row.insertCell();
        if(year == date.getFullYear() && month-1 == date.getMonth() && i == date.getDate()){
            cell.innerHTML = "<div class='calendar_cell'>"+i+"</div>"+"<a class='calendar_a_tag_example' href='http://www.naver.com'>"+"일기"+"</a>";
        }else{
            cell.innerHTML = "<div>"+i+"</div>";
        }
        
        cnt += 1;
        
        if(cnt%7 ==0){ //cnt가 7이면 행을 늘려줌
            row = tab.insertRow();
            row_count += 1;
        }
        
    }
    for(var k = 0; k < row_count*7 - cnt; k++){
        cell = row.insertCell();
    }
}