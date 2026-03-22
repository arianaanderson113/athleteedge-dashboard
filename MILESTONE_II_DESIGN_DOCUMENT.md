# Project Milestone II: Multi-Agent Workflow Design
## AthleteEdge Intelligence Platform

**Student:** Ariana Anderson  
**Course:** CIS 3300 - Software Requirements & Agile Development  
**Date:** March 11, 2026

---

## 1. Executive Summary

The AthleteEdge Intelligence Platform extends the front-end dashboard (Milestone I) with a sophisticated multi-agent workflow that addresses two critical pain points in athletic performance management:

1. **Automated Data Entry:** Student-athletes and coaches can scan lift cards or rehab sheets, and the system automatically extracts structured data and updates athlete profiles.

2. **Intelligent Comparative Analysis:** Athletic trainers and coaches can ask natural language questions like "Compare Ariana's ACL rehab protocol to a basketball player's ACL rehab" and receive detailed, evidence-based comparisons.

This multi-agent system combines document processing, data validation, semantic search, and natural language generation to create an intelligent assistant for Georgia State Athletics.

---

## 2. System Architecture Overview

### 2.1 High-Level Workflow

The system employs a **5-agent orchestrated pipeline** with two primary workflows:

**Workflow A: Document Processing Pipeline**
```
Lift Card Image → Orchestrator → Document Processor → Validator → Database
```

**Workflow B: Query Analysis Pipeline**
```
Natural Language Query → Orchestrator → Query Analyst → Response Generator → User
```

### 2.2 Agent Roles

| Agent | Role | Primary Responsibility |
|-------|------|----------------------|
| **Orchestrator** | Router & Controller | Determines request type and routes to appropriate agent |
| **Document Processor** | Data Extractor | Converts images to structured JSON data |
| **Validator** | Quality Assurance | Verifies extracted data accuracy and completeness |
| **Query Analyst** | Information Retrieval | Retrieves relevant athlete records for comparison |
| **Response Generator** | Natural Language Synthesis | Creates human-readable answers from data |

---

## 3. Detailed Agent Specifications

### 3.1 Orchestrator Agent

**Purpose:** Intelligent routing of incoming requests to the appropriate processing pipeline.

**Input Format:**
```json
{
  "request_type": "image_upload" | "text_query",
  "content": <base64_image> | <string>,
  "user_id": "string",
  "timestamp": "ISO8601"
}
```

**Output Format:**
```json
{
  "routed_to": "document_processor" | "query_analyst",
  "priority": "high" | "medium" | "low",
  "metadata": {
    "athlete_id": "optional",
    "sport": "optional"
  }
}
```

**Decision Logic:**
- **If request contains image data** → Route to Document Processor
- **If request is text query** → Route to Query Analyst
- **If ambiguous** → Request clarification from user

**Tools Used:**
- Request classification (simple keyword/content-type detection)
- Session management

---

### 3.2 Document Processor Agent

**Purpose:** Extract structured workout/rehab data from uploaded images (lift cards, rehab sheets).

**Input Format:**
```json
{
  "image_data": "<base64_encoded_image>",
  "athlete_id": "optional",
  "document_type": "lift_card" | "rehab_sheet" | "unknown"
}
```

**Processing Steps:**
1. **Image Preprocessing:** Enhance contrast, deskew, denoise
2. **OCR Extraction:** Use Claude Vision API or Google Cloud Vision to extract all text
3. **Table Detection:** Identify structured data (sets, reps, weights, exercises)
4. **Data Parsing:** Convert to JSON schema matching database structure

**Output Format:**
```json
{
  "athlete_id": "1",
  "athlete_name": "Ariana Anderson",
  "document_type": "lift_card",
  "date": "2026-03-10",
  "phase": "Week 9-10 Spring",
  "workouts": [
    {
      "exercise": "Goblet Squat",
      "sets": 4,
      "reps": 8,
      "weight_lbs": 45,
      "notes": "73% max intensity"
    },
    {
      "exercise": "BB RDL",
      "sets": 3,
      "reps": 6,
      "weight_lbs": 115,
      "notes": "Focus on hip hinge"
    }
  ],
  "confidence_score": 0.92
}
```

