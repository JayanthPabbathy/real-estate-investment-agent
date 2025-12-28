# Sample JSON Outputs

## Investment Analysis Response

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "timestamp": "2024-12-24T10:30:00",
  "property_summary": {
    "city": "Mumbai",
    "locality": "Andheri",
    "property_type": "Apartment",
    "size_sqft": 1200,
    "bedrooms": 2,
    "property_age": 5
  },
  "predictions": {
    "predicted_price": 12000000,
    "predicted_rent": 40000,
    "predicted_rental_yield": 4.0,
    "price_confidence": 0.85,
    "price_range_min": 10800000,
    "price_range_max": 13200000,
    "model_used": "xgboost"
  },
  "investment_drivers": {
    "positive_drivers": [
      "Excellent metro connectivity (1.5 km from station)",
      "Established locality with good infrastructure",
      "Strong rental demand from IT professionals",
      "Recent appreciation trend of 8-10% annually"
    ],
    "negative_drivers": [
      "High initial investment required",
      "Market correction risk in premium segment",
      "Property age impacts maintenance costs"
    ],
    "market_sentiment": "Bullish",
    "location_score": 8.5,
    "infrastructure_score": 9.0
  },
  "risk_assessment": {
    "risk_level": "medium",
    "risk_factors": [
      "Market volatility in premium segment",
      "Liquidity constraints for large properties",
      "Regulatory changes affecting stamp duty",
      "Competition from new projects in vicinity"
    ],
    "mitigation_strategies": [
      "Verify RERA compliance thoroughly",
      "Ensure clear title and legal documentation",
      "Consider rental yield for steady income",
      "Diversify investment across properties",
      "Hold for minimum 5 years for appreciation"
    ],
    "regulatory_compliance_score": 0.92
  },
  "recommendation": {
    "recommendation": "Buy",
    "confidence_score": 0.82,
    "reasoning": "This property presents a strong investment opportunity given its excellent location in Andheri with proximity to metro connectivity. The predicted rental yield of 4% is above market average, providing steady cash flow. The location fundamentals are solid with good infrastructure development and established demand drivers. While the initial investment is substantial, the 3-5 year appreciation potential (15-20%) combined with rental income makes this attractive for medium to long-term investors with moderate risk tolerance.",
    "expected_appreciation_3yr": 12.5,
    "expected_appreciation_5yr": 20.0,
    "expected_roi": 14.8
  },
  "retrieved_documents": [
    {
      "doc_id": "MKT_001_chunk_0",
      "title": "Mumbai Real Estate Market Analysis Q4 2024",
      "content": "Mumbai's real estate market showed strong resilience in Q4 2024. The western suburbs, particularly Andheri and Bandra, witnessed a 12% price appreciation driven by improved infrastructure connectivity through Metro Line 3...",
      "relevance_score": 0.89,
      "category": "market_analysis",
      "source": "vector_db"
    },
    {
      "doc_id": "REG_001_chunk_0",
      "title": "RERA Compliance Guidelines Maharashtra 2024",
      "content": "All real estate projects exceeding 500 sq meters or 8 apartments must be registered with MahaRERA. Registration must be completed before advertising or selling...",
      "relevance_score": 0.85,
      "category": "rera_compliance",
      "source": "vector_db"
    }
  ],
  "assumptions": [
    "Market conditions remain stable over investment horizon",
    "No major regulatory changes affecting property taxation",
    "Infrastructure projects complete as per timeline",
    "Rental demand continues in the locality",
    "Model predictions based on historical patterns"
  ],
  "limitations": [
    "Analysis based on synthetic data for demonstration",
    "Predictions have ±10-15% uncertainty margin",
    "Market sentiment can change rapidly",
    "Individual property inspection recommended",
    "Legal due diligence required independently",
    "Model confidence: 85.0%"
  ],
  "report_url": "/api/v1/report/550e8400-e29b-41d4-a716-446655440000"
}
```

## Health Check Response

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-12-24T10:30:00",
  "models_loaded": true,
  "vector_db_status": "connected"
}
```

## System Statistics Response

```json
{
  "model_metrics": {
    "price": {
      "random_forest": {
        "mae": 550000,
        "rmse": 800000,
        "r2": 0.89,
        "mape": 8.2
      },
      "xgboost": {
        "mae": 520000,
        "rmse": 750000,
        "r2": 0.92,
        "mape": 6.5
      },
      "lightgbm": {
        "mae": 540000,
        "rmse": 780000,
        "r2": 0.91,
        "mape": 7.1
      }
    },
    "rent": {
      "mae": 2500,
      "rmse": 3800,
      "r2": 0.88,
      "mape": 7.8
    },
    "best_model": "xgboost"
  },
  "vector_db": {
    "collection_name": "real_estate_docs",
    "total_chunks": 87,
    "embedding_dimension": 384
  },
  "reports_generated": 15
}
```

## Error Response

```json
{
  "detail": "Internal server error: OpenAI API rate limit exceeded"
}
```
