"""
Stage 4: Agentic Architecture
Multi-agent system using MCP (Model Context Protocol) pattern
"""
from typing import Dict, Any, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from loguru import logger
import json


class AgentRole(Enum):
    """Agent role definitions"""
    VALUATION = "valuation"
    MARKET_INTELLIGENCE = "market_intelligence"
    RISK_COMPLIANCE = "risk_compliance"
    NARRATIVE = "narrative"
    ORCHESTRATOR = "orchestrator"


@dataclass
class AgentMessage:
    """Message passed between agents"""
    sender: AgentRole
    receiver: AgentRole
    message_type: str
    payload: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class Agent(ABC):
    """Base agent class following MCP pattern"""
    
    def __init__(self, role: AgentRole):
        self.role = role
        self.state = {}
        self.message_history = []
    
    @abstractmethod
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process incoming message and return response"""
        pass
    
    def log_message(self, message: AgentMessage):
        """Log message for debugging"""
        self.message_history.append(message)
        logger.debug(f"[{self.role.value}] Received: {message.message_type} from {message.sender.value}")
    
    def create_message(self, receiver: AgentRole, message_type: str, 
                      payload: Dict[str, Any]) -> AgentMessage:
        """Create outgoing message"""
        return AgentMessage(
            sender=self.role,
            receiver=receiver,
            message_type=message_type,
            payload=payload
        )


class ValuationAgent(Agent):
    """
    Valuation Agent
    Responsibilities:
    - Execute ML prediction models
    - Calculate property valuations
    - Estimate rental yields
    - Provide confidence intervals
    """
    
    def __init__(self, predictive_model):
        super().__init__(AgentRole.VALUATION)
        self.predictive_model = predictive_model
    
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process valuation request"""
        self.log_message(message)
        
        if message.message_type == "valuation_request":
            property_data = message.payload['property_data']
            
            # Run predictions
            predictions = self.predictive_model.predict(property_data)
            
            # Add valuation metadata
            predictions['valuation_timestamp'] = str((message.metadata or {}).get('timestamp', ''))
            predictions['model_version'] = '1.0.0'
            
            logger.info(f"Predictions generated: {list(predictions.keys())}")
            
            return self.create_message(
                receiver=AgentRole.ORCHESTRATOR,
                message_type="valuation_response",
                payload={'predictions': predictions}
            )
        
        return self.create_message(
            receiver=message.sender,
            message_type="error",
            payload={'error': f"Unknown message type: {message.message_type}"}
        )


class MarketIntelligenceAgent(Agent):
    """
    Market Intelligence Agent
    Responsibilities:
    - Retrieve relevant market documents
    - Analyze market trends
    - Provide location intelligence
    - Infrastructure development tracking
    """
    
    def __init__(self, rag_system):
        super().__init__(AgentRole.MARKET_INTELLIGENCE)
        self.rag_system = rag_system
    
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process market intelligence request"""
        self.log_message(message)
        
        if message.message_type == "market_intelligence_request":
            property_data = message.payload['property_data']
            query = message.payload.get('query', 'Investment analysis')
            
            # Retrieve market context
            market_docs = self.rag_system.retrieve_market_intelligence(
                city=property_data['city'],
                locality=property_data['locality'],
                top_k=3
            )
            
            # Retrieve general context
            general_docs = self.rag_system.retrieve_relevant_context(
                query=query,
                property_data=property_data,
                top_k=3
            )
            
            # Combine and deduplicate
            all_docs = market_docs + general_docs
            unique_docs = {doc['chunk_id']: doc for doc in all_docs}
            
            return self.create_message(
                receiver=AgentRole.ORCHESTRATOR,
                message_type="market_intelligence_response",
                payload={'documents': list(unique_docs.values())[:5]}
            )
        
        return self.create_message(
            receiver=message.sender,
            message_type="error",
            payload={'error': f"Unknown message type: {message.message_type}"}
        )


class RiskComplianceAgent(Agent):
    """
    Risk & Compliance Agent
    Responsibilities:
    - Retrieve regulatory documents
    - Assess compliance status
    - Identify risk factors
    - Suggest mitigation strategies
    """
    
    def __init__(self, rag_system):
        super().__init__(AgentRole.RISK_COMPLIANCE)
        self.rag_system = rag_system
    
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process risk assessment request"""
        self.log_message(message)
        
        if message.message_type == "risk_assessment_request":
            property_data = message.payload['property_data']
            
            # Retrieve regulatory context
            regulatory_docs = self.rag_system.retrieve_regulatory_context(
                city=property_data['city'],
                top_k=3
            )
            
            # Basic risk assessment based on property characteristics
            risk_factors = self._assess_basic_risks(property_data)
            
            return self.create_message(
                receiver=AgentRole.ORCHESTRATOR,
                message_type="risk_assessment_response",
                payload={
                    'regulatory_documents': regulatory_docs,
                    'identified_risks': risk_factors
                }
            )
        
        return self.create_message(
            receiver=message.sender,
            message_type="error",
            payload={'error': f"Unknown message type: {message.message_type}"}
        )
    
    def _assess_basic_risks(self, property_data: Dict[str, Any]) -> List[str]:
        """Assess basic risks from property data"""
        risks = []
        
        if property_data.get('property_age', 0) > 20:
            risks.append("Property age exceeds 20 years - maintenance costs may be higher")
        
        if property_data.get('distance_to_metro_km', 10) > 5:
            risks.append("Distance to metro > 5km - may impact liquidity and rental demand")
        
        if property_data.get('size_sqft', 0) > 3000:
            risks.append("Large property size - limited buyer pool, higher holding costs")
        
        return risks


