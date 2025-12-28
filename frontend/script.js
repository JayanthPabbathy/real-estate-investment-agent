const API_BASE_URL = 'http://localhost:8000';

// Form submission handler
document.getElementById('analysisForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const analyzeBtn = document.getElementById('analyzeBtn');
    const btnText = analyzeBtn.querySelector('.btn-text');
    const loader = analyzeBtn.querySelector('.loader');
    const resultsSection = document.getElementById('resultsSection');
    
    // Disable button and show loader
    analyzeBtn.disabled = true;
    btnText.textContent = 'Analyzing...';
    loader.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Collect form data
    const formData = new FormData(e.target);
    const propertyData = {
        city: formData.get('city'),
        locality: formData.get('locality'),
        property_type: formData.get('property_type'),
        size_sqft: parseFloat(formData.get('size_sqft')),
        bedrooms: parseInt(formData.get('bedrooms')),
        bathrooms: parseInt(formData.get('bathrooms')),
        property_age: parseInt(formData.get('property_age')),
        floor: parseInt(formData.get('floor_number')) || null,
        distance_to_metro_km: parseFloat(formData.get('distance_to_metro_km')) || null,
        has_parking: formData.get('parking_available') === 'on'
    };
    
    const investmentContext = {
        investment_horizon_years: parseInt(formData.get('investment_horizon')),
        primary_goal: formData.get('primary_goal'),
        risk_tolerance: formData.get('risk_tolerance'),
        financing_required: false
    };
    
    const requestData = {
        property: propertyData,
        context: investmentContext
    };
    
    try {
        // Call analysis API
        const response = await fetch(`${API_BASE_URL}/api/v1/analyze`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(requestData)
        });
        
        if (!response.ok) {
            throw new Error(`API error: ${response.status}`);
        }
        
        const result = await response.json();
        
        // Display results
        displayResults(result);
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
        
    } catch (error) {
        console.error('Error:', error);
        resultsSection.style.display = 'block';
        resultsSection.innerHTML = `
            <div class="card error-message">
                <h2>⚠️ Error</h2>
                <p>Failed to analyze investment. Please check if the API server is running at ${API_BASE_URL}</p>
                <p><strong>Error details:</strong> ${error.message}</p>
            </div>
        `;
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    } finally {
        // Re-enable button
        analyzeBtn.disabled = false;
        btnText.textContent = 'Analyze Investment';
        loader.style.display = 'none';
    }
});

function displayResults(data) {
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    console.log('Response data:', data);
    
    // Prediction Output
    if (data.predictions) {
        displayPrediction(data.predictions);
    }
    
    // Investment Recommendation
    if (data.recommendation) {
        displayRecommendation(data.recommendation);
    }
    
    // Risk Assessment
    if (data.risk_assessment) {
        displayRisk(data.risk_assessment);
    }
    
    // Investment Drivers
    if (data.investment_drivers) {
        displayDrivers(data.investment_drivers);
    }
    
    // Market Intelligence
    if (data.retrieved_documents) {
        displayMarketIntelligence(data.retrieved_documents);
    }
    
    // Assumptions & Limitations
    if (data.assumptions || data.limitations) {
        displayTransparency(data.assumptions, data.limitations);
    }
    
    // Report Download
    if (data.request_id) {
        setupReportDownload(data.request_id, data.report_url);
    }
}

