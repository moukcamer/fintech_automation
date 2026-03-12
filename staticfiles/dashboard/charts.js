
document.addEventListener("DOMContentLoaded", function () {

    const evolutionCtx = document.getElementById("evolutionChart");
    if (evolutionCtx) {
        new Chart(evolutionCtx, {
            type: 'line',
            data: {
                labels: chartEvolutionLabels,
                datasets: [{
                    label: 'Transactions',
                    data: chartEvolutionData,
                    borderWidth: 2
                }]
            }
        });
    }

});
