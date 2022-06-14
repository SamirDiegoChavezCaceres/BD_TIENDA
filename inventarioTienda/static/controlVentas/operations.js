window.addEventListener('load', restar);
//https://stackoverflow.com/questions/10694661/document-getelementbyid-value-return-undefined-in-chrome
//ctrl + F5 https://stackoverflow.com/questions/52682812/django-css-not-updating
function restar(){
    var min = document.getElementById("minuendo").innerHTML.replace(",",".");
    var sus = document.getElementById("sustraendo").innerHTML.replace(",",".");
    console.log(min+"a");
    console.log(sus);

    
    var res = min - sus;
    console.log(res);
    document.getElementById("resultado").innerHTML = res;
}
