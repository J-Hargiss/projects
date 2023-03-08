var plant1= document.querySelector(".plants1");
var cookie= document.querySelector(".cookies");

function change(element) {
    plant1.src = "./assets/succulents-2.jpg";
}

function changeBack(element) {
    plant1.src = "./assets/succulents-1.jpg";
}
function hide() {
    cookie.remove();
}