function displayPrediction(prediction) {
    const output = document.getElementById('predictionOutput');
    
    if (!prediction) {
        output.innerHTML = '<p>No prediction data available.</p>';
        return;
    }
    
    const priceRange = `₹${formatNumber(prediction.price_range_min)} - ₹${formatNumber(prediction.price_range_max)}`;
    
    output.innerHTML = `
        <div class="metric-grid">
            <div class="metric-card">
                <div class="metric-label">Predicted Price</div>
                <div class="metric-value">₹${formatNumber(prediction.predicted_price)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Monthly Rent</div>
                <div class="metric-value">₹${formatNumber(prediction.predicted_rent)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Rental Yield</div>
                <div class="metric-value">${prediction.predicted_rental_yield.toFixed(2)}%</div>
            </div>
            <div class="metric-card">
                <div class="metric-label">Model Confidence</div>
                <div class="metric-value">${(prediction.price_confidence * 100).toFixed(1)}%</div>
            </div>
        </div>
        
        <div style="margin-top: 1rem;">
            <p><strong>Price Range:</strong> ${priceRange}</p>
            <p><strong>Model Used:</strong> ${prediction.model_used}</p>
        </div>
    `;
}

function displayRecommendation(recommendation) {
    const output = document.getElementById('recommendationOutput');
    
    if (!recommendation) {
        output.innerHTML = '<p>No recommendation data available.</p>';
        return;
    }
    
    const recommendationClass = recommendation.recommendation.toLowerCase();
    
    output.innerHTML = `
        <div class="recommendation-box ${recommendationClass}">
            <div class="recommendation-header">
                <div class="recommendation-title">
                    ${getRecommendationIcon(recommendation.recommendation)} ${recommendation.recommendation}
                </div>
                <div class="confidence-badge">
                    Confidence: ${(recommendation.confidence_score * 100).toFixed(1)}%
                </div>
            </div>
            
            <div class="reasoning">
                ${recommendation.reasoning}
            </div>
            
            <div style="margin-top: 1rem;">
                <p><strong>Expected Appreciation (3yr):</strong> ${recommendation.expected_appreciation_3yr ? recommendation.expected_appreciation_3yr.toFixed(1) + '%' : 'N/A'}</p>
                <p><strong>Expected Appreciation (5yr):</strong> ${recommendation.expected_appreciation_5yr ? recommendation.expected_appreciation_5yr.toFixed(1) + '%' : 'N/A'}</p>
                <p><strong>Expected ROI:</strong> ${recommendation.expected_roi ? recommendation.expected_roi.toFixed(1) + '%' : 'N/A'}</p>
            </div>
        </div>
    `;
}

