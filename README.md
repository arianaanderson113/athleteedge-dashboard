# AthleteEdge AI - Multi-Agent Performance Intelligence System

A multi-agent artificial intelligence system for Georgia State University Athletics that centralizes athlete performance tracking, enables cross-team comparisons, and provides AI-powered insights with research citations.

## 🎯 Project Overview

**Problem Statement:** Athletic departments lack a centralized system to track athlete performance across teams, preventing coaches from comparing progress and making data-driven training decisions.

**Solution:** AthleteEdge AI is a 4-agent system that:
- Centralizes workout data across all sports
- Enables natural language queries for performance insights
- Protects athlete privacy through role-based access
- Grounds recommendations in sports medicine research

## 📁 Repository Structure

```
athleteedge_submission/
├── athleteedge_final.py          # Complete system implementation
├── README.md                      # This file
├── evaluation_test_cases.json    # Test cases for evaluation
├── evaluation_script.py           # Automated evaluation script
├── architecture_diagram.png       # System architecture visualization
├── requirements.txt               # Python dependencies
└── AthleteEdge_Final_Report.docx  # Complete project report
```

## 🏗️ System Architecture

### Four-Agent Pipeline:

1. **Privacy Filter Agent** - Blocks inappropriate queries (homework, demeaning comparisons)
2. **Database Query Agent** - Role-based data filtering and metric calculation
3. **AI Response Generator** - Google Gemini API for natural language responses
4. **Citation Validator** - Adds sports medicine research references

See `architecture_diagram.png` for visual representation.

## 🔧 Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))

### Installation Steps

1. **Clone or extract this repository:**
   ```bash
   cd athleteedge_submission
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation:**
   ```bash
   python -c "import flask; import google.generativeai; print('✅ All dependencies installed!')"
   ```

## 🚀 Running the System Locally

### Start the Server

```bash
python athleteedge_final.py
```

You should see:
```
====================================================
🏋️ ATHLETEEDGE - COMPLETE SYSTEM
====================================================

✨ NEW: Workout Logging + Progress Tracking!

📱 http://localhost:5000
👤 Student: aanderson42 / Password123!
👨‍🏫 Coach: jsmith5 / Coach456#

====================================================
```

### Access the Application

1. Open your browser to: **http://localhost:5000**

2. **Login with demo credentials:**
   - **Student:** `aanderson42` / `Password123!`
   - **Coach:** `jsmith5` / `Coach456#`

3. **Initialize the system:**
   - Paste your Google Gemini API key
   - Click "Initialize System"
   - Wait for "✓ System Ready"

4. **Try example queries:**
   - "Show my progress over the last month" (student)
   - "Who has improved the most in squats?" (coach)
   - "Compare Ariana and Emily's ACL recovery" (coach)

### Stopping the Server

Press `Ctrl+C` in the terminal.

## 📊 System Data

The system includes:
- **15 real GSU athletes** across 7 sports
- **450+ workout records** with 12-week progressive data
- **2 ACL recovery cases** (Ariana Anderson & Emily Glenn) at 11 weeks post-op
- **Week-by-week rehab protocols** based on sports medicine research

## 🧪 Running Evaluation Scripts

### Automated Evaluation

```bash
python evaluation_script.py
```

This will:
1. Test all 20 evaluation queries
2. Measure response accuracy, privacy enforcement, and response time
3. Output results to console
4. Generate `evaluation_results.json`

### Expected Output

```
====================================================
ATHLETEEDGE AI EVALUATION
====================================================

Testing 20 queries across student and coach roles...

✅ Privacy Filter: 5/5 blocked (100%)
✅ Response Accuracy: 18/19 correct (95%)
✅ Average Response Time: 2.14s
✅ Citation Inclusion: 15/19 medical claims (79%)

Full results saved to: evaluation_results.json
====================================================
```

### Manual Testing

You can also test individual queries in the web interface:

**Student View (aanderson42):**
- "Show my ACL recovery progress"
- "When can I return to soccer?"
- "Compare my recovery to Emily's" (should block)

**Coach View (jsmith5):**
- "Who has improved the most in squats?"
- "Compare Ariana and Emily's ACL recovery"
- "Compare basketball vs football squat strength"
- "Who is weakest?" (should block)

## 🔐 User Roles & Permissions

### Student Athletes
- View only personal workout data
- Cannot compare to other athletes
- Track own injury recovery
- Log personal workouts

### Coaches
- View all 15 athletes across 7 sports
- Compare progress between athletes and teams
- Track team statistics
- Log workouts for entire team
- Monitor injury recoveries

## 📈 Key Features

### Privacy Protection
- Role-based database filtering
- Privacy Filter agent blocks inappropriate queries
- Session-based authentication
- Students cannot access others' data

### Progressive Training Data
- Realistic 3% weekly improvement curves
- Base weights to +36% over 12 weeks
- Multiple exercises: Squat, Bench, Deadlift, Power Clean

### ACL Rehabilitation Tracking
- Week-by-week protocols (11 weeks post-op)
- Progression: Ankle pumps → Back squats → Plyometrics
- Based on AJSM and JOSPT research
- Comparative analysis between athletes

### AI-Powered Insights
- Google Gemini API integration
- Natural language query processing
- Research citations (AJSM, JOSPT, BJSM)
- 2-3 paragraph responses with context

## 🐛 Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt --break-system-packages
```

### "API key invalid" error
- Verify your Gemini API key at https://aistudio.google.com/app/apikey
- Ensure you've initialized the system after pasting the key

### Server won't start (port 5000 in use)
```bash
# Find process using port 5000
lsof -i :5000

# Kill the process
kill -9 <PID>

# Or change the port in athleteedge_final.py (last line):
app.run(debug=True, port=5001)
```

### Slow AI responses
- Gemini API latency varies (1-5 seconds typical)
- Check your internet connection
- Consider caching common queries for production use

## 📚 Technology Stack

- **Backend:** Python Flask, Flask-CORS
- **AI:** Google Generative AI SDK (Gemini)
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Data:** In-memory Python data structures
- **Authentication:** Flask sessions

## 🎓 Academic Context

This system was developed for a multi-agent AI systems course at Georgia State University. It demonstrates:
- Multi-agent architecture design
- Role-based access control
- AI safety and privacy considerations
- Evidence-based response generation
- Real-world problem-solving with AI

## 📧 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review `AthleteEdge_Final_Report.docx` for detailed documentation
3. Examine `evaluation_test_cases.json` for expected behavior examples

## 📄 License

This is an academic project developed for educational purposes at Georgia State University.

## 🙏 Acknowledgments

- Georgia State Athletics for domain expertise
- Google Gemini API for AI generation
- Sports medicine research (AJSM, JOSPT, BJSM) for evidence-based protocols
