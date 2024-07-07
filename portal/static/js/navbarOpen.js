document.getElementById('toggleAside').addEventListener('click', function(event) {
    var aside = document.getElementById('nav');
    aside.classList.toggle('active');
    event.stopPropagation();
});

document.addEventListener('click', function(event) {
    var aside = document.getElementById('nav');
    var toggleButton = document.getElementById('toggleAside');
    
    if (!aside.contains(event.target) && !toggleButton.contains(event.target)) {
        aside.classList.remove('active');
    }
});