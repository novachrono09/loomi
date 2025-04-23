# Loomi Architecture Overview

## System Components

### 1. Frontend
- **Technology**: Next.js with TypeScript
- **Features**:
  - AI-powered product discovery
  - Emotion-adaptive UI
  - Visual search
  - Zero-party data marketplace integration
- **Communication**: GraphQL with backend

### 2. Backend
- **Technology**: NestJS with GraphQL
- **Features**:
  - User authentication (JWT + Magic Links)
  - Product catalog management
  - Order processing
  - Cart management
  - Integration with microservices
- **Database**: PostgreSQL with Prisma ORM

### 3. Microservices

#### AI Orchestrator
- **Technology**: FastAPI (Python)
- **Features**:
  - Natural language processing for chat
  - Visual search processing
  - Emotion analysis for adaptive UI

#### Pricing Engine
- **Technology**: FastAPI (Python)
- **Features**:
  - Dynamic pricing algorithms
  - Market trend analysis
  - Competitor price monitoring

#### Supply Chain
- **Technology**: FastAPI (Python)
- **Features**:
  - Inventory prediction
  - Shipping estimation
  - Supplier risk analysis

### 4. Infrastructure
- **Local Development**: Docker Compose with:
  - PostgreSQL
  - Redis
  - ElasticSearch
  - Prometheus + Grafana
- **Production**: Terraform for AWS ECS Fargate deployment

## Data Flow

1. **User Interaction**:
   - Frontend handles UI/UX
   - Sends requests to backend via GraphQL

2. **Backend Processing**:
   - Handles core business logic
   - Orchestrates microservice calls when needed
   - Manages database interactions

3. **Specialized Processing**:
   - AI, pricing, and supply chain tasks delegated to microservices
   - Results aggregated by backend

4. **Data Storage**:
   - PostgreSQL for transactional data
   - Redis for caching
   - ElasticSearch for product search

## Security

- **Authentication**: JWT with OAuth2 and magic links
- **Authorization**: Role-based access control
- **Data Protection**: Encryption at rest and in transit
- **Monitoring**: Prometheus metrics + Sentry error tracking