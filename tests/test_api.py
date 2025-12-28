"""
Example usage and test scripts
"""
import requests
import json
from datetime import datetime


def test_health():
    """Test health endpoint"""
    response = requests.get("http://localhost:8000/health")
    print(f"Health Check: {response.json()}")
    return response.status_code == 200


def test_investment_analysis():
    """Test investment analysis endpoint"""
    
    request_data = {
        "property": {
            "city": "Mumbai",
            "locality": "Andheri",
            "property_type": "Apartment",
            "size_sqft": 1200,
            "bedrooms": 2,
            "bathrooms": 2,
            "property_age": 5,
            "distance_to_metro_km": 1.5,
            "has_parking": True,
            "floor": 3
        },
        "context": {
            "investment_horizon_years": 5,
            "primary_goal": "both",
            "risk_tolerance": "medium",
            "budget_range_min": 10000000,
            "budget_range_max": 15000000,
            "financing_required": False
        }
    }
    
    print("\nSending investment analysis request...")
    print(json.dumps(request_data, indent=2))
    
    response = requests.post(
        "http://localhost:8000/api/v1/analyze",
        json=request_data,
        headers={"Content-Type": "application/json"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print("\n" + "="*80)
        print("INVESTMENT ANALYSIS RESULT")
        print("="*80)
        
        print(f"\nRequest ID: {result['request_id']}")
        print(f"Timestamp: {result['timestamp']}")
        
        print("\n--- PREDICTIONS ---")
        pred = result['predictions']
        print(f"Predicted Price: ₹{pred['predicted_price']:,.0f}")
        print(f"Price Range: ₹{pred['price_range_min']:,.0f} - ₹{pred['price_range_max']:,.0f}")
        print(f"Monthly Rent: ₹{pred['predicted_rent']:,.0f}")
        print(f"Rental Yield: {pred['predicted_rental_yield']:.2f}%")
        print(f"Confidence: {pred['price_confidence']:.1%}")
        print(f"Model: {pred['model_used']}")
        
        print("\n--- RECOMMENDATION ---")
        rec = result['recommendation']
        print(f"Recommendation: {rec['recommendation']}")
        print(f"Confidence: {rec['confidence_score']:.1%}")
        print(f"Reasoning: {rec['reasoning']}")
        
        if rec['expected_appreciation_3yr']:
            print(f"3-Year Appreciation: {rec['expected_appreciation_3yr']:.1f}%")
        if rec['expected_appreciation_5yr']:
            print(f"5-Year Appreciation: {rec['expected_appreciation_5yr']:.1f}%")
        if rec['expected_roi']:
            print(f"Expected ROI: {rec['expected_roi']:.1f}%")
        
        print("\n--- INVESTMENT DRIVERS ---")
        drivers = result['investment_drivers']
        print("\nPositive Factors:")
        for factor in drivers['positive_drivers']:
            print(f"  + {factor}")
        
        print("\nConcerns:")
        for concern in drivers['negative_drivers']:
            print(f"  - {concern}")
        
        print(f"\nMarket Sentiment: {drivers['market_sentiment']}")
        print(f"Location Score: {drivers['location_score']}/10")
        print(f"Infrastructure Score: {drivers['infrastructure_score']}/10")
        
        print("\n--- RISK ASSESSMENT ---")
        risk = result['risk_assessment']
        print(f"Risk Level: {risk['risk_level'].upper()}")
        print(f"Compliance Score: {risk['regulatory_compliance_score']:.1%}")
        
        print("\nRisk Factors:")
        for factor in risk['risk_factors']:
            print(f"  • {factor}")
        
        print("\nMitigation Strategies:")
        for strategy in risk['mitigation_strategies']:
            print(f"  • {strategy}")
        
        print("\n--- RETRIEVED DOCUMENTS ---")
        for doc in result['retrieved_documents'][:3]:
            print(f"\n{doc['title']}")
            print(f"  Category: {doc['category']}")
            print(f"  Relevance: {doc['relevance_score']:.3f}")
            print(f"  Content: {doc['content'][:150]}...")
        
        print("\n--- ASSUMPTIONS ---")
        for assumption in result['assumptions']:
            print(f"  • {assumption}")
        
        print("\n--- LIMITATIONS ---")
        for limitation in result['limitations']:
            print(f"  • {limitation}")
        
        if result.get('report_url'):
            print(f"\n📄 PDF Report: {result['report_url']}")
        
        print("\n" + "="*80)
        
        return True
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return False


def test_get_stats():
    """Test statistics endpoint"""
    response = requests.get("http://localhost:8000/api/v1/stats")
    print("\nSystem Statistics:")
    print(json.dumps(response.json(), indent=2))


if __name__ == "__main__":
    print("Testing Real Estate Investment Intelligence API")
    print("="*80)
    
    # Test health
    if test_health():
        print("✓ Health check passed")
    
    # Test investment analysis
    if test_investment_analysis():
        print("\n✓ Investment analysis completed successfully")
    
    # Test stats
    test_get_stats()
