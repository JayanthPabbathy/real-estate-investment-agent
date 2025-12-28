# Setup and Deployment Guide

## Prerequisites

### System Requirements
- **OS:** Windows 10/11, Ubuntu 20.04+, or macOS 12+
- **Python:** 3.11 or higher
- **RAM:** Minimum 8GB (16GB recommended)
- **Storage:** 5GB free space
- **Internet:** Required for OpenAI API calls

### Required Accounts
- OpenAI API account with GPT-4 access
- (Optional) Docker Hub account for custom images

---

## Installation Methods

### Method 1: Local Installation (Recommended for Development)

#### Step 1: Clone Repository
```bash
git clone <repository-url>
cd "Real Estate Agent"
```

#### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

#### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

#### Step 4: Configure Environment Variables
```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

Edit `.env` file:
```env
OPENAI_API_KEY=sk-your-actual-openai-key-here
OPENAI_MODEL=gpt-4-turbo-preview
DEBUG=True
LOG_LEVEL=INFO
```

#### Step 5: Initialize Data (First Run Only)
```bash
python src/data_generation.py
```

This generates:
- `data/properties_data.csv` - 5000 property records
- `data/market_documents.json` - Market intelligence
- `data/regulatory_documents.json` - Compliance docs

#### Step 6: Train Models (First Run Only)
```bash
python src/models/predictive_models.py
```

This creates:
- `models/price_model.joblib`
- `models/rent_model.joblib`
- `models/scaler.joblib`
- `models/label_encoders.joblib`
- `models/metadata.json`

#### Step 7: Setup Vector Database
```bash
python src/rag/vector_store.py
```

This initializes ChromaDB and indexes documents.

#### Step 8: Start the Server
```bash
python src/api/main.py
```

Server starts at `http://localhost:8000`

#### Step 9: Verify Installation
```bash
# In another terminal
curl http://localhost:8000/health
```

Expected output:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "models_loaded": true,
  "vector_db_status": "connected"
}
```

---

### Method 2: Docker Installation (Recommended for Production)

#### Step 1: Prerequisites
```bash
# Verify Docker is installed
docker --version
docker-compose --version
```

#### Step 2: Configure Environment
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

#### Step 3: Build and Run
```bash
# Build image
docker build -t real-estate-intelligence .

# Run container
docker run -d \
  -p 8000:8000 \
  -e OPENAI_API_KEY=your_key_here \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/reports:/app/reports \
  --name real-estate-api \
  real-estate-intelligence
```

Or use Docker Compose:
```bash
docker-compose up -d
```

#### Step 4: Check Logs
```bash
docker-compose logs -f
```

#### Step 5: Access Application
- API: `http://localhost:8000`
- Docs: `http://localhost:8000/docs`

#### Step 6: Stop Services
```bash
docker-compose down
```

---

## Configuration Options

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `OPENAI_API_KEY` | OpenAI API key | - | ✅ Yes |
| `OPENAI_MODEL` | LLM model name | gpt-4-turbo-preview | No |
| `OPENAI_EMBEDDING_MODEL` | Embedding model | text-embedding-3-small | No |
| `API_HOST` | API host | 0.0.0.0 | No |
| `API_PORT` | API port | 8000 | No |
| `DEBUG` | Debug mode | False | No |
| `LOG_LEVEL` | Logging level | INFO | No |
| `VECTOR_DB_PATH` | Vector DB location | ./data/vector_db | No |
| `MODEL_CACHE_DIR` | Model storage | ./models | No |

### Advanced Configuration

Edit `src/config.py` for:
- Data generation parameters
- Model hyperparameters
- RAG retrieval settings
- API rate limits

---

## Testing

### Run Unit Tests
```bash
pytest tests/test_system.py -v
```

### Run API Tests
```bash
# Start server first
python src/api/main.py

# In another terminal
python tests/test_api.py
```

### Run All Tests with Coverage
```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report: `htmlcov/index.html`

---

## Troubleshooting

### Issue: "OpenAI API key not found"
**Solution:**
```bash
# Verify .env file exists and contains key
cat .env | grep OPENAI_API_KEY

# Ensure environment is activated
echo $VIRTUAL_ENV  # Should show venv path
```

### Issue: "Models not found"
**Solution:**
```bash
# Train models manually
python src/models/predictive_models.py
```

### Issue: "ChromaDB error"
**Solution:**
```bash
# Delete and recreate vector DB
rm -rf data/vector_db
python src/rag/vector_store.py
```

### Issue: "Port 8000 already in use"
**Solution:**
```bash
# Find process using port
# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F