**Tools/APIs Used:**
- **Anthropic Claude Vision API** (primary OCR)
- **Google Cloud Vision API** (backup OCR for low confidence)
- Custom regex parsers for exercise names, sets/reps patterns
- Schema validation library (Pydantic/Zod)

**Error Handling:**
- **Low confidence (<0.75):** Flag for human review
- **Missing critical fields (athlete_id, date):** Request user input
- **OCR failures:** Retry with alternative API, then escalate to manual entry

---

### 3.3 Validator Agent

**Purpose:** Ensure extracted data quality before committing to database.

**Input Format:** (Same as Document Processor output)

**Validation Checks:**
1. **Schema Compliance**
   - All required fields present (athlete_id, date, exercises)
   - Data types correct (numbers for sets/reps/weight)
   
2. **Domain Logic Validation**
   - Exercise names match known exercise library (fuzzy matching)
   - Weight values are physiologically realistic (e.g., back squat 50-500 lbs)
   - Sets/reps in typical ranges (1-10 sets, 1-20 reps)
   - Dates are not in the future
   
3. **Confidence Scoring**
   - OCR confidence (from Document Processor)
   - Field completeness (% of expected fields populated)
   - Data plausibility (values within expected ranges)

**Output Format:**
```json
{
  "validation_status": "approved" | "flagged" | "rejected",
  "confidence_score": 0.92,
  "issues": [
    {
      "field": "workouts[1].weight_lbs",
      "issue": "Unusually high value (450 lbs for Goblet Squat)",
      "severity": "warning"
    }
  ],
  "approved_for_database": true
}
```

**Decision Rules:**
- **Confidence > 0.90** → Auto-approve
- **Confidence 0.75-0.90** → Flag for coach review, but save tentatively
- **Confidence < 0.75** → Reject, request manual entry

**Tools Used:**
- Pydantic for schema validation
- Custom rule engine for domain logic
- Fuzzy string matching (FuzzyWuzzy library) for exercise names

---

### 3.4 Query Analyst Agent

**Purpose:** Understand natural language queries and retrieve relevant athlete data for comparison.

**Input Format:**
```json
{
  "query": "Compare Ariana's ACL rehab to a basketball player's ACL rehab",
  "user_id": "coach_123",
  "context": {
    "current_athlete_view": "Ariana Anderson"
  }
}
```

**Processing Steps:**
1. **Intent Classification**
   - Comparison query vs. single athlete lookup
   - Time-based query (recent vs. all-time)
   - Specific metric query (exercises, weights, duration)

2. **Entity Extraction**
   - Athlete names (Ariana)
   - Sports (basketball)
   - Injury types (ACL)
   - Time ranges (implicit: all ACL rehab data)

3. **Database Query Construction**
   ```sql
   -- Retrieve Ariana's ACL rehab records
   SELECT * FROM treatments 
   WHERE athlete_id = 1 
   AND treatment_type LIKE '%ACL%'
   ORDER BY date DESC;
   
   -- Retrieve basketball player ACL rehab records
   SELECT * FROM treatments t
   JOIN athletes a ON t.athlete_id = a.id
   WHERE a.sport = 'Basketball'
   AND t.treatment_type LIKE '%ACL%'
   ORDER BY date DESC;
   ```

4. **Semantic Search** (for similar protocols)
   - Embed all rehab protocols in vector database
   - Find k-nearest neighbors to Ariana's protocol
   - Filter by sport if specified

