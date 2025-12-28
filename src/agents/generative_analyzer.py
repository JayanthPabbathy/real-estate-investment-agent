"""
Stage 3: Generative Reasoning Layer
LLM-based investment analysis and explanation generation
"""
from openai import AzureOpenAI
from typing import Dict, Any, List
import json
from loguru import logger
from tenacity import retry, stop_after_attempt, wait_exponential


class PromptTemplates:
    """Prompt templates for different analysis tasks"""
    
    INVESTMENT_ANALYSIS = """
You are an expert real estate investment analyst for Golden Mile Properties in India. 
Your role is to provide data-backed, transparent investment analysis.

PROPERTY DETAILS:
{property_details}

PREDICTED METRICS:
- Predicted Price: ₹{predicted_price:,.0f}
- Price Range: ₹{price_min:,.0f} - ₹{price_max:,.0f}
- Predicted Monthly Rent: ₹{predicted_rent:,.0f}
- Predicted Rental Yield: {rental_yield:.2f}%
- Model Confidence: {confidence:.1%}

INVESTOR CONTEXT:
- Investment Horizon: {investment_horizon} years
- Primary Goal: {primary_goal}
- Risk Tolerance: {risk_tolerance}

MARKET INTELLIGENCE:
{market_context}

REGULATORY CONTEXT:
{regulatory_context}

Based on the above information, provide a comprehensive investment analysis in JSON format:

{{
  "recommendation": "Buy/Hold/Avoid",
  "confidence_score": 0.0-1.0,
  "reasoning": "Detailed reasoning in 3-4 sentences",
  "positive_drivers": ["driver1", "driver2", "driver3"],
  "negative_drivers": ["concern1", "concern2"],
  "risk_factors": ["risk1", "risk2", "risk3"],
  "mitigation_strategies": ["strategy1", "strategy2"],
  "market_sentiment": "Bullish/Neutral/Bearish",
  "location_score": 0-10,
  "infrastructure_score": 0-10,
  "regulatory_compliance_score": 0.0-1.0,
  "risk_level": "low/medium/high",
  "expected_appreciation_3yr": percentage,
  "expected_appreciation_5yr": percentage,
  "expected_roi": percentage,
  "assumptions": ["assumption1", "assumption2"],
  "limitations": ["limitation1", "limitation2"]
}}

IMPORTANT GUIDELINES:
1. Be conservative and transparent about uncertainties
2. Explicitly state assumptions made
3. Flag any data quality or availability concerns
4. Consider regulatory compliance and legal factors
5. Align analysis with investor's goals and risk tolerance
6. Base reasoning on retrieved market intelligence
7. Avoid hallucination - only use provided data
8. If information is insufficient, state it clearly in limitations
"""

    RISK_ASSESSMENT = """
Analyze the investment risks for this real estate opportunity:

PROPERTY: {property_summary}
PREDICTIONS: {predictions}
MARKET CONTEXT: {market_context}

Provide a structured risk assessment identifying:
1. Market risks (demand/supply, price volatility)
2. Location risks (infrastructure, accessibility)
3. Regulatory risks (compliance, legal)
4. Financial risks (liquidity, financing)
5. Developer risks (if applicable)

Return assessment in JSON format with risk_level, risk_factors, and mitigation_strategies.
"""


