# Technical Architecture Documentation

## System Overview

The Real Estate Investment Intelligence Platform is built using a multi-agent architecture that combines:
- **Machine Learning** for predictive analytics
- **Retrieval-Augmented Generation (RAG)** for contextual knowledge
- **Generative AI** for reasoning and synthesis
- **Agentic orchestration** for workflow management

---

## Architecture Layers

### 1. Data Layer

**Components:**
- Synthetic data generator for properties, market docs, regulatory docs
- CSV/Parquet storage for structured data
- JSON storage for unstructured documents

**Design Decision:** Synthetic data allows demonstration without accessing paid datasets. In production, replace with:
- Real estate transaction databases
- RERA API integration
- Market research feeds
- Regulatory document scrapers

### 2. ML Layer (Stage 1)

**Pipeline:**
```
Raw Data → Feature Engineering → Model Training → Prediction → Confidence Estimation
```

**Models Evaluated:**
1. **Random Forest** - Baseline, interpretable
2. **XGBoost** - Best performance on tabular data
3. **LightGBM** - Fast, memory-efficient

**Feature Engineering:**
- Derived features: price_per_sqft, metro_score
- Categorical encoding: cities, localities, property types
- Interaction features: city_locality combinations
- Temporal features: transaction patterns

**Model Selection:** Automatic based on cross-validation R² score

**Uncertainty Quantification:**
- Confidence scores based on model agreement
- Prediction intervals (±1.96 std)
- Out-of-distribution detection (placeholder for production)

### 3. RAG Layer (Stage 2)

**Architecture:**
```
Documents → Chunking → Embedding → Vector DB → Retrieval → Ranking
```

**Chunking Strategy:**
- **Method:** Paragraph-based with overlap
- **Size:** 400 tokens per chunk
- **Overlap:** 50 tokens
- **Rationale:** Preserves context while enabling granular retrieval

**Embedding Model:**
- **Model:** all-MiniLM-L6-v2 (384 dimensions)
- **Why:** Balance between performance and speed
- **Alternative:** OpenAI text-embedding-3-small for production

**Vector Database:**
- **DB:** ChromaDB with persistent storage
- **Similarity:** Cosine similarity
- **Indexing:** HNSW for fast approximate search

**Retrieval Strategy:**
- Top-K retrieval (K=5 default)
- Metadata filtering (city, category)
- Relevance score thresholding

### 4. Generative Layer (Stage 3)

**LLM Configuration:**
- **Model:** GPT-4 Turbo (gpt-4-turbo-preview)
- **Temperature:** 0.7 (balanced creativity/consistency)
- **Max Tokens:** 2000
- **Response Format:** Structured JSON

**Prompt Engineering:**

**System Prompt:**
```
You are an expert real estate investment analyst for Golden Mile Properties in India.
Provide data-backed, transparent investment analysis.
```

**Structured Output:**
- Enforced JSON schema
- Required fields validation
- Output sanitization

**Hallucination Safeguards:**
1. Explicit context injection
2. Source attribution
3. Confidence scoring
4. Limitations disclosure
5. Output validation

**Retry Logic:**
- Exponential backoff
- 3 retry attempts
- Fallback to rule-based analysis

### 5. Agentic Layer (Stage 4)

**Agent Architecture:**

```
                 Orchestrator Agent
                        |
        ┌───────────────┼───────────────┐
        |               |               |
    Valuation     Market Intel     Risk Agent
     Agent           Agent              |
        |               |               |
        └───────────────┼───────────────┘
                        |
                 Narrative Agent
```

**Communication Pattern: Model Context Protocol (MCP)**

**Message Structure:**
```python
AgentMessage(
    sender: AgentRole,
    receiver: AgentRole,
    message_type: str,
    payload: Dict[str, Any],
    metadata: Optional[Dict]
)
```

**Agent Responsibilities:**

1. **Valuation Agent**
   - Execute ML predictions
   - Calculate confidence intervals
   - Provide numerical metrics

2. **Market Intelligence Agent**
   - Query RAG system for market data
   - Filter by location and category
   - Rank documents by relevance

3. **Risk & Compliance Agent**
   - Retrieve regulatory documents
   - Assess basic risk factors
   - Provide mitigation strategies

4. **Narrative Agent**
   - Synthesize all agent outputs
   - Generate structured recommendations
   - Ensure explainability

5. **Orchestrator Agent**
   - Coordinate workflow
   - Route messages
   - Handle errors
   - Aggregate responses

**Benefits:**
- **Modularity:** Independent agent testing
- **Scalability:** Easy to add agents
- **Observability:** Message history tracking
- **Extensibility:** Plugin architecture

### 6. API Layer (Stage 5)

**Framework:** FastAPI

**Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Root info |
| `/health` | GET | Health check |
| `/api/v1/analyze` | POST | Investment analysis |
| `/api/v1/report/{id}` | GET | Download PDF |
| `/api/v1/stats` | GET | System statistics |

**Request Flow:**
```
Client → FastAPI → Pydantic Validation → Agentic System → 
Response Formatting → PDF Generation (Background) → JSON Response
```

**Error Handling:**
- Input validation (Pydantic)
- Try-catch at each layer
- Structured error responses
- Detailed logging

