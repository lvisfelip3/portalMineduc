document.querySelectorAll('.hora').forEach(hora => {
    hora.addEventListener('mouseover', () => {
        const parentRow = hora.closest('tr');
        parentRow.querySelectorAll('.conRamo, .sinRamo, .hora').forEach(cell => {
            cell.classList.add('highlight');
        });
    });
    
    hora.addEventListener('mouseout', () => {
        const parentRow = hora.closest('tr');
        parentRow.querySelectorAll('.conRamo, .sinRamo, .hora').forEach(cell => {
            cell.classList.remove('highlight');
        });
    });
});

document.querySelectorAll('th').forEach(th => {
    const index = Array.from(th.parentNode.children).indexOf(th);

    th.addEventListener('mouseover', () => {
        document.querySelectorAll(`tbody tr td:nth-child(${index + 1}) .conRamo`).forEach(cell => {
            cell.classList.add('sinRamoHover');
        });
    });
    
    th.addEventListener('mouseout', () => {
        document.querySelectorAll(`tbody tr td:nth-child(${index + 1}) .conRamo`).forEach(cell => {
            cell.classList.remove('sinRamoHover');
        });
    });
});
