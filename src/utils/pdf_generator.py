"""
PDF Report Generation
Creates comprehensive technical PDF reports
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from datetime import datetime
from typing import Dict, Any
from pathlib import Path
import json


class InvestmentReportGenerator:
    """Generate comprehensive PDF investment reports"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def generate_report(self, report_data: Dict[str, Any], filename: str = None) -> str:
        """Generate complete investment analysis report"""
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"investment_report_{timestamp}.pdf"
        
        filepath = self.output_dir / filename
        
        # Create PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )
        
        # Container for elements
        elements = []
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#1f4788'),
            spaceAfter=12,
            spaceBefore=12
        )
        
        # Title Page
        elements.append(Paragraph("Real Estate Investment Intelligence Report", title_style))
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Golden Mile Properties", styles['Heading2']))
        elements.append(Spacer(1, 0.2*inch))
        elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        elements.append(Paragraph(f"Request ID: {report_data.get('request_id', 'N/A')}", styles['Normal']))
        elements.append(PageBreak())
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", heading_style))
        property_summary = report_data.get('property_summary', {})
        recommendation = report_data.get('recommendation', {})
        
        summary_text = f"""
        <b>Property:</b> {property_summary.get('property_type', 'N/A')} in {property_summary.get('locality', 'N/A')}, {property_summary.get('city', 'N/A')}<br/>
        <b>Size:</b> {property_summary.get('size_sqft', 'N/A')} sq ft | <b>Age:</b> {property_summary.get('property_age', 'N/A')} years<br/>
        <b>Investment Recommendation:</b> <b>{recommendation.get('recommendation', 'N/A')}</b><br/>
        <b>Confidence Score:</b> {recommendation.get('confidence_score', 0):.1%}<br/>
        """
        elements.append(Paragraph(summary_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Predictions Section
        elements.append(Paragraph("Valuation & Predictions", heading_style))
        predictions = report_data.get('predictions', {})
        
        prediction_data = [
            ['Metric', 'Value', 'Range/Details'],
            ['Predicted Price', f"₹{predictions.get('predicted_price', 0):,.0f}", 
             f"₹{predictions.get('price_range_min', 0):,.0f} - ₹{predictions.get('price_range_max', 0):,.0f}"],
            ['Monthly Rent', f"₹{predictions.get('predicted_rent', 0):,.0f}", ''],
            ['Rental Yield', f"{predictions.get('predicted_rental_yield', 0):.2f}%", 'Annual basis'],
            ['Model Confidence', f"{predictions.get('price_confidence', 0):.1%}", ''],
            ['Model Used', predictions.get('model_used', 'N/A'), '']
        ]
        
        prediction_table = Table(prediction_data, colWidths=[2*inch, 2*inch, 2.5*inch])
        prediction_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(prediction_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Investment Analysis
        elements.append(Paragraph("Investment Analysis", heading_style))
        elements.append(Paragraph(recommendation.get('reasoning', 'N/A'), styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Drivers
        elements.append(Paragraph("Investment Drivers", heading_style))
        drivers = report_data.get('investment_drivers', {})
        
        positive_text = "<b>Positive Factors:</b><br/>" + "<br/>".join(
            [f"• {d}" for d in drivers.get('positive_drivers', [])]
        )
        elements.append(Paragraph(positive_text, styles['Normal']))
        elements.append(Spacer(1, 0.1*inch))
        
        negative_text = "<b>Concerns:</b><br/>" + "<br/>".join(
            [f"• {d}" for d in drivers.get('negative_drivers', [])]
        )
        elements.append(Paragraph(negative_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Risk Assessment
        elements.append(Paragraph("Risk Assessment", heading_style))
        risk_assessment = report_data.get('risk_assessment', {})
        
        risk_text = f"""
        <b>Risk Level:</b> {risk_assessment.get('risk_level', 'N/A').upper()}<br/>
        <b>Compliance Score:</b> {risk_assessment.get('regulatory_compliance_score', 0):.1%}<br/><br/>
        <b>Identified Risks:</b><br/>
        """ + "<br/>".join([f"• {r}" for r in risk_assessment.get('risk_factors', [])])
        
        elements.append(Paragraph(risk_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        mitigation_text = "<b>Mitigation Strategies:</b><br/>" + "<br/>".join(
            [f"• {m}" for m in risk_assessment.get('mitigation_strategies', [])]
        )
        elements.append(Paragraph(mitigation_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Expected Returns
        elements.append(Paragraph("Expected Returns", heading_style))
        returns_data = [
            ['Period', 'Appreciation Estimate', 'Expected ROI'],
            ['3 Years', f"{recommendation.get('expected_appreciation_3yr', 0):.1f}%", ''],
            ['5 Years', f"{recommendation.get('expected_appreciation_5yr', 0):.1f}%", ''],
            ['Total ROI', '', f"{recommendation.get('expected_roi', 0):.1f}%"]
        ]
        
        returns_table = Table(returns_data, colWidths=[2*inch, 2*inch, 2*inch])
        returns_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ]))
        elements.append(returns_table)
        elements.append(PageBreak())
        
        # Technical Details
        elements.append(Paragraph("Technical Methodology", heading_style))
        
        methodology_text = """
        <b>1. Data Sources & Assumptions</b><br/>
        This analysis is based on synthetic data generated for demonstration purposes. 
        In production, data would be sourced from:<br/>
        • Property transaction databases<br/>
        • RERA registered project data<br/>
        • Market research reports<br/>
        • Government regulatory documents<br/><br/>
        
        <b>2. Machine Learning Models</b><br/>
        Price and rent predictions use ensemble methods:<br/>
        • XGBoost/LightGBM gradient boosting<br/>
        • Random Forest regression<br/>
        • Feature engineering: location, size, age, amenities<br/>
        • Cross-validation for model selection<br/><br/>
        
        <b>3. RAG System Design</b><br/>
        • Document chunking: 400 tokens with 50-token overlap<br/>
        • Embeddings: all-MiniLM-L6-v2 (384 dimensions)<br/>
        • Vector DB: ChromaDB with cosine similarity<br/>
        • Retrieval: Top-5 relevant chunks per query<br/><br/>
        
        <b>4. Generative AI Layer</b><br/>
        • Model: GPT-4 Turbo<br/>
        • Structured prompts with context injection<br/>
        • Hallucination safeguards: explicit limitations<br/>
        • Output validation and sanitization<br/><br/>
        
        <b>5. Agentic Architecture</b><br/>
        Multi-agent system with specialized agents:<br/>
        • Valuation Agent: ML predictions<br/>
        • Market Intelligence Agent: RAG-based retrieval<br/>
        • Risk & Compliance Agent: Regulatory assessment<br/>
        • Narrative Agent: Synthesis and reasoning<br/>
        • Orchestrator Agent: Workflow coordination<br/>
        """
        elements.append(Paragraph(methodology_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Assumptions
        elements.append(Paragraph("Key Assumptions", heading_style))
        assumptions = report_data.get('assumptions', [])
        assumptions_text = "<br/>".join([f"• {a}" for a in assumptions])
        elements.append(Paragraph(assumptions_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Limitations
        elements.append(Paragraph("Limitations & Disclaimers", heading_style))
        limitations = report_data.get('limitations', [])
        limitations_text = "<br/>".join([f"• {l}" for l in limitations])
        elements.append(Paragraph(limitations_text, styles['Normal']))
        elements.append(Spacer(1, 0.2*inch))
        
        disclaimer_text = """
        <b>Important Disclaimer:</b><br/>
        This report is generated by an AI system for informational purposes only. 
        It should not be considered as financial or investment advice. 
        Independent due diligence, legal verification, and professional consultation 
        are strongly recommended before making any investment decision.
        """
        elements.append(Paragraph(disclaimer_text, styles['Normal']))
        
        # Build PDF
        doc.build(elements)
        
        return str(filepath)


if __name__ == "__main__":
    # Test report generation
    test_data = {
        'request_id': 'TEST_001',
        'property_summary': {
            'city': 'Mumbai',
            'locality': 'Andheri',
            'property_type': 'Apartment',
            'size_sqft': 1200,
            'property_age': 5
        },
        'predictions': {
            'predicted_price': 12000000,
            'predicted_rent': 40000,
            'predicted_rental_yield': 4.0,
            'price_confidence': 0.85,
            'price_range_min': 10800000,
            'price_range_max': 13200000,
            'model_used': 'XGBoost'
        },
        'recommendation': {
            'recommendation': 'Buy',
            'confidence_score': 0.82,
            'reasoning': 'Strong location fundamentals with good infrastructure connectivity.',
            'expected_appreciation_3yr': 8.5,
            'expected_appreciation_5yr': 15.0,
            'expected_roi': 12.5
        },
        'investment_drivers': {
            'positive_drivers': ['Metro connectivity', 'Established locality', 'Good rental demand'],
            'negative_drivers': ['High initial investment', 'Market volatility']
        },
        'risk_assessment': {
            'risk_level': 'medium',
            'risk_factors': ['Market correction risk', 'Liquidity constraints'],
            'mitigation_strategies': ['Hold for long-term', 'Verify RERA compliance'],
            'regulatory_compliance_score': 0.9
        },
        'assumptions': ['Stable economic conditions', 'No major regulatory changes'],
        'limitations': ['Based on synthetic data', 'Model uncertainty exists']
    }
    
    generator = InvestmentReportGenerator(Path('./reports'))
    report_path = generator.generate_report(test_data)
    print(f"Report generated: {report_path}")
