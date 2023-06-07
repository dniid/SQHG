document.addEventListener('DOMContentLoaded', function () {
    var xValues = ['Média dos supervisores', 'Média do avaliado', 'Maior média']
    var yValues =  []
    var backgroudColors = ['rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(153, 102, 255, 0.2)']
    var borderColors = ['rgb(153, 102, 255)', 'rgb(153, 102, 255)', 'rgb(153, 102, 255)']
    var ctx = document.getElementById('myChart').getContext('2d');
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: [xValues],
            datasets: [{
                label: 'Resultado corporativo',
                data: [yValues],
                borderWidth: 1,
                backgroundColor: backgroudColors,
                borderColor: borderColors,
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