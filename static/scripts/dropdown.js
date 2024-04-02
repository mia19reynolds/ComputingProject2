document.addEventListener("DOMContentLoaded", function() {

    var dropdowns = document.getElementsByClassName('dropdown');
    for(var i=0; i<dropdowns.length; i++){
        dropdowns[i].getElementsByClassName('anchor')[0].onclick = function(evt) {
            if (this.parentElement.classList.contains('visible')){
                this.parentElement.classList.remove('visible');
            }else{
                this.parentElement.classList.add('visible');
            }
        }
    }
});