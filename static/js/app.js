document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById('inputForm');
    const resultDiv = document.getElementById('result');
    const ctx = document.getElementById('predictionChart').getContext('2d');
    let predictionChart;

    form.addEventListener('submit', function(event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => response.json())
        .then(result => {
            displayResult(result);
        })
        .catch(error => {
            console.error('Error:', error);
            resultDiv.innerHTML = '<p class="error">An error occurred. Please try again.</p>';
        });
    });

    function displayResult(result) {
        resultDiv.innerHTML = `
            <div class="result-box">
                <h3>Prediction Results</h3>
                <p><strong>Prediction of Sleep Disorder:</strong> ${result.disorder_prediction}</p>
                <p><strong>Predicted Sleep Quality:</strong> ${result.quality_prediction}</p>
            </div>
        `;

        const labels = ['Disorder Prediction', 'Quality Prediction'];
        const data = [result.disorder_prediction, result.quality_prediction];

        if (predictionChart) {
            predictionChart.destroy();
        }

        predictionChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Prediction Results',
                    data: data,
                    backgroundColor: ['#5555e1', '#ff7f50'],
                    borderColor: ['#3333cc', '#cc3300'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                },
                plugins: {
                    legend: {
                        display: true,
                        labels: {
                            color: '#333'
                        }
                    },
                    tooltip: {
                        enabled: true,
                        backgroundColor: '#333',
                        titleColor: '#fff',
                        bodyColor: '#fff',
                        borderColor: '#fff',
                        borderWidth: 1
                    }
                }
            }
        });
    }
});
