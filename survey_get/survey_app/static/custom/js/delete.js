


document.addEventListener('DOMContentLoaded', () => {
    const deleteButtons = document.querySelectorAll('.delete-btn');
    const deleteModal = document.getElementById('deleteModal');
    const confirmDeleteBtn = document.getElementById('confirmDeleteBtn');
    const record_name_to_delete = document.getElementById('record_name_to_delete');
    const closeModalBtn = document.getElementById('closeModalBtn');
    const cancelBtn = document.getElementById('cancelBtn');
  
    // Show the modal when a delete button is clicked
    deleteButtons.forEach((button) => {
      button.addEventListener('click', (event) => {
        event.preventDefault();
  
        // Get user data from the button's attributes
        const href = button.getAttribute('data-href');
        const record_name = button.getAttribute('data-record-name');
  
        // Update modal content
        record_name_to_delete.textContent = record_name;
  
        // Set the confirm button's href
        confirmDeleteBtn.href = href;
  
        // Show the modal
        deleteModal.classList.add('show');
      });
    });
  
    // Close modal on close or cancel buttons
    [closeModalBtn, cancelBtn].forEach((btn) =>
      btn.addEventListener('click', () => {
        deleteModal.classList.remove('show');
      })
    );
  
    // Close modal when clicking outside the modal content
    window.addEventListener('click', (event) => {
      if (event.target === deleteModal) {
        deleteModal.classList.remove('show');
      }
    });
  });
  
  
  
  
  