**Output Format:**
```json
{
  "athlete_data": {
    "ariana": {
      "total_sessions": 24,
      "duration_weeks": 16,
      "exercises": ["Quad Activation", "Box Squats", "Single-Leg Deadlift"],
      "progression": "Week 1-4: ROM, Week 5-8: Strength, Week 9-12: Power"
    },
    "basketball_comparison": {
      "average_sessions": 22,
      "average_duration_weeks": 14,
      "common_exercises": ["Quad Activation", "Box Squats"],
      "unique_exercises_bball": ["Vertical Jump Training", "Cutting Drills"]
    }
  },
  "semantic_matches": [
    {
      "athlete": "Christian Beam (Men's Basketball)",
      "similarity_score": 0.87,
      "protocol_overlap": ["Quad focus", "Progressive loading"]
    }
  ]
}
```

**Tools/APIs Used:**
- **SQL Database** (PostgreSQL) for structured queries
- **Vector Database** (Pinecone/Chroma) for semantic similarity search
- **LangChain** for query parsing and entity extraction
- **Anthropic Claude API** for intent classification

---

### 3.5 Response Generator Agent

**Purpose:** Synthesize retrieved data into natural, human-readable answers.

**Input Format:** (Same as Query Analyst output)

**Processing Steps:**
1. **Data Aggregation:** Combine database results and semantic matches
2. **Comparison Analysis:** Identify differences, similarities, trends
3. **Natural Language Generation:** Use LLM to create coach-friendly response

**Output Format:**
```json
{
  "response_text": "Ariana's ACL rehab protocol (16 weeks, 24 sessions) is slightly longer than the basketball player average (14 weeks, 22 sessions). Key differences:\n\n**Similarities:**\n- Both emphasize quad activation and box squats early in rehab\n- Progressive loading from ROM → Strength → Power\n\n**Differences:**\n- Ariana's protocol includes more single-leg stability work (relevant for goalkeeper lateral movements)\n- Basketball players add vertical jump training earlier (Week 6 vs. Week 10)\n- Ariana's cutting drill progression is more conservative due to goalkeeper-specific movement patterns\n\n**Most Similar Protocol:** Christian Beam (Men's Basketball) - 87% overlap in exercise selection and progression timeline.",
  "structured_data": {
    "comparison_table": [
      {"metric": "Duration", "ariana": "16 weeks", "basketball_avg": "14 weeks"},
      {"metric": "Sessions", "ariana": "24", "basketball_avg": "22"}
    ]
  },
  "confidence": 0.94
}
```

**Tools/APIs Used:**
- **Anthropic Claude API** (primary LLM for synthesis)
- Template-based generation for structured sections
- Data visualization hints (for front-end rendering)

---

## 4. Agent Communication Protocol

### 4.1 Message Passing Format

All inter-agent communication uses a standardized JSON message structure:

```json
{
  "from_agent": "string",
  "to_agent": "string",
  "message_type": "data" | "control" | "error",
  "payload": { /* agent-specific data */ },
  "correlation_id": "uuid",
  "timestamp": "ISO8601"
}
```

### 4.2 Coordination Mechanism

**Fixed Pipeline with Conditional Branching:**

- **Orchestrator** acts as central coordinator
- Agents communicate via message queue (in production) or function calls (in MVP)
- **No direct agent-to-agent communication** - all routing through Orchestrator
- **Asynchronous processing** for image uploads (long-running OCR tasks)

### 4.3 Stopping Conditions

**Document Processing Pipeline:**
- **Success:** Data validated and committed to database
- **Failure:** Confidence too low → Request human review
- **Max retries (3):** Escalate to manual data entry

**Query Analysis Pipeline:**
- **Success:** Response generated and displayed to user
- **Failure:** No matching data found → Suggest alternative queries
- **Ambiguous query:** Request clarification from user

---

## 5. Failure Handling & Recovery

### 5.1 Document Processor Failures

| Failure Mode | Detection | Recovery Strategy |
|--------------|-----------|-------------------|
| **OCR API timeout** | No response after 30s | Retry with backup API (Google Vision) |
| **Unreadable image** | Confidence < 0.5 | Request higher quality image from user |
| **Unknown exercise names** | >50% exercises not in library | Fuzzy match + suggest to user for confirmation |
| **Missing athlete identification** | No name/ID extracted | Prompt user to select athlete from dropdown |

