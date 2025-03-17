document.addEventListener('DOMContentLoaded', function() {
    // Get all tab links
    const tabLinks = document.querySelectorAll('.profile-nav .nav-link');
    
    // Get all content sections
    const contentSections = document.querySelectorAll('#recipes, #favorites, #reviews');
    
    // Add click event listener to each tab link
    tabLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Remove active class from all links
            tabLinks.forEach(l => l.classList.remove('active'));
            
            // Add active class to clicked link
            this.classList.add('active');
            
            // Get the target section ID
            const targetId = this.getAttribute('href').substring(1);
            
            // Hide all content sections
            contentSections.forEach(section => {
                section.classList.add('d-none');
            });
            
            // Show the target section
            document.getElementById(targetId).classList.remove('d-none');
        });
    });
    
    // Set the first tab (Recipes) as active by default
    tabLinks[0].classList.add('active');
    document.getElementById('recipes').classList.remove('d-none');
    
    // Check if there's a hash in the URL and activate the corresponding tab
    if (window.location.hash) {
        const hash = window.location.hash.substring(1);
        const tabLink = document.querySelector(`.profile-nav .nav-link[href="#${hash}"]`);
        if (tabLink) {
            tabLink.click();
        }
    }
});