document.addEventListener("DOMContentLoaded", function() {

    var dropdowns = document.getElementsByClassName('dropdown');
    for(var i=0; i<dropdowns.length; i++){
        dropdowns[i].getElementsByClassName('anchor')[0].onclick = function(evt) {
            console.log('clicked');
            console.log(dropdowns[i].classList)
    
            if (dropdowns[i].classList.contains('visible')){
                dropdowns[i].classList.remove('visible');
            }else{
                dropdowns[i].classList.add('visible');
            }
        }
    }
    

});