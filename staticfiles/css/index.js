// Smooth scroll pour le bouton "Découvrir"
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        e.preventDefault();
        document.querySelector(this.getAttribute("href")).scrollIntoView({behavior:"smooth"});
    });
});

// Animation des KPI (compteurs)
document.addEventListener("DOMContentLoaded", () => {
    const counters = document.querySelectorAll(".kpi-value");
    counters.forEach(counter => {
        const updateCount = () => {
            const target = +counter.textContent.replace(/[^0-9]/g,'');
            let count = 0;
            const increment = target / 100;
            const interval = setInterval(() => {
                count += increment;
                if(count >= target){
                    counter.textContent = target.toLocaleString();
                    clearInterval(interval);
                } else {
                    counter.textContent = Math.floor(count).toLocaleString();
                }
            }, 20);
        };
        updateCount();
    });
});
