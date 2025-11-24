document.addEventListener('DOMContentLoaded', function () {
  var detailModal = document.getElementById('detailModal');
  if (!detailModal) return;

  detailModal.addEventListener('show.bs.modal', function (event) {
    var button = event.relatedTarget;
    var id = button.getAttribute('data-order-id');
    var title = button.getAttribute('data-order-title');
    var desc = button.getAttribute('data-order-desc');
    var user = button.getAttribute('data-order-user');
    var status = button.getAttribute('data-order-status');

    var html = `
      <h5 class="mb-1">${title} <small class="text-muted">#${id}</small></h5>
      <div class="small text-muted mb-2">Solicitante: ${user}</div>
      <div class="mb-3"><strong>Descrição</strong><p class="mb-0">${desc}</p></div>
      <div><strong>Status:</strong> ${status}</div>
    `;
    document.getElementById('ticketDetails').innerHTML = html;

    var statusForm = document.getElementById('statusForm');
    if (statusForm) {
      statusForm.action = '/update_status/' + id;
      // pre-select current status
      var sel = statusForm.querySelector('select[name="status"]');
      if (sel) {
        for (var i=0;i<sel.options.length;i++){
          if(sel.options[i].value === status) sel.selectedIndex = i;
        }
      }
    }
  });
});


document.addEventListener('DOMContentLoaded', function() {
  var searchInput = document.getElementById('searchInput');
  var table = document.getElementById('ticketsTable');
  if (!searchInput || !table) return;

  searchInput.addEventListener('input', function() {
    var filter = searchInput.value.toLowerCase();
    var rows = table.getElementsByTagName('tbody')[0].getElementsByTagName('tr');

    Array.from(rows).forEach(function(row) {
      var cells = row.getElementsByTagName('td');
      var match = false;

      Array.from(cells).forEach(function(cell) {
        if (cell.textContent.toLowerCase().indexOf(filter) > -1) {
          match = true;
        }
      });

      row.style.display = match ? '' : 'none';
    });
  });
});