# Linux/Mac
lsof -i :8000
kill -9 <pid>

# Or change port in .env
API_PORT=8001
```

### Issue: "Out of memory"
**Solution:**
- Reduce `SYNTHETIC_DATA_SIZE` in config
- Use smaller embedding model
- Increase system RAM allocation

### Issue: Docker build fails
**Solution:**
```bash
# Clear Docker cache
docker system prune -a

# Rebuild without cache
docker build --no-cache -t real-estate-intelligence .
```

---

## Production Deployment

### AWS Deployment

#### Option 1: EC2
```bash
# Launch EC2 instance (t3.medium or larger)
# Install Docker
sudo yum install docker -y
sudo service docker start

# Clone and deploy
git clone <repo>
cd "Real Estate Agent"
docker-compose up -d

# Configure security group: Allow port 8000
```

#### Option 2: ECS/Fargate
1. Push image to ECR
```bash
aws ecr create-repository --repository-name real-estate-intelligence
docker tag real-estate-intelligence:latest <ecr-url>
docker push <ecr-url>
```

2. Create ECS task definition
3. Create ECS service
4. Configure load balancer

### Azure Deployment

#### Azure Container Instances
```bash
# Login
az login

# Create resource group
az group create --name real-estate-rg --location eastus

# Create container instance
az container create \
  --resource-group real-estate-rg \
  --name real-estate-api \
  --image real-estate-intelligence \
  --dns-name-label real-estate-api \
  --ports 8000 \
  --environment-variables OPENAI_API_KEY=$OPENAI_API_KEY
```

### GCP Deployment

#### Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/PROJECT_ID/real-estate-intelligence

# Deploy
gcloud run deploy real-estate-api \
  --image gcr.io/PROJECT_ID/real-estate-intelligence \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars OPENAI_API_KEY=$OPENAI_API_KEY
```

---

## Monitoring Setup

### Application Monitoring

#### Prometheus + Grafana
```yaml
# docker-compose.monitoring.yml
version: '3.8'
services:
  prometheus:
    image: prom/prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana
    ports:
      - "3000:3000"
```

#### Log Aggregation (ELK Stack)
```bash
docker run -d -p 5601:5601 -p 9200:9200 -p 5044:5044 \
  sebp/elk
```

### Performance Monitoring
```python
# Add to main.py
from prometheus_client import Counter, Histogram

request_count = Counter('api_requests_total', 'Total API requests')
request_duration = Histogram('api_request_duration_seconds', 'API request duration')
```

---

## Backup and Recovery

### Data Backup
```bash
# Backup data directory
tar -czf backup_$(date +%Y%m%d).tar.gz data/ models/ reports/

# Upload to cloud storage
aws s3 cp backup_*.tar.gz s3://your-bucket/backups/
```

### Automated Backups (Cron)
```bash
# Add to crontab
0 2 * * * cd /path/to/app && ./backup.sh
```

### Recovery
```bash
# Restore from backup
tar -xzf backup_20240101.tar.gz
python src/api/main.py
```

---

## Scaling Guidelines

### Vertical Scaling
- Increase CPU/RAM for single instance
- Recommended: 4 vCPU, 16GB RAM for production

### Horizontal Scaling
```yaml
# docker-compose.scale.yml
version: '3.8'
services:
  api:
    deploy:
      replicas: 3
```

```bash
docker-compose up --scale api=3
```

### Load Balancing
```nginx
# nginx.conf
upstream api_backend {
    server api1:8000;
    server api2:8000;
    server api3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://api_backend;
    }
}
```

---

## Maintenance

### Regular Tasks
- [ ] Weekly: Review logs for errors
- [ ] Monthly: Update dependencies
- [ ] Quarterly: Retrain models
- [ ] Annually: Security audit

### Dependency Updates
```bash
# Check outdated packages
pip list --outdated

# Update specific package
pip install --upgrade <package>

# Update all
pip install --upgrade -r requirements.txt
```

### Model Retraining
```bash
# Update data
python src/data_generation.py

# Retrain models
python src/models/predictive_models.py

# Restart API
docker-compose restart
```

---

## Support

For issues:
1. Check logs: `logs/api_*.log`
2. Run health check: `/health` endpoint
3. Verify configuration: `.env` file
4. Review documentation: `README.md`

---

**Deployment checklist completed? Start serving investment intelligence!** 🚀
