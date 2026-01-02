document.addEventListener("DOMContentLoaded", function () {
    const containers = document.querySelectorAll('[data-animate]');
  
    const observer = new IntersectionObserver(
      (entries, observer) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add("visible");
            observer.unobserve(entry.target); 
          }
        });
      },
      {
        threshold: 0.1, // Trigger when 10% of the container is visible
      }
    );
  
    containers.forEach(container => observer.observe(container));

    // Check for elements in the viewport on page load
    containers.forEach(container => {
        if (isInViewport(container)) {
            container.classList.add("visible");
        }
    });

    // Check for elements in the viewport on window resize
    window.addEventListener('resize', () => {
        containers.forEach(container => {
            if (isInViewport(container)) {
                container.classList.add("visible");
            }
        });
    });
});

// Function to check if an element is in the viewport
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}







