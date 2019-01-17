
var modal = document.getElementById('myModal');
var modalImg = document.getElementById("img01");
var captionText = document.getElementById("caption");
function imageOnClick(e){    
    modal.style.display = "block";
    modalImg.src = e.src;
    captionText.innerHTML = "";
    $.get("/getcelebrity/"+ e.name, function(data){
        celebrityinfo = $.parseJSON(data)   
        for (i = 0; i < celebrityinfo.length-1; i++){
            celebrityObject = celebrityinfo[i]  
            captionText.innerHTML = captionText.innerHTML + celebrityObject.name + ", " ;
        }
    captionText.innerHTML = captionText.innerHTML + celebrityinfo[celebrityinfo.length-1].name;
    });
}

var span = document.getElementsByClassName("close")[0];

span.onclick = function() { 
    modal.style.display = "none";
}