**Background Tasks:**
- PDF report generation
- Non-blocking execution

**CORS:** Enabled for development (configure for production)

---

## Data Flow Example

**Input:**
```json
{
  "property": {
    "city": "Mumbai",
    "locality": "Andheri",
    "size_sqft": 1200,
    ...
  },
  "context": {
    "investment_horizon_years": 5,
    ...
  }
}
```

**Processing:**

1. **Valuation Agent** runs ML model:
   - Predicted price: ₹12,000,000
   - Confidence: 85%

2. **Market Agent** retrieves docs:
   - "Mumbai Market Analysis Q4 2024"
   - "Infrastructure Impact on Andheri"

3. **Risk Agent** retrieves compliance docs:
   - "RERA Compliance Maharashtra"
   - "Stamp Duty Regulations"

4. **Narrative Agent** synthesizes:
   - Combines predictions + context
   - Generates recommendation
   - Provides reasoning

**Output:**
```json
{
  "request_id": "uuid",
  "predictions": {...},
  "recommendation": {
    "recommendation": "Buy",
    "confidence_score": 0.82,
    "reasoning": "..."
  },
  "risk_assessment": {...},
  "retrieved_documents": [...]
}
```

---

## Scalability Considerations

### Current Capacity
- **Requests:** ~100/min (single instance)
- **Latency:** 2-5 seconds per analysis
- **Concurrent:** Limited by async handling

### Scaling Strategies

**Horizontal Scaling:**
- Deploy multiple API instances
- Load balancer (Nginx/AWS ALB)
- Shared vector DB and model storage

**Performance Optimization:**
- Redis caching for frequent queries
- Async RAG retrieval (parallel chunks)
- Model serving optimization (ONNX)
- Database connection pooling

**Cost Optimization:**
- Cache LLM responses (Redis)
- Batch embeddings generation
- Use smaller models for simple queries
- Rate limiting per user

---

## Monitoring & Observability

### Metrics to Track

**Application Metrics:**
- Request rate, latency, error rate
- Agent execution times
- Queue depths

**ML Metrics:**
- Prediction distribution
- Confidence score distribution
- Model drift detection

**RAG Metrics:**
- Retrieval latency
- Average relevance scores
- Cache hit rates

**LLM Metrics:**
- Token usage
- API costs
- Response validation failures

### Logging Strategy

**Levels:**
- DEBUG: Detailed flow
- INFO: Key operations
- WARNING: Unusual patterns
- ERROR: Failures

**Log Aggregation:**
- Centralized logging (ELK stack)
- Structured JSON logs
- Request tracing (correlation IDs)

---

## Security & Compliance

### API Security
- HTTPS only in production
- API key authentication (recommended)
- Rate limiting per client
- Input sanitization

### Data Security
- No PII storage (currently)
- Encrypted connections
- Environment variable secrets
- Regular security audits

### LLM Safety
- Output validation
- Content filtering
- Prompt injection protection
- Audit trails

---

## Deployment Options

### Option 1: Docker (Recommended)
```bash
docker-compose up -d
```
- Self-contained
- Easy scaling
- Environment isolation

### Option 2: Cloud Platforms

**AWS:**
- ECS/Fargate for containers
- S3 for data storage
- RDS for metadata
- Lambda for serverless

**Azure:**
- AKS for Kubernetes
- Cosmos DB for vector store
- App Service for API

**GCP:**
- Cloud Run for containers
- Vertex AI for models
- BigQuery for analytics

### Option 3: Kubernetes
- Production-grade orchestration
- Auto-scaling
- Service mesh
- CI/CD integration

---

## Testing Strategy

### Unit Tests
- Individual function testing
- Mock external dependencies
- Coverage target: 80%+

### Integration Tests
- End-to-end API tests
- Agent communication tests
- Database integration tests

### Performance Tests
- Load testing (Locust/k6)
- Stress testing
- Latency benchmarks

### Validation Tests
- Model performance on holdout set
- RAG retrieval accuracy
- LLM output quality

---

## Cost Analysis

### Development Costs
- OpenAI API: ~$0.01-0.03 per analysis
- Compute: ~$50-100/month (single instance)
- Storage: ~$5/month

### Production Costs (estimated for 10K requests/day)
- LLM API: ~$300-500/month
- Compute: ~$200-400/month (3-5 instances)
- Storage: ~$50/month
- Monitoring: ~$100/month

**Total:** ~$650-1050/month

### Cost Optimization
- Cache frequent queries (50% reduction)
- Use GPT-3.5 for simple cases (70% cheaper)
- Batch processing where possible
- Reserved instances for compute

---

## Future Architecture Enhancements

1. **Real-time Data Pipelines**
   - Kafka/Pulsar for streaming
   - Incremental model updates
   - Live market feeds

2. **Advanced ML**
   - Neural network ensembles
   - Bayesian uncertainty
   - Transfer learning

3. **Enhanced RAG**
   - Multi-modal embeddings (images)
   - Graph-based knowledge
   - Hybrid search (dense + sparse)

4. **Agentic Improvements**
   - Self-healing agents
   - Dynamic agent spawning
   - Learning from feedback

---

**This architecture prioritizes production readiness, scalability, and maintainability.**
