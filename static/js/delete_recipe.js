// document.addEventListener('DOMContentLoaded', function() {
//     // Get modal element
//     const deleteModal = document.getElementById('deleteRecipeModal');
    
//     // If using Bootstrap 5
//     const modal = new bootstrap.Modal(deleteModal);
    
//     // Get all delete buttons
//     const deleteButtons = document.querySelectorAll('.delete-recipe-btn');
    
//     // Add click event to all delete buttons
//     deleteButtons.forEach(button => {
//         button.addEventListener('click', function() {
//             const recipeId = this.getAttribute('data-recipe-id');
//             const recipeTitle = this.getAttribute('data-recipe-title');
            
//             // Set the recipe title in the modal
//             document.getElementById('recipe-title-to-delete').textContent = recipeTitle;
            
//             // Set data attribute for the confirm button
//             document.getElementById('confirm-delete-btn').setAttribute('data-recipe-id', recipeId);
            
//             // Show the modal
//             modal.show();
//         });
//     });
    
//     // Add click event to confirm delete button
//     document.getElementById('confirm-delete-btn').addEventListener('click', function() {
//         const recipeId = this.getAttribute('data-recipe-id');
//         deleteRecipe(recipeId);
//     });
    
//     // Function to handle the AJAX delete request
//     function deleteRecipe(recipeId) {
//         // Get CSRF token
//         const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        
//         fetch(`/recipes/recipe/${recipeId}/delete/ajax/`, {
//             method: 'POST',
//             headers: {
//                 'X-CSRFToken': csrftoken,
//                 'X-Requested-With': 'XMLHttpRequest',
//                 'Content-Type': 'application/json'
//             },
//         })
//         .then(response => response.json())
//         .then(data => {
//             if (data.success) {
//                 // Remove the recipe element from the DOM
//                 const recipeElement = document.getElementById(`recipe-${recipeId}`);
//                 recipeElement.remove();
                
//                 // Show success message
//                 showAlert('success', data.message);
//             } else {
//                 // Show error message
//                 showAlert('danger', data.error);
//             }
            
//             // Hide the modal
//             modal.hide();
//         })
//         .catch(error => {
//             console.error('Error:', error);
//             showAlert('danger', 'An error occurred while deleting the recipe.');
//             modal.hide();
//         });
//     }
    
//     // Function to show alert messages
//     function showAlert(type, message) {
//         const alertDiv = document.createElement('div');
//         alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
//         alertDiv.role = 'alert';
//         alertDiv.innerHTML = `
//             ${message}
//             <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
//         `;
        
//         // Insert at the top of the content area
//         document.querySelector('.recipe-list').before(alertDiv);
        
//         // Auto dismiss after 5 seconds
//         setTimeout(() => {
//             alertDiv.classList.remove('show');
//             setTimeout(() => alertDiv.remove(), 150);
//         }, 5000);
//     }
// });