document.addEventListener('DOMContentLoaded', function() {
  const currentPage = window.location.pathname.split('/').pop() || 'index.html';
  const navLinks = document.querySelectorAll('.nav-link');
  
  navLinks.forEach(link => {
    const linkPage = link.getAttribute('href').split('/').pop();
    if (currentPage === linkPage) {
      link.classList.add('active');
    }
  });
});


  function toggleForm() {
        const formDiv = document.getElementById("addProductForm");
        formDiv.style.display = formDiv.style.display === "none" ? "block" : "none";
    }
