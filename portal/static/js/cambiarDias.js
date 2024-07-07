function mostrarClases(dia) {
    document.querySelectorAll('.tabla').forEach(tabla => {
        tabla.style.display = 'none';
    });
    document.getElementById(`clases-${dia}`).style.display = 'flex';
}