class GenerativeAnalyzer:
    """LLM-based investment analysis"""
    
    def __init__(self, api_key: str, endpoint: str = "", api_version: str = "2025-01-01-preview", 
                 model: str = "gpt-4o", temperature: float = 0.7):
        if endpoint:
            # Azure OpenAI
            self.client = AzureOpenAI(
                api_key=api_key,
                azure_endpoint=endpoint,
                api_version=api_version
            )
        else:
            # Standard OpenAI (fallback)
            from openai import OpenAI
            self.client = OpenAI(api_key=api_key)
        self.model = model
        self.temperature = temperature
    
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def generate_completion(self, prompt: str, response_format: str = "json") -> str:
        """Generate completion with retry logic"""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert real estate investment analyst. Provide accurate, data-driven analysis in valid JSON format."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=2000,
                response_format={"type": "json_object"} if response_format == "json" else None
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error generating completion: {e}")
            raise
    
    def analyze_investment(self, property_data: Dict[str, Any], 
                          predictions: Dict[str, float],
                          investment_context: Dict[str, Any],
                          retrieved_docs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive investment analysis"""
        
        # Format property details
        property_details = f"""
City: {property_data['city']}
Locality: {property_data['locality']}
Type: {property_data['property_type']}
Size: {property_data['size_sqft']} sq ft
Bedrooms: {property_data['bedrooms']}
Age: {property_data['property_age']} years
Distance to Metro: {property_data.get('distance_to_metro_km', 'N/A')} km
"""
        
        # Format market context
        market_docs = [doc for doc in retrieved_docs if 'market' in doc['metadata'].get('category', '').lower() or 'news' in doc['metadata'].get('category', '').lower()]
        market_context = "\n\n".join([
            f"Document: {doc['metadata']['title']}\n{doc['content'][:500]}"
            for doc in market_docs[:3]
        ]) if market_docs else "Limited market data available."
        
        # Format regulatory context
        regulatory_docs = [doc for doc in retrieved_docs if 'reg' in doc['metadata'].get('category', '').lower() or 'rera' in doc['metadata'].get('category', '').lower()]
        regulatory_context = "\n\n".join([
            f"Document: {doc['metadata']['title']}\n{doc['content'][:500]}"
            for doc in regulatory_docs[:2]
        ]) if regulatory_docs else "Standard regulatory compliance applies."
        
        # Generate prompt
        prompt = PromptTemplates.INVESTMENT_ANALYSIS.format(
            property_details=property_details,
            predicted_price=predictions['predicted_price'],
            price_min=predictions['price_range_min'],
            price_max=predictions['price_range_max'],
            predicted_rent=predictions['predicted_rent'],
            rental_yield=predictions['predicted_rental_yield'],
            confidence=predictions['price_confidence'],
            investment_horizon=investment_context['investment_horizon_years'],
            primary_goal=investment_context['primary_goal'],
            risk_tolerance=investment_context['risk_tolerance'],
            market_context=market_context,
            regulatory_context=regulatory_context
        )
        
        # Generate analysis
        logger.info("Generating investment analysis...")
        try:
            response = self.generate_completion(prompt, response_format="json")
            
            # Parse response
            try:
                analysis = json.loads(response)
                logger.info("Successfully parsed LLM response")
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing JSON response: {e}")
                logger.error(f"Raw response: {response[:500]}")
                # Fallback analysis
                analysis = self._create_fallback_analysis(property_data, predictions, investment_context)
        except Exception as e:
            logger.error(f"Error generating completion: {e}", exc_info=True)
            # Fallback analysis
            analysis = self._create_fallback_analysis(property_data, predictions, investment_context)
        
        # Add hallucination safeguards
        analysis = self._validate_and_sanitize_analysis(analysis, predictions, investment_context)
        
        return analysis
    
    def _create_fallback_analysis(self, property_data: Dict, predictions: Dict, context: Dict) -> Dict:
        """Create fallback analysis if LLM fails"""
        return {
            "recommendation": "Hold",
            "confidence_score": 0.5,
            "reasoning": "Analysis based on predictive models only. Limited contextual data available.",
            "positive_drivers": ["Quantitative prediction available", "Property details verified"],
            "negative_drivers": ["Limited market intelligence", "Unable to generate comprehensive analysis"],
            "risk_factors": ["Data availability", "Market volatility", "Regulatory changes"],
            "mitigation_strategies": ["Conduct independent due diligence", "Verify RERA compliance", "Local market research"],
            "market_sentiment": "Neutral",
            "location_score": 5.0,
            "infrastructure_score": 5.0,
            "regulatory_compliance_score": 0.7,
            "risk_level": "medium",
            "expected_appreciation_3yr": 5.0,
            "expected_appreciation_5yr": 8.0,
            "expected_roi": predictions['predicted_rental_yield'] * context['investment_horizon_years'] / 100,
            "assumptions": ["Model predictions are accurate", "Market conditions remain stable"],
            "limitations": ["LLM analysis unavailable", "Limited contextual data", "Requires expert verification"]
        }
    
    def _validate_and_sanitize_analysis(self, analysis: Dict, predictions: Dict, context: Dict) -> Dict:
        """Validate and sanitize LLM output"""
        
        # Ensure required fields exist
        required_fields = ['recommendation', 'confidence_score', 'reasoning', 
                          'positive_drivers', 'negative_drivers', 'risk_factors',
                          'mitigation_strategies', 'assumptions', 'limitations']
        
        for field in required_fields:
            if field not in analysis:
                logger.warning(f"Missing field in analysis: {field}")
                if field in ['positive_drivers', 'negative_drivers', 'risk_factors', 
                           'mitigation_strategies', 'assumptions', 'limitations']:
                    analysis[field] = []
                elif field == 'reasoning':
                    analysis[field] = "Analysis generated from predictive models."
                elif field == 'recommendation':
                    analysis[field] = "Hold"
                elif field == 'confidence_score':
                    analysis[field] = predictions['price_confidence']
        
        # Validate recommendation
        if analysis['recommendation'] not in ['Buy', 'Hold', 'Avoid']:
            analysis['recommendation'] = 'Hold'
        
        # Validate confidence score
        if not (0 <= analysis.get('confidence_score', 0) <= 1):
            analysis['confidence_score'] = predictions['price_confidence']
        
        # Validate risk level
        if analysis.get('risk_level') not in ['low', 'medium', 'high']:
            analysis['risk_level'] = 'medium'
        
        # Add explicit limitations
        if 'limitations' not in analysis or not analysis['limitations']:
            analysis['limitations'] = [
                "Analysis based on synthetic/limited data",
                "Market conditions subject to rapid change",
                "Predictions have inherent uncertainty",
                "Independent verification recommended"
            ]
        
        # Add data quality disclaimer
        analysis['limitations'].append(
            f"Model confidence: {predictions['price_confidence']:.1%}"
        )
        
        return analysis


if __name__ == "__main__":
    # Test with dummy data
    import os
    
    api_key = os.getenv('OPENAI_API_KEY', 'test-key')
    analyzer = GenerativeAnalyzer(api_key=api_key)
    
    property_data = {
        'city': 'Mumbai',
        'locality': 'Andheri',
        'property_type': 'Apartment',
        'size_sqft': 1200,
        'bedrooms': 2,
        'property_age': 5,
        'distance_to_metro_km': 1.5
    }
    
    predictions = {
        'predicted_price': 12000000,
        'predicted_rent': 40000,
        'predicted_rental_yield': 4.0,
        'price_confidence': 0.85,
        'price_range_min': 10800000,
        'price_range_max': 13200000
    }
    
    context = {
        'investment_horizon_years': 5,
        'primary_goal': 'both',
        'risk_tolerance': 'medium'
    }
    
    retrieved_docs = []
    
    # This would fail without valid API key, which is expected for testing
    try:
        analysis = analyzer.analyze_investment(property_data, predictions, context, retrieved_docs)
        print(json.dumps(analysis, indent=2))
    except Exception as e:
        print(f"Expected error without valid API key: {e}")
