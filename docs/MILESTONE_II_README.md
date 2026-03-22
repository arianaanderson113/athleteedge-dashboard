# Project Milestone II Submission
## AthleteEdge Multi-Agent Workflow

**Student:** Ariana Anderson  
**Course:** CIS 3300  
**Date:** March 11, 2026

---

## 📦 Submission Contents

This submission includes:

1. **MILESTONE_II_DESIGN_DOCUMENT.md** - Complete 11-page design document
2. **agent-architecture.mermaid** - Mermaid diagram source code
3. **Architecture Diagram (Interactive)** - View in the Figma diagram tool above
4. **athleteedge_agents.py** - Python implementation skeleton
5. **requirements.txt** - Python dependencies

---

## 🎯 Multi-Agent System Overview

### Problem Solved
1. **Automated Lift Card Processing:** Scan lift cards/rehab sheets → auto-update athlete profiles
2. **Intelligent Comparisons:** Ask "Compare Ariana's ACL rehab to a basketball player's" → get detailed analysis

### Agent Architecture (5 Agents)

```
[ORCHESTRATOR] → Routes requests to appropriate pipeline
    ↓
[DOCUMENT PROCESSOR] → Extracts data from images (OCR)
    ↓
[VALIDATOR] → Verifies data quality
    ↓
[QUERY ANALYST] → Retrieves relevant athlete records
    ↓
[RESPONSE GENERATOR] → Creates human-readable answers
```

### Coordination Mechanism
- **Fixed pipeline with conditional branching**
- **Orchestrator** acts as central controller
- **Asynchronous processing** for image uploads
- **Stopping conditions:** Success/failure thresholds for each agent

---

## 🏗️ Agent Details

### Agent 1: Orchestrator
- **Role:** Request router
- **Input:** Image or text query
- **Output:** Routed to appropriate agent
- **Tools:** Request classification

### Agent 2: Document Processor
- **Role:** Extract structured data from images
- **Input:** Lift card/rehab sheet image
- **Output:** JSON workout data
- **Tools:** Claude Vision API, Google Cloud Vision (backup), regex parsers
- **Failure Handling:** Retry with backup API, request human review if confidence <75%

### Agent 3: Validator
- **Role:** Quality assurance
- **Input:** Extracted workout data
- **Output:** Approved/Flagged/Rejected status
- **Tools:** Pydantic schema validation, fuzzy string matching, domain logic rules
- **Stopping Condition:** Approve if confidence >90%, flag if 75-90%, reject if <75%

### Agent 4: Query Analyst
- **Role:** Understand queries & retrieve data
- **Input:** Natural language question
- **Output:** Relevant athlete records
- **Tools:** Claude API (entity extraction), SQL database, Vector DB (semantic search)
- **Failure Handling:** Ask clarifying questions, suggest alternative queries

### Agent 5: Response Generator
- **Role:** Natural language synthesis
- **Input:** Retrieved athlete data
- **Output:** Human-readable comparison
- **Tools:** Claude API (text generation), templating

---

## 📊 Data Flow Examples

### Example 1: Upload Lift Card
```
User uploads image
  → Orchestrator detects image_upload
  → Document Processor extracts exercises via OCR
  → Validator checks data quality (confidence=0.94)
  → Data saved to database
  → Success message to user
Time: 3-5 seconds
```

### Example 2: Comparative Query
```
Coach asks "Compare Ariana's ACL rehab to Christian Beam's"
  → Orchestrator detects text_query
  → Query Analyst extracts entities (Ariana, Christian, ACL)
  → Query Analyst retrieves both athletes' rehab records
  → Response Generator synthesizes comparison
  → Response displayed in chat
Time: 2-4 seconds
```

---

## 🛠️ Technology Stack

- **Language:** Python 3.11+
- **Framework:** LangChain for agent orchestration
- **AI APIs:** Anthropic Claude (Vision + Text)
- **Databases:** PostgreSQL (structured), ChromaDB (vector)
- **APIs:** FastAPI for REST endpoints
- **Libraries:** Pydantic, FuzzyWuzzy, Pillow, SQLAlchemy

---

## 📈 Evaluation Plan (Milestone III Preview)

### Metrics
1. **Document Processing Accuracy:** 85% auto-approval rate
2. **Query Understanding:** 90% intent classification accuracy
3. **Response Quality:** Average coach rating >4.0/5.0

### Test Data
- 50 real GSU lift cards (manually annotated)
- 100 representative coach queries
- User surveys from 5 GSU strength coaches

---

## 🚀 Running the Code

### Prerequisites
```bash
pip install -r requirements.txt
```

### Set API Key
```bash
export ANTHROPIC_API_KEY="your-key-here"
```

### Run Demo
```bash
python athleteedge_agents.py
```

**Note:** The demo uses simulated data. Full implementation with database integration coming in Final Submission.

---

## 📁 Repository Structure

```
athleteedge-dashboard/
├── frontend/
│   └── athleteedge-gsu-final.html    (Milestone I)
├── backend/
│   ├── athleteedge_agents.py         (Milestone II - Agent code)
│   ├── requirements.txt
│   └── database/
│       └── schema.sql
├── docs/
│   ├── MILESTONE_I_SUBMISSION.docx
│   ├── MILESTONE_II_DESIGN_DOCUMENT.md
│   └── diagrams/
│       └── agent-architecture.mermaid
└── README.md
```

---

## 🎓 Key Design Decisions

1. **Why 5 agents?** Clear separation of concerns - each agent has single responsibility
2. **Why Orchestrator pattern?** Centralized routing simplifies debugging and monitoring
3. **Why Validator Agent?** Data quality is critical for athletic decisions - can't risk bad data
4. **Why separate Query Analyst + Response Generator?** Retrieval and synthesis are distinct skills

---

## 🔮 Future Enhancements

1. **Multi-modal input:** Voice queries
2. **Predictive analytics:** Injury risk prediction
3. **Automated recommendations:** Program adjustments
4. **Mobile app:** On-field scanning

---

## ✅ Rubric Checklist

- [x] **At least 2 distinct agents** → We have 5
- [x] **Different roles** → Orchestrator, Processor, Validator, Analyst, Generator
- [x] **Defined coordination mechanism** → Orchestrated pipeline
- [x] **Architecture diagram** → Interactive diagram above + Mermaid source
- [x] **Design document (2-3 pages)** → 11 pages with full specifications
- [x] **Agent input/output formats** → Documented for all 5 agents
- [x] **Communication protocol** → JSON message passing defined
- [x] **Failure handling** → Retry strategies, escalation paths, stopping conditions
- [x] **Updated code** → athleteedge_agents.py with working skeleton

---

## 📧 Questions?

For questions about the implementation, see comments in `athleteedge_agents.py` or refer to Section 3 of the design document for detailed agent specifications.

---

**Total Time Invested:** ~20 hours (research, design, implementation, documentation)
