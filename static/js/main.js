document.addEventListener('DOMContentLoaded', function() {
  
  // ----------------- Filter Logic -----------------
  const filterBtns = document.querySelectorAll('.filter-btn');
  const ticketRows = document.querySelectorAll('.ticket-row');

  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        const filterStatus = btn.getAttribute('data-filter');
        const isActive = btn.classList.contains('active');

        // Reset all buttons
        filterBtns.forEach(b => b.classList.remove('active'));

        // If clicking active button, turn it off (show all)
        if (isActive) {
             ticketRows.forEach(row => row.style.display = '');
        } else {
             // Activate button
             btn.classList.add('active');
             
             // Filter rows
             ticketRows.forEach(row => {
                 const rowStatus = row.getAttribute('data-status');
                 if (rowStatus === filterStatus) {
                     row.style.display = '';
                 } else {
                     row.style.display = 'none';
                 }
             });
        }
    });
  });

  // ----------------- Search Logic -----------------
  var searchInput = document.getElementById('searchInput');
  if (searchInput) {
    searchInput.addEventListener('input', function() {
        var filter = searchInput.value.toLowerCase();
        
        ticketRows.forEach(function(row) {
            var text = row.querySelector('.ticket-header').textContent.toLowerCase();
            if (text.indexOf(filter) > -1) {
                row.style.display = '';
            } else {
                row.style.display = 'none';
            }
        });
    });
  }

  // ----------------- File Feedback Logic (New Ticket) -----------------
  const newTicketFile = document.getElementById('newTicketFile');
  const newTicketFileLabel = document.getElementById('newTicketFileLabel');
  
  if(newTicketFile){
      newTicketFile.addEventListener('change', function(){
          if (this.files && this.files.length > 0) {
              newTicketFileLabel.innerHTML = `<strong>Arquivo selecionado:</strong> ${this.files[0].name}`;
              newTicketFileLabel.classList.add('text-success');
          } else {
              newTicketFileLabel.innerHTML = 'Clique para anexar um arquivo';
              newTicketFileLabel.classList.remove('text-success');
          }
      });
  }

  // ----------------- File Feedback Logic (Chat) -----------------
  const chatFileInputs = document.querySelectorAll('.chat-file-input');
  chatFileInputs.forEach(input => {
      input.addEventListener('change', function() {
          const feedbackId = this.getAttribute('data-feedback');
          const feedbackEl = document.getElementById(feedbackId);
          
          if(feedbackEl && this.files && this.files.length > 0) {
              feedbackEl.style.display = 'block';
              feedbackEl.querySelector('.filename').textContent = this.files[0].name;
          } else if (feedbackEl) {
              feedbackEl.style.display = 'none';
          }
      });
  });

});