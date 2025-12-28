"""
Data Generation Module
Generates synthetic real estate data for demonstration purposes
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List
import json


class SyntheticDataGenerator:
    """Generates realistic synthetic real estate data"""
    
    def __init__(self, n_samples: int = 5000):
        self.n_samples = n_samples
        self.random_state = 42
        np.random.seed(self.random_state)
        
        # Indian cities and localities
        self.cities = {
            'Mumbai': ['Andheri', 'Bandra', 'Juhu', 'Powai', 'Worli', 'Lower Parel'],
            'Delhi': ['Connaught Place', 'Dwarka', 'Rohini', 'Vasant Kunj', 'Greater Kailash'],
            'Bangalore': ['Whitefield', 'Koramangala', 'Indiranagar', 'Electronic City', 'HSR Layout'],
            'Pune': ['Hinjewadi', 'Wakad', 'Kharadi', 'Baner', 'Viman Nagar'],
            'Hyderabad': ['Gachibowli', 'HITECH City', 'Madhapur', 'Kondapur', 'Banjara Hills'],
            'Chennai': ['OMR', 'Anna Nagar', 'T Nagar', 'Velachery', 'Adyar']
        }
        
        self.property_types = ['Apartment', 'Villa', 'Independent House', 'Penthouse']
        
    def generate_structured_data(self) -> pd.DataFrame:
        """Generate structured property dataset"""
        
        data = []
        
        for i in range(self.n_samples):
            city = np.random.choice(list(self.cities.keys()))
            locality = np.random.choice(self.cities[city])
            property_type = np.random.choice(self.property_types)
            
            # Size based on property type
            if property_type == 'Apartment':
                size = np.random.randint(600, 2000)
            elif property_type == 'Villa':
                size = np.random.randint(1500, 4000)
            elif property_type == 'Penthouse':
                size = np.random.randint(2000, 5000)
            else:
                size = np.random.randint(1200, 3500)
            
            age = np.random.randint(0, 30)
            bedrooms = min(max(1, size // 500), 5)
            bathrooms = min(bedrooms, bedrooms - 1) if bedrooms > 1 else 1
            
            # Price influenced by city, locality, size, and age
            city_multiplier = {'Mumbai': 1.5, 'Delhi': 1.3, 'Bangalore': 1.2, 
                             'Pune': 1.0, 'Hyderabad': 0.9, 'Chennai': 0.95}
            
            base_price = size * np.random.uniform(4000, 8000)
            price = base_price * city_multiplier[city] * (1 - age * 0.01)
            price += np.random.normal(0, price * 0.1)  # Add noise
            
            # Rental yield
            monthly_rent = price * np.random.uniform(0.002, 0.004)
            annual_rent = monthly_rent * 12
            rental_yield = (annual_rent / price) * 100
            
            # Distance to metro
            distance_to_metro = np.random.uniform(0.5, 10)
            
            # Additional features
            has_parking = np.random.choice([True, False], p=[0.7, 0.3])
            floor = np.random.randint(0, 20) if property_type == 'Apartment' else 0
            
            # Transaction date
            days_ago = np.random.randint(0, 1095)  # 3 years
            transaction_date = datetime.now() - timedelta(days=days_ago)
            
            data.append({
                'property_id': f'PROP_{i+1:05d}',
                'city': city,
                'locality': locality,
                'property_type': property_type,
                'size_sqft': size,
                'bedrooms': bedrooms,
                'bathrooms': bathrooms,
                'property_age': age,
                'price': round(price, 2),
                'monthly_rent': round(monthly_rent, 2),
                'annual_rent': round(annual_rent, 2),
                'rental_yield': round(rental_yield, 2),
                'distance_to_metro_km': round(distance_to_metro, 2),
                'has_parking': has_parking,
                'floor': floor,
                'transaction_date': transaction_date.strftime('%Y-%m-%d'),
                'year': transaction_date.year,
                'month': transaction_date.month
            })
        
        return pd.DataFrame(data)
    
    def generate_market_documents(self) -> List[Dict[str, str]]:
        """Generate market news and analysis documents"""
        
        documents = [
            {
                'doc_id': 'MKT_001',
                'title': 'Mumbai Real Estate Market Analysis Q4 2024',
                'content': """
