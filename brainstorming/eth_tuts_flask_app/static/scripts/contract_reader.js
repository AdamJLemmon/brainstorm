var xmlhttp = new XMLHttpRequest();

xmlhttp.onreadystatechange = function(){
    if(xmlhttp.status == 200 && xmlhttp.readyState == 4){
        var source = xmlhttp.responseText;
    }
};

xmlhttp.open("GET","read_my_token",true);
xmlhttp.send();