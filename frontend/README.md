# Real Estate Investment Intelligence - Frontend

Beautiful, responsive frontend for the AI-Driven Real Estate Investment Intelligence Platform.

## Features

- 🎨 Modern, gradient-based UI design
- 📱 Fully responsive (mobile, tablet, desktop)
- ⚡ Real-time API integration
- 📊 Interactive data visualization
- 📄 PDF report download
- 🔄 Loading states and error handling

## Quick Start

### Option 1: Open Directly in Browser

Simply open `index.html` in your browser:
```bash
# Windows
start index.html

# Mac
open index.html

# Linux
xdg-open index.html
```

### Option 2: Use Python HTTP Server

```bash
cd frontend
python -m http.server 8080
```

Then visit: http://localhost:8080

### Option 3: Use Live Server (VS Code)

1. Install "Live Server" extension in VS Code
2. Right-click `index.html`
3. Select "Open with Live Server"

## Usage

1. **Ensure API is Running**: The backend API must be running at `http://localhost:8000`
   ```bash
   python src/api/main.py
   ```

2. **Fill Property Details**: Enter all required property information
   - City, locality, property type
   - Size, bedrooms, bathrooms
   - Property age, floor details
   - Distance to metro, amenities

3. **Set Investment Context**:
   - Investment horizon (years)
   - Primary goal (appreciation/income/balanced)
   - Risk tolerance (conservative/moderate/aggressive)

4. **Analyze**: Click "Analyze Investment" button

5. **Review Results**:
   - Predictive analysis with price/rent/yield
   - Investment recommendation (Buy/Hold/Avoid)
   - Risk assessment with mitigation strategies
   - Positive and negative drivers
   - Market intelligence from documents
   - Download comprehensive PDF report

## API Configuration

The frontend connects to the backend API at `http://localhost:8000` by default.

To change the API URL, edit `script.js`:
```javascript
const API_BASE_URL = 'http://your-api-url:port';
```

## File Structure

```
frontend/
├── index.html      # Main HTML structure
├── styles.css      # CSS styling and animations
├── script.js       # JavaScript API integration
└── README.md       # This file
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Troubleshooting

### API Connection Issues

If you see "Failed to analyze investment":
1. Check that the API server is running
2. Verify the API URL in `script.js`
3. Check browser console for CORS errors
4. Ensure port 8000 is not blocked

### CORS Issues

If running frontend and backend on different domains, the API needs CORS enabled (already configured in backend).

### PDF Download Not Working

1. Wait for report generation (up to 30 seconds)
2. Check browser's download permissions
3. Verify `reports/` directory exists in backend

## Features Breakdown

### Predictive Analysis
- Price prediction with confidence intervals
- Monthly rent estimation
- Rental yield calculation
- Model confidence score

### Investment Recommendation
- Buy/Hold/Avoid recommendation
- Location and infrastructure scores
- Regulatory compliance rating
- Expected ROI and appreciation rates
- Market sentiment analysis

### Risk Assessment
- Risk level classification (Low/Medium/High)
- Identified risk factors
- Mitigation strategies

### Investment Drivers
- Positive drivers supporting investment
- Negative drivers to consider

### Market Intelligence
- Relevant market documents
- Regulatory context
- Relevance scoring

### PDF Report
- Comprehensive analysis report
- All metrics and recommendations
- Professional formatting
- Downloadable and shareable

## Customization

### Colors

Edit CSS variables in `styles.css`:
```css
:root {
    --primary-color: #2563eb;
    --success-color: #10b981;
    --warning-color: #f59e0b;
    --danger-color: #ef4444;
}
```

### Form Fields

Add/modify form fields in `index.html` and update the data collection in `script.js`.

### Result Display

Customize result visualization in `script.js` display functions:
- `displayPrediction()`
- `displayRecommendation()`
- `displayRisk()`
- `displayDrivers()`
- `displayMarketIntelligence()`

## License

MIT License - Part of Real Estate Investment Intelligence Platform
