document.addEventListener("DOMContentLoaded", function () {
    const services = document.querySelectorAll(".service");

    const observer = new IntersectionObserver(
        (entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    entry.target.classList.add("show");
                }
            });
        },
        { threshold: 0.3 } // 30% visibility triggers the animation
    );

    services.forEach((service) => {
        observer.observe(service);
    });
});
