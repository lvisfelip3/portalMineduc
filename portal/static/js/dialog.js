
var abrirPopup = document.getElementById("abrirPopup")
var cerrarPopup = document.getElementById("cerrarPopup")
var dialog = document.getElementById("popup")

abrirPopup.addEventListener("click", function(){
    dialog.showModal()
})
dialog.addEventListener('mousedown', function(event) {
    var rect = dialog.getBoundingClientRect();
    var isInDialog = (rect.top <= event.clientY && event.clientY <= rect.top + rect.height &&
      rect.left <= event.clientX && event.clientX <= rect.left + rect.width);
    if (!isInDialog) {
      dialog.close();
    }
  });