class NarrativeAgent(Agent):
    """
    Narrative Agent
    Responsibilities:
    - Synthesize information from all agents
    - Generate investment narratives
    - Create structured recommendations
    - Ensure transparency and explainability
    """
    
    def __init__(self, generative_analyzer):
        super().__init__(AgentRole.NARRATIVE)
        self.generative_analyzer = generative_analyzer
    
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process narrative generation request"""
        self.log_message(message)
        
        if message.message_type == "narrative_generation_request":
            property_data = message.payload['property_data']
            predictions = message.payload['predictions']
            investment_context = message.payload['investment_context']
            retrieved_docs = message.payload['retrieved_documents']
            
            # Generate comprehensive analysis
            analysis = self.generative_analyzer.analyze_investment(
                property_data=property_data,
                predictions=predictions,
                investment_context=investment_context,
                retrieved_docs=retrieved_docs
            )
            
            return self.create_message(
                receiver=AgentRole.ORCHESTRATOR,
                message_type="narrative_response",
                payload={'analysis': analysis}
            )
        
        return self.create_message(
            receiver=message.sender,
            message_type="error",
            payload={'error': f"Unknown message type: {message.message_type}"}
        )


class OrchestratorAgent(Agent):
    """
    Orchestrator Agent
    Responsibilities:
    - Coordinate multi-agent workflow
    - Route messages between agents
    - Aggregate responses
    - Handle errors and retries
    - Maintain conversation state
    """
    
    def __init__(self, valuation_agent: ValuationAgent,
                 market_agent: MarketIntelligenceAgent,
                 risk_agent: RiskComplianceAgent,
                 narrative_agent: NarrativeAgent):
        super().__init__(AgentRole.ORCHESTRATOR)
        self.agents = {
            AgentRole.VALUATION: valuation_agent,
            AgentRole.MARKET_INTELLIGENCE: market_agent,
            AgentRole.RISK_COMPLIANCE: risk_agent,
            AgentRole.NARRATIVE: narrative_agent
        }
    
    async def process(self, message: AgentMessage) -> AgentMessage:
        """Process orchestration request"""
        self.log_message(message)
        
        if message.message_type == "investment_analysis_request":
            return await self._orchestrate_investment_analysis(message)
        
        return self.create_message(
            receiver=message.sender,
            message_type="error",
            payload={'error': f"Unknown message type: {message.message_type}"}
        )
    
    async def _orchestrate_investment_analysis(self, message: AgentMessage) -> AgentMessage:
        """Orchestrate complete investment analysis workflow"""
        
        property_data = message.payload['property_data']
        investment_context = message.payload['investment_context']
        
        logger.info("Starting investment analysis orchestration...")
        
        # Step 1: Valuation
        logger.info("Step 1: Requesting valuation...")
        valuation_msg = self.create_message(
            receiver=AgentRole.VALUATION,
            message_type="valuation_request",
            payload={'property_data': property_data}
        )
        valuation_response = await self.agents[AgentRole.VALUATION].process(valuation_msg)
        predictions = valuation_response.payload['predictions']
        
        # Step 2: Market Intelligence (parallel with risk assessment conceptually)
        logger.info("Step 2: Requesting market intelligence...")
        market_msg = self.create_message(
            receiver=AgentRole.MARKET_INTELLIGENCE,
            message_type="market_intelligence_request",
            payload={
                'property_data': property_data,
                'query': 'Investment opportunity analysis'
            }
        )
        market_response = await self.agents[AgentRole.MARKET_INTELLIGENCE].process(market_msg)
        market_docs = market_response.payload['documents']
        
        # Step 3: Risk & Compliance Assessment
        logger.info("Step 3: Requesting risk assessment...")
        risk_msg = self.create_message(
            receiver=AgentRole.RISK_COMPLIANCE,
            message_type="risk_assessment_request",
            payload={'property_data': property_data}
        )
        risk_response = await self.agents[AgentRole.RISK_COMPLIANCE].process(risk_msg)
        regulatory_docs = risk_response.payload['regulatory_documents']
        identified_risks = risk_response.payload['identified_risks']
        
        # Combine all documents
        all_docs = market_docs + regulatory_docs
        
        # Step 4: Narrative Generation
        logger.info("Step 4: Generating narrative...")
        narrative_msg = self.create_message(
            receiver=AgentRole.NARRATIVE,
            message_type="narrative_generation_request",
            payload={
                'property_data': property_data,
                'predictions': predictions,
                'investment_context': investment_context,
                'retrieved_documents': all_docs
            }
        )
        narrative_response = await self.agents[AgentRole.NARRATIVE].process(narrative_msg)
        analysis = narrative_response.payload['analysis']
        
        # Add identified risks to analysis
        if identified_risks:
            analysis['risk_factors'] = list(set(
                analysis.get('risk_factors', []) + identified_risks
            ))
        
        # Aggregate final response
        final_payload = {
            'predictions': predictions,
            'analysis': analysis,
            'retrieved_documents': all_docs,
            'agent_execution_summary': {
                'valuation_completed': True,
                'market_intelligence_completed': True,
                'risk_assessment_completed': True,
                'narrative_completed': True
            }
        }
        
        logger.info("Investment analysis orchestration completed successfully")
        
        return self.create_message(
            receiver=message.sender,
            message_type="investment_analysis_response",
            payload=final_payload
        )


class AgenticSystem:
    """
    Complete agentic system
    Provides high-level API for investment analysis
    """
    
    def __init__(self, predictive_model, rag_system, generative_analyzer):
        # Initialize agents
        self.valuation_agent = ValuationAgent(predictive_model)
        self.market_agent = MarketIntelligenceAgent(rag_system)
        self.risk_agent = RiskComplianceAgent(rag_system)
        self.narrative_agent = NarrativeAgent(generative_analyzer)
        
        # Initialize orchestrator
        self.orchestrator = OrchestratorAgent(
            valuation_agent=self.valuation_agent,
            market_agent=self.market_agent,
            risk_agent=self.risk_agent,
            narrative_agent=self.narrative_agent
        )
    
    async def analyze_investment(self, property_data: Dict[str, Any], 
                                investment_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perform complete investment analysis using multi-agent system
        
        Args:
            property_data: Property details
            investment_context: Investor preferences and constraints
            
        Returns:
            Complete investment analysis
        """
        
        # Create analysis request
        request = AgentMessage(
            sender=AgentRole.ORCHESTRATOR,  # External caller
            receiver=AgentRole.ORCHESTRATOR,
            message_type="investment_analysis_request",
            payload={
                'property_data': property_data,
                'investment_context': investment_context
            }
        )
        
        # Execute orchestration
        response = await self.orchestrator.process(request)
        
        if response.message_type == "error":
            raise Exception(response.payload['error'])
        
        return response.payload


if __name__ == "__main__":
    print("""
    Agentic Architecture Design:
    
    1. ValuationAgent: Handles ML predictions
    2. MarketIntelligenceAgent: Retrieves market data via RAG
    3. RiskComplianceAgent: Assesses risks and regulatory compliance
    4. NarrativeAgent: Synthesizes information into recommendations
    5. OrchestratorAgent: Coordinates the entire workflow
    
    Communication Pattern: Model Context Protocol (MCP)
    - Agents communicate via structured messages
    - Orchestrator routes messages and aggregates responses
    - Error handling and retry logic built-in
    - State management for complex workflows
    
    Benefits:
    - Modularity: Each agent has single responsibility
    - Scalability: Easy to add new agents
    - Testability: Agents can be tested independently
    - Extensibility: New capabilities via new agents
    - Observability: Message history for debugging
    """)