Mumbai's real estate market showed strong resilience in Q4 2024. The western suburbs, 
particularly Andheri and Bandra, witnessed a 12% price appreciation driven by improved 
infrastructure connectivity through Metro Line 3. Luxury segment in Worli and Lower Parel 
continued to outperform with average prices touching ₹45,000 per sq ft. 

Key drivers: Metro connectivity, premium office spaces, and NRI investments.
Risk factors: High inventory levels in certain micro-markets, regulatory compliance delays.
                """,
                'category': 'market_analysis',
                'city': 'Mumbai',
                'date': '2024-10-15'
            },
            {
                'doc_id': 'MKT_002',
                'title': 'Bangalore Tech Corridor Property Trends 2024',
                'content': """
Bangalore's IT corridors in Whitefield and Electronic City saw sustained demand throughout 2024.
Average rental yields in these areas stabilized at 3-3.5%, making them attractive for investors.
The upcoming Peripheral Ring Road project is expected to unlock value in emerging localities.

Whitefield: Strong appreciation potential (8-10% annually)
Electronic City: Stable rental yields, good for long-term holding
HSR Layout: Premium residential, limited supply driving prices
                """,
                'category': 'market_analysis',
                'city': 'Bangalore',
                'date': '2024-09-20'
            },
            {
                'doc_id': 'MKT_003',
                'title': 'Infrastructure Impact on Pune Real Estate',
                'content': """
The Pune Metro expansion to Hinjewadi has significantly impacted property values. 
Areas within 1 km of metro stations saw 15-18% appreciation. IT parks in Hinjewadi
continue to attract residential demand. However, oversupply in Wakad poses short-term risks.

Investment recommendation: Focus on metro-adjacent properties with possession-ready status.
Rental demand strong in Hinjewadi Phase 1 and 2.
                """,
                'category': 'market_analysis',
                'city': 'Pune',
                'date': '2024-11-05'
            },
            {
                'doc_id': 'NEWS_001',
                'title': 'RERA Compliance Strengthens Buyer Confidence',
                'content': """
Real Estate Regulatory Authority (RERA) compliance has improved dramatically across major cities.
90% of new projects now have valid RERA registrations. This has increased buyer confidence and
reduced project delivery delays. However, buyers should still verify RERA status before investment.

Key checks: RERA registration validity, project timeline, builder track record.
                """,
                'category': 'regulatory_news',
                'city': 'All',
                'date': '2024-08-12'
            },
            {
                'doc_id': 'NEWS_002',
                'title': 'Stamp Duty Changes Impact Investment Returns',
                'content': """
Recent stamp duty revisions in Maharashtra and Karnataka affect net returns for investors.
Maharashtra: 5% for women, 6% for men (down from 7%)
Karnataka: 3% stamp duty + 1% registration charges

These changes improve initial investment IRR by 8-12 basis points. Factor these costs 
into total acquisition cost when evaluating deals.
                """,
                'category': 'regulatory_news',
                'city': 'Multiple',
                'date': '2024-07-18'
            },
            {
                'doc_id': 'INF_001',
                'title': 'Metro Expansion Plans 2025-2030',
                'content': """
Major metro expansion projects across Indian cities will reshape real estate values:

Mumbai: Metro Line 4, 5, 6 completion by 2026
Delhi: Phase 4 covering Gurgaon and Noida
Bangalore: Airport line and Outer Ring Road metro by 2027
Hyderabad: Extension to Shamshabad and Gachibowli

Properties within 500m of planned stations show 20-30% appreciation potential post-completion.
                """,
                'category': 'infrastructure',
                'city': 'Multiple',
                'date': '2024-06-25'
            },
            {
                'doc_id': 'RISK_001',
                'title': 'Real Estate Investment Risk Framework',
                'content': """