function displayRisk(risk) {
    const output = document.getElementById('riskOutput');
    
    if (!risk) {
        output.innerHTML = '<p>No risk assessment data available.</p>';
        return;
    }
    
    output.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
            <span class="risk-badge ${risk.risk_level.toLowerCase()}">${risk.risk_level.toUpperCase()} RISK</span>
            <div style="text-align: right;">
                <div style="font-size: 0.9rem; color: var(--text-secondary);">Regulatory Compliance</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: var(--primary-color);">${(risk.regulatory_compliance_score * 100).toFixed(0)}%</div>
            </div>
        </div>
        
        ${risk.risk_factors && risk.risk_factors.length > 0 ? `
            <div class="list-section negative">
                <h4>Risk Factors</h4>
                <ul>
                    ${risk.risk_factors.map(r => `<li>${r}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
        
        ${risk.mitigation_strategies && risk.mitigation_strategies.length > 0 ? `
            <div class="list-section positive">
                <h4>Mitigation Strategies</h4>
                <ul>
                    ${risk.mitigation_strategies.map(m => `<li>${m}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;
}

function displayDrivers(drivers) {
    const output = document.getElementById('driversOutput');
    
    if (!drivers) {
        output.innerHTML = '<p>No investment drivers data available.</p>';
        return;
    }
    
    output.innerHTML = `
        <div class="score-grid" style="margin-bottom: 1.5rem;">
            <div class="score-item">
                <div class="score-value">${drivers.location_score}/10</div>
                <div class="score-label">Location</div>
            </div>
            <div class="score-item">
                <div class="score-value">${drivers.infrastructure_score}/10</div>
                <div class="score-label">Infrastructure</div>
            </div>
            <div class="score-item">
                <div class="score-value" style="font-size: 1.5rem;">${drivers.market_sentiment}</div>
                <div class="score-label">Market Sentiment</div>
            </div>
        </div>
        
        ${drivers.positive_drivers && drivers.positive_drivers.length > 0 ? `
            <div class="list-section positive">
                <h4>✅ Positive Drivers</h4>
                <ul>
                    ${drivers.positive_drivers.map(d => `<li>${d}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
        
        ${drivers.negative_drivers && drivers.negative_drivers.length > 0 ? `
            <div class="list-section negative">
                <h4>❌ Negative Drivers</h4>
                <ul>
                    ${drivers.negative_drivers.map(d => `<li>${d}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;
}

function displayMarketIntelligence(documents) {
    const output = document.getElementById('marketOutput');
    
    if (!documents || documents.length === 0) {
        output.innerHTML = '<p>No market intelligence documents available.</p>';
        return;
    }
    
    output.innerHTML = documents.map(doc => `
        <div class="document-card">
            <div class="document-title">${doc.title}</div>
            <div class="document-snippet">${doc.content.substring(0, 300)}...</div>
            <span class="relevance-score">Relevance: ${(doc.relevance_score * 100).toFixed(0)}%</span>
        </div>
    `).join('');
}

function displayTransparency(assumptions, limitations) {
    const output = document.getElementById('transparencyOutput');
    
    output.innerHTML = `
        ${assumptions && assumptions.length > 0 ? `
            <div class="list-section" style="margin-bottom: 1.5rem;">
                <h4>Key Assumptions</h4>
                <ul>
                    ${assumptions.map(a => `<li>${a}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
        
        ${limitations && limitations.length > 0 ? `
            <div class="list-section">
                <h4>Limitations</h4>
                <ul>
                    ${limitations.map(l => `<li>${l}</li>`).join('')}
                </ul>
            </div>
        ` : ''}
    `;
}

function setupReportDownload(analysisId, reportPath) {
    const reportStatus = document.getElementById('reportStatus');
    const downloadBtn = document.getElementById('downloadBtn');
    
    if (reportPath) {
        reportStatus.textContent = 'PDF report is ready for download';
        downloadBtn.style.display = 'block';
        downloadBtn.onclick = () => {
            window.open(`${API_BASE_URL}${reportPath}`, '_blank');
        };
    } else {
        // Poll for report generation
        reportStatus.textContent = 'Generating comprehensive PDF report...';
        
        const pollInterval = setInterval(async () => {
            try {
                const response = await fetch(`${API_BASE_URL}/api/v1/report/${analysisId}`);
                const data = await response.json();
                
                if (data.status === 'completed' && data.report_path) {
                    clearInterval(pollInterval);
                    reportStatus.textContent = 'PDF report is ready for download';
                    downloadBtn.style.display = 'block';
                    downloadBtn.onclick = () => {
                        window.open(`${API_BASE_URL}${data.report_path}`, '_blank');
                    };
                } else if (data.status === 'failed') {
                    clearInterval(pollInterval);
                    reportStatus.textContent = 'Report generation failed. Please try again.';
                }
            } catch (error) {
                console.error('Error polling report status:', error);
            }
        }, 3000);
        
        // Stop polling after 1 minute
        setTimeout(() => clearInterval(pollInterval), 60000);
    }
}

function getRecommendationIcon(recommendation) {
    const icons = {
        'Buy': '✅',
        'Hold': '⏸️',
        'Avoid': '❌'
    };
    return icons[recommendation] || '•';
}

function formatNumber(num) {
    if (num >= 10000000) {
        return (num / 10000000).toFixed(2) + ' Cr';
    } else if (num >= 100000) {
        return (num / 100000).toFixed(2) + ' L';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(2) + ' K';
    }
    return num.toFixed(0);
}

// Check API health on page load
window.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        const health = await response.json();
        console.log('API Status:', health);
    } catch (error) {
        console.warn('API server not reachable:', error);
    }
});
