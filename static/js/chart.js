function initializeCharts(resultData) {
    // Feature Importance Chart
    const featureImportanceCtx = document.getElementById('featureImportanceChart').getContext('2d');
    
    const featureLabels = resultData.features.map(f => f.name);
    const featureValues = resultData.features.map(f => f.value);
    const featureImportance = resultData.features.map(f => f.importance);
    
    new Chart(featureImportanceCtx, {
        type: 'bar',
        data: {
            labels: featureLabels,
            datasets: [{
                label: 'Feature Importance',
                data: featureImportance,
                backgroundColor: 'rgba(69, 123, 157, 0.7)',
                borderColor: 'rgba(69, 123, 157, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Importance Score'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Features'
                    }
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Feature Importance in Prediction',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Value: ${featureValues[context.dataIndex]}`;
                        }
                    }
                }
            }
        }
    });

    // Risk Factors Chart (Radar)
    const riskFactorsCtx = document.getElementById('riskFactorsChart').getContext('2d');
    
    // Select top 6 most important features for radar chart
    const topFeatures = resultData.features.slice(0, 6);
    const radarLabels = topFeatures.map(f => f.name);
    const radarData = topFeatures.map(f => {
        // Normalize value for radar chart (0-100 scale)
        // This is a simplified normalization - adjust based on your feature ranges
        return Math.min(100, Math.max(0, f.value * 10));
    });
    
    new Chart(riskFactorsCtx, {
        type: 'radar',
        data: {
            labels: radarLabels,
            datasets: [{
                label: 'Your Values',
                data: radarData,
                backgroundColor: 'rgba(230, 57, 70, 0.2)',
                borderColor: 'rgba(230, 57, 70, 1)',
                pointBackgroundColor: 'rgba(230, 57, 70, 1)',
                pointBorderColor: '#fff',
                pointHoverBackgroundColor: '#fff',
                pointHoverBorderColor: 'rgba(230, 57, 70, 1)'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                r: {
                    angleLines: {
                        display: true
                    },
                    suggestedMin: 0,
                    suggestedMax: 100
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Key Risk Factors Analysis',
                    font: {
                        size: 16
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Value: ${topFeatures[context.dataIndex].value}`;
                        }
                    }
                }
            }
        }
    });
}