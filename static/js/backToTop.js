// Back to Top Button functionality
document.addEventListener('DOMContentLoaded', function() {
    const backToTopBtn = document.getElementById('backToTopBtn');
    
    // Show/hide button based on scroll position
    window.onscroll = function() {
      if (document.body.scrollTop > 200 || document.documentElement.scrollTop > 200) {
        backToTopBtn.style.display = 'block';
      } else {
        backToTopBtn.style.display = 'none';
      }
    };
    
    // Scroll to top when button is clicked
    backToTopBtn.addEventListener('click', function() {
      // Smooth scroll to top
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });
    });
  });