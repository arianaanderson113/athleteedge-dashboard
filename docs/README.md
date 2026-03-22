# AthleteEdge Dashboard

**Georgia State University Athletics Performance Tracking System**

---

## 📍 Project Status

- ✅ **Milestone I:** Front-End Interface - Complete
- ✅ **Milestone II:** Multi-Agent Workflow - Complete
- 🔄 **Milestone III:** Evaluation & Testing - In Progress

---

## 🎯 Project Overview

AthleteEdge is an AI-powered performance tracking platform for Georgia State University Athletics. The system combines document processing AI with natural language understanding to automate workout data entry and provide intelligent athlete comparisons.

---

## 🤖 Milestone II: Multi-Agent AI Features

### New Features Added

**1. Scan Lift Card**
- Upload photos of lift cards or rehab sheets
- AI automatically extracts workout data (exercises, sets, reps, weights)
- Validates data quality before saving
- One-click import to athlete profiles

**2. AI Assistant**
- Natural language query interface
- Compare rehabilitation protocols between athletes
- Analyze workout progression and trends
- Answer questions about athlete training history

### Multi-Agent Architecture

Our system uses a 5-agent pipeline:

1. **Orchestrator Agent** - Routes requests to appropriate processing pipeline
2. **Document Processor Agent** - Extracts structured data from images using OCR
3. **Validator Agent** - Verifies data quality and accuracy
4. **Query Analyst Agent** - Understands natural language queries
5. **Response Generator Agent** - Creates human-readable comparisons

**Coordination Mechanism:** Orchestrated pipeline with conditional branching and confidence-based stopping conditions.

---

## 📁 Repository Structure
```
athleteedge-dashboard/
├── README.md
├── docs/
│   ├── MILESTONE_II_DESIGN_DOCUMENT.md    (11-page technical spec)
│   ├── MILESTONE_II_README.md              (Submission guide)
│   ├── V2_UPDATE_README.md                 (Feature documentation)
│   ├── agent-architecture-diagram.png       (System diagram)
│   └── screenshots/                         (UI screenshots)
├── backend/
│   ├── athleteedge_agents.py               (Multi-agent implementation)
│   └── requirements.txt                     (Python dependencies)
└── frontend/
    └── athleteedge-gsu-professional.html   (Web interface)
```

---

## 🚀 Quick Start

### View the Interface

1. Download `frontend/athleteedge-gsu-professional.html`
2. Open in your web browser
3. Navigate through the 6 features:
   - Dashboard
   - Athlete Roster
   - Scan Lift Card (NEW)
   - Log Workout
   - Log Treatment
   - AI Assistant (NEW)

### Run the Backend
```bash
# Install dependencies
pip install -r backend/requirements.txt

# Set API key
export ANTHROPIC_API_KEY="your-key-here"

# Run demo
python backend/athleteedge_agents.py
```

---

## 📊 Technical Details

### Technology Stack

**Frontend:**
- HTML5, CSS3, Vanilla JavaScript
- Single-file application (no build required)
- Responsive design

**Backend:**
- Python 3.11+
- LangChain for agent orchestration
- Anthropic Claude API (Vision + Text)
- PostgreSQL + ChromaDB (planned)

**AI Features:**
- Document OCR with Claude Vision API
- Natural language understanding
- Semantic similarity search
- Automated data validation

---

## 📚 Documentation

- **[Design Document](docs/MILESTONE_II_DESIGN_DOCUMENT.md)** - Complete system architecture
- **[Agent Implementation](backend/athleteedge_agents.py)** - Python code with documentation
- **[Feature Guide](docs/V2_UPDATE_README.md)** - How to use new AI features
- **[Architecture Diagram](docs/agent-architecture-diagram.png)** - Visual system overview

---

## 🎓 Academic Project

**Course:** CIS 3300 - Software Requirements & Agile Development  
**Institution:** Georgia State University  
**Student:** Ariana Anderson  
**Term:** Spring 2026

---

## 📧 Contact

For questions about implementation details, see the documentation in the `docs/` folder or review inline code comments.

**Project Repository:** [https://github.com/yourusername/athleteedge-dashboard](https://github.com/yourusername/athleteedge-dashboard)
```

### Step 5: Save your changes

1. Scroll down to the bottom of the page
2. You'll see a section called **"Commit changes"**
3. In the first box, type: `Update README with Milestone II information`
4. Click the green **"Commit changes"** button

### Step 6: Verify it worked

1. Go back to your repository main page
2. Scroll down - you should see your new README displayed at the bottom
3. It should have sections for Milestone II, features, and documentation links

---

## ⚠️ IMPORTANT: Replace Your Username

In the README, find this line at the very bottom:
```
**Project Repository:** [https://github.com/yourusername/athleteedge-dashboard]
```

**Change `yourusername`** to your actual GitHub username!

---

## 📋 What This README Includes

✅ **Project status** - Shows both milestones complete  
✅ **Feature descriptions** - Explains Scan Lift Card + AI Assistant  
✅ **Architecture overview** - Lists all 5 agents  
✅ **Repository structure** - Shows where all files are  
✅ **Quick start guide** - How to run the interface  
✅ **Documentation links** - Points to all your docs  
✅ **Professional formatting** - Clean, organized, academic  

---

## 🎯 Quick Visual Guide

**Before (old README):**
```
# AthleteEdge Dashboard
Some basic info...
```

**After (your new README):**
```
# AthleteEdge Dashboard
Georgia State University Athletics Performance Tracking System

📍 Project Status
✅ Milestone I: Complete
✅ Milestone II: Complete

🤖 Multi-Agent AI Features
[Detailed description of your system]

📁 Repository Structure
[Clean file organization]

📚 Documentation
[Links to all your docs]