### 5.2 Query Analyst Failures

| Failure Mode | Detection | Recovery Strategy |
|--------------|-----------|-------------------|
| **Ambiguous query** | Multiple valid interpretations | Ask clarifying question (e.g., "Which basketball player?") |
| **No matching data** | Empty result set | Suggest broadening criteria or related queries |
| **Database timeout** | Query > 10s | Optimize query, add indexes, or paginate results |

### 5.3 System-Wide Failures

- **Agent crash:** Orchestrator detects timeout, restarts agent, retries request
- **Database unavailable:** Queue requests, retry with exponential backoff
- **API rate limits:** Implement token bucket algorithm, queue excess requests

---

## 6. Data Flow Examples

### 6.1 Example 1: Uploading a Lift Card

**User Action:** Ariana uploads a photo of her Week 9-10 lift card

**System Flow:**
```
1. User uploads image via Front-End Interface
2. Orchestrator receives request, identifies as image_upload
3. Orchestrator routes to Document Processor
4. Document Processor:
   - Calls Claude Vision API
   - Extracts: Athlete="Ariana Anderson", Exercises=[Goblet Squat 4x8@45lbs, BB RDL 3x6@115lbs]
   - Returns JSON with confidence=0.94
5. Validator receives data:
   - Checks schema ✓
   - Validates exercise names (fuzzy match to "Goblet Squat" in library) ✓
   - Checks weight plausibility (45 lbs for goblet squat = reasonable) ✓
   - Approves for database
6. Data committed to database
7. Front-End displays success message + updated athlete profile
```

**Total Time:** ~3-5 seconds

---

### 6.2 Example 2: Comparative Query

**User Action:** Coach asks "Compare Ariana's ACL rehab to Christian Beam's"

**System Flow:**
```
1. User types query in chatbot interface
2. Orchestrator identifies as text_query, routes to Query Analyst
3. Query Analyst:
   - Extracts entities: Athlete1="Ariana Anderson", Athlete2="Christian Beam", Topic="ACL rehab"
   - Queries database:
     * Ariana's ACL treatment records (24 sessions found)
     * Christian's ACL treatment records (22 sessions found)
   - Performs semantic search in Vector DB for similar protocols
4. Query Analyst sends structured comparison to Response Generator
5. Response Generator:
   - Uses Claude API to synthesize natural language response
   - Highlights similarities (both quad-focused) and differences (Ariana more conservative)
   - Returns formatted response
6. Front-End displays comparison in chat interface
```

**Total Time:** ~2-4 seconds

---

## 7. Technology Stack

### 7.1 Agent Framework
- **LangChain** for agent orchestration and tool calling
- **Python 3.11+** as primary language
- **FastAPI** for RESTful API endpoints

### 7.2 External APIs & Tools
- **Anthropic Claude API** (Vision + text generation)
- **Google Cloud Vision API** (backup OCR)
- **Pinecone** or **ChromaDB** (vector database)
- **PostgreSQL** (relational database)

### 7.3 Libraries
- **Pydantic** (data validation)
- **FuzzyWuzzy** (string matching)
- **Pillow** (image preprocessing)
- **SQLAlchemy** (ORM)

---

## 8. Performance & Scalability Considerations

### 8.1 Expected Load
- **Document uploads:** ~50-100 per day (coaches upload post-practice)
- **Queries:** ~200-300 per day (coaches checking athlete progress)
- **Peak times:** Weekday afternoons (3-6 PM) after practices

### 8.2 Optimization Strategies
- **Caching:** Cache common queries (e.g., "all Women's Soccer athletes")
- **Indexing:** Database indexes on athlete_id, date, sport, exercise
- **Batch processing:** Process multiple lift cards simultaneously
- **Lazy loading:** Load athlete history on-demand, not proactively