Comprehensive risk assessment for real estate investments:

1. Market Risk: Price volatility, demand-supply imbalances
2. Liquidity Risk: Longer holding periods, limited exit options
3. Regulatory Risk: RERA, zoning changes, tax implications
4. Developer Risk: Project delays, quality issues, financial stability
5. Location Risk: Infrastructure delays, changing demographics

Mitigation: Due diligence, diversification, legal verification, market research.
                """,
                'category': 'risk_analysis',
                'city': 'All',
                'date': '2024-10-01'
            }
        ]
        
        return documents
    
    def generate_regulatory_pdfs_content(self) -> List[Dict[str, str]]:
        """Generate content for regulatory PDF documents"""
        
        pdfs = [
            {
                'doc_id': 'REG_001',
                'title': 'RERA Compliance Guidelines Maharashtra 2024',
                'content': """
REAL ESTATE (REGULATION AND DEVELOPMENT) ACT, 2016
MAHARASHTRA RERA COMPLIANCE REQUIREMENTS

1. REGISTRATION REQUIREMENTS
All real estate projects exceeding 500 sq meters or 8 apartments must be registered with MahaRERA.
Registration must be completed before advertising or selling.

2. MANDATORY DISCLOSURES
- Project layout plans approved by competent authority
- Project completion timeline
- Land title status and encumbrances
- Quarterly project progress reports
- Details of contractors and development agreements

3. ESCROW ACCOUNT MANDATE
70% of customer payments must be deposited in escrow account
Funds can be withdrawn only for project-related expenses
Bank certification required for fund utilization

4. PENALTY PROVISIONS
Non-compliance: Penalty up to 10% of project cost
Delayed possession: Interest compensation to buyers
False information: Imprisonment up to 3 years

5. BUYER PROTECTIONS
Standardized agreements and allotment letters
Mandatory structural defect liability: 5 years
Right to withdraw with interest within cooling period

Effective Date: January 1, 2024
Authority: Maharashtra Real Estate Regulatory Authority
                """,
                'category': 'rera_compliance',
                'jurisdiction': 'Maharashtra',
                'effective_date': '2024-01-01'
            },
            {
                'doc_id': 'REG_002',
                'title': 'Karnataka RERA Registration and Compliance Manual',
                'content': """
KARNATAKA REAL ESTATE REGULATORY AUTHORITY
REGISTRATION AND COMPLIANCE FRAMEWORK

APPLICABILITY
Projects with land area > 500 sq meters or > 8 apartments
Both residential and commercial projects covered

REGISTRATION PROCESS
1. Online application through K-RERA portal
2. Upload of land documents, approvals, project plans
3. Payment of registration fee (0.05% of project cost)
4. RERA certificate issuance within 30 days

ONGOING COMPLIANCE
- Quarterly progress reports mandatory
- Website disclosure of all project details
- Escrow account maintenance (70% rule)
- Timely possession delivery

DISPUTE RESOLUTION
K-RERA Conciliation Forum for buyer grievances
Appellate Tribunal for appeals
Timeline: 60 days for first resolution

PENALTIES AND CONSEQUENCES
Project delay: Interest @ 10.75% per annum to buyers
Non-registration: Prohibition on marketing and sales
False certification: Debarring from future projects

Authority: Karnataka Real Estate Regulatory Authority
Updated: March 2024
                """,
                'category': 'rera_compliance',
                'jurisdiction': 'Karnataka',
                'effective_date': '2024-03-01'
            },
            {
                'doc_id': 'REG_003',
                'title': 'Stamp Duty and Registration Charges - Pan India Guide',
                'content': """
STAMP DUTY AND REGISTRATION CHARGES
STATE-WISE COMPILATION 2024

MAHARASHTRA
Stamp Duty: 5% (women), 6% (men), 1% (Metro Cess in Mumbai)
Registration: 1% of property value
Exemption: First-time women buyers in certain categories

