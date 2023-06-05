document.addEventListener('DOMContentLoaded', function () {
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Média dos supervisores', 'Média do avaliado', 'Maior média'],
            datasets: [{
                label: 'Resultado corporativo',
                data: [7.9, 8.5, 8.8],
                borderWidth: 1,
                backgroundColor: ['rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 0.2)'],
                borderColor: ['rgb(153, 102, 255)', 'rgb(153, 102, 255)', 'rgb(153, 102, 255)'],
                borderWidth: 1
            }]
        },
        options: {
            backgroundColor: 'white',
            plugins: {
                legend: {
                    labels: {
                        font: {
                            size: 14,
                            weight: 'bold'
                        }
                    }
                }
            },
            scales: {
                x: {
                    ticks: {
                        font: {
                            size: 14
                        }
                    }
                },
                y: {
                    beginAtZero: true,
                    max: 10,
                    ticks: {
                        font: {
                            size: 14
                        }
                    }
                }
            }
        },
    });
});