### 8.3 Scalability Plan
- **Horizontal scaling:** Deploy agents as microservices, scale independently
- **Load balancing:** Distribute OCR requests across multiple API keys
- **Database sharding:** Partition by sport or season if data volume grows

---

## 9. Evaluation Criteria (Preview for Milestone III)

### 9.1 Document Processor Accuracy
- **Metric:** % of lift cards extracted with >90% accuracy
- **Target:** 85% auto-approval rate
- **Test set:** 50 manually annotated lift cards from GSU archives

### 9.2 Query Understanding
- **Metric:** % of queries correctly interpreted
- **Target:** 90% intent classification accuracy
- **Test set:** 100 representative coach queries

### 9.3 Response Quality
- **Metric:** Coach satisfaction rating (1-5 scale)
- **Target:** Average rating >4.0
- **Method:** User survey after each query response

---

## 10. Future Enhancements

1. **Multi-modal input:** Support voice queries ("Hey AthleteEdge, how is Ariana's knee rehab progressing?")
2. **Predictive analytics:** ML model to predict injury risk based on training load
3. **Automated recommendations:** "Ariana's squat weight hasn't increased in 3 weeks - consider adjusting program"
4. **Coach collaboration:** Tag other coaches in query responses for collaborative decision-making
5. **Mobile app:** Native iOS/Android for on-field lift card scanning

---

## 11. Conclusion

The AthleteEdge multi-agent system transforms athletic performance tracking from a manual, time-intensive process to an intelligent, automated platform. By combining document processing AI with semantic search and natural language understanding, the system empowers coaches and trainers to make faster, more informed decisions about athlete development and injury recovery.

The 5-agent architecture provides clear separation of concerns, enabling independent testing and iterative improvement of each component. The fixed pipeline with conditional branching ensures predictable behavior while allowing flexibility for complex queries.

**Next Steps (Milestone III):** Implement full system, conduct user testing with GSU strength coaches, and evaluate accuracy metrics on real lift cards and rehab sheets.

---

## Appendix A: Database Schema

```sql
-- Athletes table
CREATE TABLE athletes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    sport VARCHAR(100),
    position VARCHAR(100),
    year VARCHAR(50),
    status VARCHAR(50)
);

-- Workouts table
CREATE TABLE workouts (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    date DATE,
    exercise VARCHAR(255),
    sets INTEGER,
    reps INTEGER,
    weight_lbs DECIMAL,
    duration_minutes INTEGER,
    notes TEXT,
    confidence_score DECIMAL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Treatments table
CREATE TABLE treatments (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    date DATE,
    treatment_type VARCHAR(255),
    body_area VARCHAR(255),
    duration_minutes INTEGER,
    notes TEXT,
    followup_needed BOOLEAN,
    confidence_score DECIMAL,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Vector embeddings table
CREATE TABLE rehab_embeddings (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER REFERENCES athletes(id),
    protocol_text TEXT,
    embedding VECTOR(1536),  -- OpenAI ada-002 dimensions
    metadata JSONB
);
```

---

## Appendix B: Example API Request/Response

### Upload Lift Card
**Request:**
```http
POST /api/v1/upload-lift-card
Content-Type: multipart/form-data

{
  "image": <binary_data>,
  "athlete_id": 1 (optional)
}
```

**Response:**
```json
{
  "status": "success",
  "data": {
    "workouts_extracted": 5,
    "confidence": 0.94,
    "athlete": "Ariana Anderson",
    "date": "2026-03-10"
  },
  "warnings": []
}
```

### Ask Query
**Request:**
```http
POST /api/v1/query
Content-Type: application/json

{
  "query": "Compare Ariana's ACL rehab to Christian Beam's",
  "user_id": "coach_123"
}
```

**Response:**
```json
{
  "status": "success",
  "response": "Ariana's ACL rehab protocol (16 weeks...",
  "structured_data": { /* comparison table */ },
  "confidence": 0.94
}
```