KARNATAKA
Stamp Duty: 3% (women), 5% (men)
Registration: 1% 
Additional: 0.5% cess on stamp duty

DELHI/NCR
Stamp Duty: 4% (women), 6% (men)
Registration: 1%
Additional charges: As per authority rates

TELANGANA
Stamp Duty: 4% (rural), 5% (urban)
Registration: Flat rate based on property value
Transfer duty: 1% for urban properties

TAMIL NADU
Stamp Duty: 7% of property value
Registration: 1%
Additional local body charges apply

IMPORTANT CONSIDERATIONS
- Stamp duty calculated on circle rate or transaction value (whichever higher)
- Additional charges: legal fees, processing fees
- Online payment available in most states
- Property registration within 4 months mandatory

Tax Planning: Factor stamp duty + registration = 6-8% of total investment cost
                """,
                'category': 'stamp_duty',
                'jurisdiction': 'Multiple States',
                'effective_date': '2024-01-01'
            },
            {
                'doc_id': 'REG_004',
                'title': 'Building Regulations and Zoning Laws',
                'content': """
MUNICIPAL BUILDING REGULATIONS AND ZONING COMPLIANCE

FLOOR AREA RATIO (FAR) / FLOOR SPACE INDEX (FSI)
Mumbai: FAR 1.33 to 3.0 (varies by zone)
Bangalore: FAR 1.75 to 3.25 
Pune: FAR 1.0 to 2.5
Delhi: FAR 1.2 to 3.5 (based on road width)

SETBACK REQUIREMENTS
Front setback: Minimum 3 meters
Side setback: 2-3 meters (varies by plot size)
Rear setback: 2 meters minimum
Height restrictions: 15 meters (ground + 4 floors) typical

LAND USE CLASSIFICATION
Residential: Exclusive residential zones
Commercial: Retail, office, mixed-use
Industrial: IT parks, manufacturing (restricted zones)
Agricultural: Conversion approval required for development

PARKING NORMS
Residential: 1 covered parking per unit (minimum)
Commercial: 1 parking per 50-75 sq meters
Visitor parking: 10% of total parking

BUILDING SAFETY AND AMENITIES
Fire safety: NOC mandatory for buildings > 15 meters
Rainwater harvesting: Mandatory for plots > 300 sq meters
Waste management: On-site STP for large projects
Disabled access: Ramps and lifts required

APPROVAL PROCESS
1. Building plan approval from municipal authority
2. Commencement certificate before construction
3. Occupancy certificate before possession
4. Compliance with NBC (National Building Code)

Non-compliance: Demolition orders, penalties, criminal prosecution
                """,
                'category': 'building_regulations',
                'jurisdiction': 'Multiple',
                'effective_date': '2024-01-01'
            }
        ]
        
        return pdfs
    
    def save_datasets(self, output_dir: Path):
        """Save all generated datasets"""
        
        # Structured data
        df = self.generate_structured_data()
        df.to_csv(output_dir / 'properties_data.csv', index=False)
        df.to_parquet(output_dir / 'properties_data.parquet', index=False)
        
        # Market documents
        market_docs = self.generate_market_documents()
        with open(output_dir / 'market_documents.json', 'w') as f:
            json.dump(market_docs, f, indent=2)
        
        # Regulatory documents
        regulatory_docs = self.generate_regulatory_pdfs_content()
        with open(output_dir / 'regulatory_documents.json', 'w') as f:
            json.dump(regulatory_docs, f, indent=2)
        
        print(f"✓ Generated {len(df)} property records")
        print(f"✓ Generated {len(market_docs)} market documents")
        print(f"✓ Generated {len(regulatory_docs)} regulatory documents")
        
        return df, market_docs, regulatory_docs


if __name__ == "__main__":
    from pathlib import Path
    
    output_dir = Path("./data")
    output_dir.mkdir(exist_ok=True)
    
    generator = SyntheticDataGenerator(n_samples=5000)
    generator.save_datasets(output_dir)
