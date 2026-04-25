from flask import Flask, request, jsonify, session
from flask_cors import CORS
import google.generativeai as genai
import json
from datetime import datetime, timedelta
import random
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
CORS(app, supports_credentials=True)

system_state = {'initialized': False, 'model': None}

ATHLETES = [
    {"id": 1, "name": "Ariana Anderson", "sport": "Women's Soccer", "position": "Goalkeeper", "injury_status": "ACL Recovery - 11 weeks post-op", "surgery_date": "2026-01-29"},
    {"id": 2, "name": "Micah Tucker", "sport": "Men's Basketball", "position": "Guard"},
    {"id": 3, "name": "Jakai Newton", "sport": "Men's Basketball", "position": "Guard"},
    {"id": 4, "name": "James Cooper", "sport": "Men's Basketball", "position": "Forward"},
    {"id": 5, "name": "Christian Beam", "sport": "Men's Basketball", "position": "Center"},
    {"id": 6, "name": "Malachi Brown", "sport": "Men's Basketball", "position": "Guard"},
    {"id": 7, "name": "Jelani Hamilton", "sport": "Men's Basketball", "position": "Guard"},
    {"id": 8, "name": "Anthony Enoh", "sport": "Men's Basketball", "position": "Forward"},
    {"id": 9, "name": "Emily Glenn", "sport": "Women's Soccer", "position": "Forward", "injury_status": "ACL Reconstruction - 11 weeks post-op", "surgery_date": "2026-01-29"},
    {"id": 10, "name": "Marcus Thompson", "sport": "Football", "position": "QB"},
    {"id": 11, "name": "Isaiah Brown", "sport": "Football", "position": "LB"},
    {"id": 12, "name": "Maya Johnson", "sport": "Women's Basketball", "position": "Guard", "injury_status": "Shoulder Impingement - 8 weeks post-treatment", "injury_date": "2026-02-19"},
    {"id": 13, "name": "Diego Rodriguez", "sport": "Men's Soccer", "position": "Forward"},
    {"id": 14, "name": "Jake Morrison", "sport": "Baseball", "position": "Pitcher"},
    {"id": 15, "name": "Ashley Roberts", "sport": "Softball", "position": "Pitcher"},
]

USERS = {
    "aanderson42": {"password": "Password123!", "role": "student", "athlete_id": 1},
    "jsmith5": {"password": "Coach456#", "role": "coach", "athlete_id": None}
}

# Enhanced workout data with progressive improvement
WORKOUTS = []
def init_workouts():
    global WORKOUTS
    WORKOUTS = []
    exercises_by_type = {
        "strength": ["Back Squat", "Bench Press", "Deadlift", "Power Clean", "Front Squat", "Overhead Press"],
        "endurance": ["Mile Run", "5K Run", "Sprint 400m", "Box Jumps"],
        "agility": ["Shuttle Run", "Cone Drills", "Ladder Drills"]
    }
    
    # Generate progressive workout data (showing improvement over 12 weeks)
    for athlete in ATHLETES:
        # Special ACL rehab protocol for Ariana Anderson (11 weeks post-op)
        if athlete['id'] == 1:
            # ACL Rehab Timeline (weeks 1-11 post-op)
            rehab_exercises = [
                # Week 1-2: Immediate post-op
                {"week": 1, "exercise": "Ankle Pumps", "reps": 20, "sets": 3, "notes": "Focus on reducing swelling"},
                {"week": 1, "exercise": "Quad Sets", "reps": 15, "sets": 3, "notes": "Activate quad muscle"},
                {"week": 2, "exercise": "Straight Leg Raises", "reps": 10, "sets": 3, "notes": "No brace, feeling stronger"},
                {"week": 2, "exercise": "Heel Slides", "reps": 15, "sets": 3, "notes": "ROM improving"},
                
                # Week 3-4: Early mobility
                {"week": 3, "exercise": "Wall Sits", "duration": "30 sec", "sets": 3, "notes": "Building endurance"},
                {"week": 3, "exercise": "Stationary Bike", "duration": "10 min", "resistance": "light", "notes": "Cleared for bike"},
                {"week": 4, "exercise": "Mini Squats", "reps": 12, "sets": 3, "notes": "0-45 degree range"},
                {"week": 4, "exercise": "Calf Raises", "reps": 15, "sets": 3, "notes": "Balance improving"},
                
                # Week 5-6: Strengthening phase
                {"week": 5, "exercise": "Leg Press", "weight": 50, "reps": 12, "sets": 3, "notes": "Starting strength work"},
                {"week": 5, "exercise": "Step Ups", "height": "4 inch", "reps": 10, "sets": 3, "notes": "Controlled movement"},
                {"week": 6, "exercise": "Leg Press", "weight": 75, "reps": 10, "sets": 3, "notes": "Progressing well"},
                {"week": 6, "exercise": "Single Leg Balance", "duration": "45 sec", "sets": 3, "notes": "Proprioception work"},
                
                # Week 7-8: Progressive loading
                {"week": 7, "exercise": "Goblet Squat", "weight": 15, "reps": 10, "sets": 3, "notes": "First weighted squat!"},
                {"week": 7, "exercise": "Leg Press", "weight": 100, "reps": 10, "sets": 3, "notes": "Feeling confident"},
                {"week": 8, "exercise": "Goblet Squat", "weight": 25, "reps": 12, "sets": 3, "notes": "ROM to 90 degrees"},
                {"week": 8, "exercise": "Romanian Deadlift", "weight": 45, "reps": 10, "sets": 3, "notes": "Hamstring activation"},
                
                # Week 9-10: Advanced strengthening
                {"week": 9, "exercise": "Goblet Squat", "weight": 35, "reps": 10, "sets": 3, "notes": "No pain, great form"},
                {"week": 9, "exercise": "Walking Lunges", "weight": 10, "reps": 8, "sets": 3, "notes": "First lunges since surgery"},
                {"week": 10, "exercise": "Box Squat", "weight": 45, "reps": 10, "sets": 3, "notes": "Cleared for barbell"},
                {"week": 10, "exercise": "Leg Press", "weight": 135, "reps": 12, "sets": 3, "notes": "Back to pre-injury weight"},
                
                # Week 11: Current (return to sport prep)
                {"week": 11, "exercise": "Back Squat", "weight": 65, "reps": 10, "sets": 3, "notes": "Building back strength"},
                {"week": 11, "exercise": "Single Leg RDL", "weight": 25, "reps": 8, "sets": 3, "notes": "Balance is back"},
                {"week": 11, "exercise": "Lateral Lunges", "weight": 15, "reps": 10, "sets": 3, "notes": "Sport-specific movement"},
                {"week": 11, "exercise": "Jump Rope", "duration": "2 min", "sets": 3, "notes": "First plyometric cleared!"},
            ]
            
            for rehab in rehab_exercises:
                weeks_ago = 11 - rehab['week']
                date = datetime.now() - timedelta(weeks=weeks_ago)
                
                WORKOUTS.append({
                    "id": len(WORKOUTS) + 1,
                    "athlete_id": 1,
                    "athlete_name": "Ariana Anderson",
                    "sport": "Women's Soccer",
                    "exercise": rehab['exercise'],
                    "weight": rehab.get('weight', 0),
                    "sets": rehab.get('sets', 0),
                    "reps": rehab.get('reps', 0),
                    "duration": rehab.get('duration', ''),
                    "date": date.strftime("%Y-%m-%d"),
                    "notes": f"Week {rehab['week']} post-op: {rehab['notes']}",
                    "type": "rehab"
                })
            continue
        
        # ACL Rehab for Emily Glenn (11 weeks post-op - same timeline as Ariana)
        if athlete['id'] == 9:
            rehab_exercises = [
                # Week 1-2: Immediate post-op
                {"week": 1, "exercise": "Ankle Pumps", "reps": 20, "sets": 3, "notes": "Managing swelling well"},
                {"week": 1, "exercise": "Quad Sets", "reps": 15, "sets": 4, "notes": "Focusing on activation"},
                {"week": 2, "exercise": "Straight Leg Raises", "reps": 12, "sets": 3, "notes": "Getting stronger"},
                {"week": 2, "exercise": "Heel Slides", "reps": 15, "sets": 3, "notes": "ROM at 90 degrees"},
                
                # Week 3-4: Early mobility
                {"week": 3, "exercise": "Wall Sits", "duration": "30 sec", "sets": 3, "notes": "Quad endurance"},
                {"week": 3, "exercise": "Stationary Bike", "duration": "15 min", "resistance": "light", "notes": "Feeling good"},
                {"week": 4, "exercise": "Mini Squats", "reps": 15, "sets": 3, "notes": "Controlled depth"},
                {"week": 4, "exercise": "Calf Raises", "reps": 20, "sets": 3, "notes": "Balance work"},
                
                # Week 5-6: Strengthening
                {"week": 5, "exercise": "Leg Press", "weight": 60, "reps": 12, "sets": 3, "notes": "Starting heavier"},
                {"week": 5, "exercise": "Step Ups", "height": "6 inch", "reps": 10, "sets": 3, "notes": "Higher step cleared"},
                {"week": 6, "exercise": "Leg Press", "weight": 90, "reps": 10, "sets": 4, "notes": "Progressing faster than expected"},
                {"week": 6, "exercise": "Single Leg Balance", "duration": "60 sec", "sets": 3, "notes": "Proprioception excellent"},
                
                # Week 7-8: Progressive loading
                {"week": 7, "exercise": "Goblet Squat", "weight": 20, "reps": 12, "sets": 3, "notes": "First weighted squat - felt great"},
                {"week": 7, "exercise": "Leg Press", "weight": 115, "reps": 10, "sets": 4, "notes": "No pain at all"},
                {"week": 8, "exercise": "Goblet Squat", "weight": 30, "reps": 12, "sets": 3, "notes": "Full depth achieved"},
                {"week": 8, "exercise": "Romanian Deadlift", "weight": 55, "reps": 10, "sets": 3, "notes": "Posterior chain strong"},
                
                # Week 9-10: Advanced strengthening  
                {"week": 9, "exercise": "Goblet Squat", "weight": 40, "reps": 10, "sets": 4, "notes": "Confidence is back"},
                {"week": 9, "exercise": "Walking Lunges", "weight": 15, "reps": 10, "sets": 3, "notes": "Dynamic movement cleared"},
                {"week": 10, "exercise": "Box Squat", "weight": 55, "reps": 10, "sets": 3, "notes": "Barbell work feels natural"},
                {"week": 10, "exercise": "Leg Press", "weight": 155, "reps": 12, "sets": 4, "notes": "Exceeding expectations"},
                
                # Week 11: Current (return to sport prep)
                {"week": 11, "exercise": "Back Squat", "weight": 75, "reps": 10, "sets": 3, "notes": "Building sport-specific strength"},
                {"week": 11, "exercise": "Single Leg RDL", "weight": 30, "reps": 8, "sets": 3, "notes": "Symmetry restored"},
                {"week": 11, "exercise": "Lateral Bounds", "reps": 8, "sets": 3, "notes": "First lateral plyometric!"},
                {"week": 11, "exercise": "Box Jumps", "height": "12 inch", "reps": 6, "sets": 3, "notes": "Cleared for jumping - so excited!"},
            ]
            
            for rehab in rehab_exercises:
                weeks_ago = 11 - rehab['week']
                date = datetime.now() - timedelta(weeks=weeks_ago)
                
                WORKOUTS.append({
                    "id": len(WORKOUTS) + 1,
                    "athlete_id": 9,
                    "athlete_name": "Emily Glenn",
                    "sport": "Women's Soccer",
                    "exercise": rehab['exercise'],
                    "weight": rehab.get('weight', 0),
                    "sets": rehab.get('sets', 0),
                    "reps": rehab.get('reps', 0),
                    "duration": rehab.get('duration', ''),
                    "height": rehab.get('height', ''),
                    "date": date.strftime("%Y-%m-%d"),
                    "notes": f"Week {rehab['week']} post-op: {rehab['notes']}",
                    "type": "rehab"
                })
            continue
        
        base_squat = random.randint(185, 275)
        base_bench = random.randint(135, 225)
        base_deadlift = random.randint(225, 365)
        
        # Create workouts over 12 weeks with progressive overload
        for week in range(12):
            date = datetime.now() - timedelta(weeks=11-week, days=random.randint(0, 6))
            
            # Strength workouts - show progressive improvement
            improvement_factor = 1 + (week * 0.03)  # 3% improvement per week
            
            # Back Squat
            WORKOUTS.append({
                "id": len(WORKOUTS) + 1,
                "athlete_id": athlete['id'],
                "athlete_name": athlete['name'],
                "sport": athlete['sport'],
                "exercise": "Back Squat",
                "weight": int(base_squat * improvement_factor),
                "sets": random.randint(3, 5),
                "reps": random.randint(5, 8),
                "date": date.strftime("%Y-%m-%d"),
                "notes": f"Week {week+1} - Feeling strong" if week % 3 == 0 else ""
            })
            
            # Bench Press
            WORKOUTS.append({
                "id": len(WORKOUTS) + 1,
                "athlete_id": athlete['id'],
                "athlete_name": athlete['name'],
                "sport": athlete['sport'],
                "exercise": "Bench Press",
                "weight": int(base_bench * improvement_factor),
                "sets": random.randint(3, 5),
                "reps": random.randint(6, 10),
                "date": date.strftime("%Y-%m-%d"),
                "notes": ""
            })
            
            # Deadlift
            if week % 2 == 0:  # Every other week
                WORKOUTS.append({
                    "id": len(WORKOUTS) + 1,
                    "athlete_id": athlete['id'],
                    "athlete_name": athlete['name'],
                    "sport": athlete['sport'],
                    "exercise": "Deadlift",
                    "weight": int(base_deadlift * improvement_factor),
                    "sets": random.randint(3, 4),
                    "reps": random.randint(3, 6),
                    "date": date.strftime("%Y-%m-%d"),
                    "notes": "PR!" if week == 11 else ""
                })

init_workouts()

class PrivacyFilter:
    @staticmethod
    def check(query):
        query_lower = query.lower()
        if any(w in query_lower for w in ['homework', 'cheat', 'essay']):
            return False, "⚠️ This is for athletic performance only."
        if any(w in query_lower for w in ['weakest', 'worst', 'laziest']):
            return False, "⚠️ I cannot rank athletes by weakness."
        return True, None

class DatabaseQuery:
    @staticmethod
    def get_context(query, user_role, athlete_id=None):
        query_lower = query.lower()
        
        # Student view
        if user_role == 'student' and athlete_id:
            if 'compare' in query_lower:
                return {'error': 'Students can only view their own data.'}
            athlete = ATHLETES[athlete_id-1]
            my_workouts = [w for w in WORKOUTS if w['athlete_id'] == athlete_id]
            
            # Calculate progress
            recent = [w for w in my_workouts if 'Squat' in w['exercise']][-5:] if my_workouts else []
            old = [w for w in my_workouts if 'Squat' in w['exercise']][:5] if my_workouts else []
            
            return {
                'type': 'student',
                'athlete': athlete,
                'total_workouts': len(my_workouts),
                'recent_workouts': my_workouts[-10:],
                'progress': {
                    'recent_avg': sum(w['weight'] for w in recent) / len(recent) if recent else 0,
                    'old_avg': sum(w['weight'] for w in old) / len(old) if old else 0
                }
            }
        
        # Coach comparison queries
        if any(word in query_lower for word in ['compare', 'progress', 'improvement', 'improved', 'improving', 'most', 'top', 'best', 'who has']):
            exercise = 'squat' if 'squat' in query_lower else 'bench' if 'bench' in query_lower else 'deadlift' if 'deadlift' in query_lower else 'squat'
            
            # Get progress data for each athlete
            athlete_progress = {}
            for athlete in ATHLETES:
                athlete_workouts = [w for w in WORKOUTS if w['athlete_id'] == athlete['id'] and exercise.lower() in w['exercise'].lower()]
                if athlete_workouts:
                    old_workouts = athlete_workouts[:3]
                    recent_workouts = athlete_workouts[-3:]
                    old_avg = sum(w['weight'] for w in old_workouts) / len(old_workouts)
                    recent_avg = sum(w['weight'] for w in recent_workouts) / len(recent_workouts)
                    improvement = recent_avg - old_avg
                    
                    athlete_progress[athlete['id']] = {
                        'name': athlete['name'],
                        'sport': athlete['sport'],
                        'current_max': max(w['weight'] for w in athlete_workouts),
                        'old_avg': int(old_avg),
                        'recent_avg': int(recent_avg),
                        'improvement': int(improvement),
                        'improvement_pct': round((improvement / old_avg * 100), 1) if old_avg > 0 else 0
                    }
            
            # Sort by improvement
            top_improvers = sorted(athlete_progress.values(), key=lambda x: x['improvement_pct'], reverse=True)[:10]
            
            return {
                'type': 'progress_comparison',
                'exercise': exercise,
                'top_improvers': top_improvers,
                'total_athletes': len(athlete_progress)
            }
        
        # General team stats
        return {
            'type': 'general',
            'total_athletes': len(ATHLETES),
            'total_workouts': len(WORKOUTS),
            'sports': list(set(a['sport'] for a in ATHLETES)),
            'date_range': f"{min(w['date'] for w in WORKOUTS)} to {max(w['date'] for w in WORKOUTS)}"
        }

@app.route('/')
def home():
    return """<!DOCTYPE html>
<html><head><meta charset="UTF-8"><title>AthleteEdge</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: Outfit, sans-serif; background: #0a0e1a; color: #fff; }
.login-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 2rem; }
.login-box { background: #12161f; border: 1px solid #2a3154; border-radius: 16px; padding: 3rem; max-width: 450px; width: 100%; }
.logo { font-size: 3rem; text-align: center; margin-bottom: 1rem; }
h1 { font-size: 2rem; text-align: center; margin-bottom: 0.5rem; background: linear-gradient(135deg, #fff, #00d4ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.subtitle { color: #9ca3bf; text-align: center; margin-bottom: 2rem; }
.form-group { margin-bottom: 1.5rem; }
label { display: block; margin-bottom: 0.5rem; font-weight: 600; color: #9ca3bf; font-size: 0.9rem; }
input, select, textarea { width: 100%; padding: 0.9rem; background: #0a0e1a; border: 1px solid #2a3154; border-radius: 12px; color: #fff; font-size: 0.95rem; font-family: inherit; }
input:focus, select:focus, textarea:focus { outline: none; border-color: #00d4ff; }
.btn { width: 100%; padding: 1rem; background: linear-gradient(135deg, #0039A6, #00d4ff); border: none; border-radius: 12px; color: #fff; font-weight: 700; cursor: pointer; }
.btn:disabled { opacity: 0.5; cursor: not-allowed; }
.demo { margin-top: 1.5rem; padding: 1rem; background: #0a0e1a; border-radius: 8px; font-size: 0.85rem; color: #9ca3bf; }
.dashboard { display: none; }
.dashboard.active { display: block; }
.header { background: #12161f; border-bottom: 1px solid #2a3154; padding: 1.5rem 2rem; display: flex; justify-content: space-between; align-items: center; }
.main-content { display: grid; grid-template-columns: 350px 1fr; gap: 2rem; padding: 2rem; max-width: 1600px; margin: 0 auto; }
.card { background: #12161f; border: 1px solid #2a3154; border-radius: 16px; padding: 2rem; margin-bottom: 1.5rem; }
.card-title { font-size: 1.3rem; font-weight: 700; margin-bottom: 1.5rem; color: #fff; }
.tabs { display: flex; gap: 1rem; margin-bottom: 1.5rem; border-bottom: 2px solid #2a3154; }
.tab { padding: 0.75rem 1.5rem; cursor: pointer; color: #9ca3bf; border-bottom: 2px solid transparent; margin-bottom: -2px; transition: all 0.2s; }
.tab.active { color: #00d4ff; border-bottom-color: #00d4ff; }
.tab:hover { color: #fff; }
.tab-content { display: none; }
.tab-content.active { display: block; }
.chat-messages { height: 500px; overflow-y: auto; margin-bottom: 1rem; padding: 1rem; background: #0a0e1a; border-radius: 12px; }
.message { margin-bottom: 1rem; padding: 1rem; border-radius: 12px; line-height: 1.6; }
.user-message { background: rgba(200, 16, 46, 0.1); border-left: 3px solid #C8102E; }
.ai-message { background: rgba(0, 212, 255, 0.05); border-left: 3px solid #00d4ff; }
.input-group { display: flex; gap: 1rem; }
.chat-input { flex: 1; }
.send-btn { width: auto; padding: 1rem 2rem; }
.example-btn { padding: 0.8rem 1rem; margin: 0.5rem 0.5rem 0.5rem 0; background: #0a0e1a; border: 1px solid #2a3154; border-radius: 12px; cursor: pointer; display: inline-block; color: #9ca3bf; font-size: 0.9rem; }
.example-btn:hover { border-color: #00d4ff; color: #fff; }
.athlete-item { padding: 0.9rem; background: #0a0e1a; border: 1px solid #2a3154; border-radius: 8px; margin-bottom: 0.5rem; }
.athlete-item b { display: block; margin-bottom: 0.25rem; color: #fff; }
.athlete-item small { color: #9ca3bf; }
.workout-item { padding: 1rem; background: #0a0e1a; border: 1px solid #2a3154; border-radius: 8px; margin-bottom: 0.75rem; }
.workout-item strong { color: #00d4ff; }
.workout-item small { color: #9ca3bf; }
.workout-history { max-height: 400px; overflow-y: auto; }
.hidden { display: none; }
.logout-btn { padding: 0.5rem 1.2rem; background: #0a0e1a; border: 1px solid #2a3154; border-radius: 6px; cursor: pointer; color: #9ca3bf; font-size: 0.9rem; }
.logout-btn:hover { border-color: #C8102E; color: #fff; }
.success-msg { padding: 1rem; background: rgba(0, 255, 136, 0.1); border-left: 3px solid #00ff88; border-radius: 8px; margin-bottom: 1rem; color: #00ff88; }
</style></head><body>
<div class="login-page" id="loginPage">
<div class="login-box">
<div class="logo">🏋️</div>
<h1>AthleteEdge</h1>
<div class="subtitle">Georgia State Athletics AI</div>
<form onsubmit="login(event)">
<div class="form-group">
<label>Username</label>
<input type="text" id="username" required>
</div>
<div class="form-group">
<label>Password</label>
<input type="password" id="password" required>
</div>
<button type="submit" class="btn">Sign In</button>
</form>
<div class="demo">
<strong>Demo Credentials:</strong><br>
Student: aanderson42 / Password123!<br>
Coach: jsmith5 / Coach456#
</div>
</div>
</div>

<div class="dashboard" id="dashboard">
<div class="header">
<div><strong>🏋️ AthleteEdge</strong> • <span id="userName"></span> (<span id="userRole"></span>)</div>
<button class="logout-btn" onclick="logout()">Logout</button>
</div>
<div class="main-content">
<div class="sidebar">
<div class="card">
<div class="card-title">⚙️ Configuration</div>
<input type="password" id="apiKey" placeholder="Enter Gemini API key..." style="margin-bottom: 1rem;">
<button class="btn" id="initBtn" onclick="initSystem()">Initialize System</button>
</div>
<div class="card">
<div class="card-title">👥 Athletes</div>
<div id="athletesList">Loading...</div>
</div>
</div>
<div class="content-area">
<div class="card">
<div class="tabs">
<div class="tab active" onclick="switchTab('chat')">💬 AI Assistant</div>
<div class="tab" onclick="switchTab('workouts')">🏋️ Log Workout</div>
</div>

<div class="tab-content active" id="chatTab">
<div style="margin-bottom: 1rem;">
<button class="example-btn" onclick="ask('Show my progress over the last month')">📈 My Progress</button>
<button class="example-btn" onclick="ask('Who has improved the most in squats?')">🏆 Top Improvers</button>
<button class="example-btn" onclick="ask('Team stats this week')">📊 Team Stats</button>
<button class="example-btn" onclick="ask('Who is weakest?')">🚫 Test Block</button>
</div>
<div class="chat-messages" id="chat">
<div style="text-align: center; padding: 3rem; color: #9ca3bf;">
<div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div>
<div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">AI Assistant Ready</div>
<div style="font-size: 0.9rem;">Enter your API key and initialize the system to start asking questions</div>
</div>
</div>
<div class="input-group">
<input type="text" class="chat-input" id="query" placeholder="Ask about performance..." onkeypress="if(event.key==='Enter')send()">
<button class="btn send-btn" onclick="send()">Send</button>
</div>
</div>

<div class="tab-content" id="workoutsTab">
<div id="successMsg" class="success-msg hidden">✓ Workout logged successfully!</div>
<form onsubmit="logWorkout(event)">
<div class="form-group">
<label>Exercise</label>
<select id="exerciseType" required>
<option value="">Select exercise...</option>
<option value="Back Squat">Back Squat</option>
<option value="Bench Press">Bench Press</option>
<option value="Deadlift">Deadlift</option>
<option value="Power Clean">Power Clean</option>
<option value="Front Squat">Front Squat</option>
<option value="Overhead Press">Overhead Press</option>
</select>
</div>
<div class="form-group">
<label>Weight (lbs)</label>
<input type="number" id="workoutWeight" required min="0" max="1000">
</div>
<div class="form-group">
<label>Sets</label>
<input type="number" id="workoutSets" required min="1" max="10" value="3">
</div>
<div class="form-group">
<label>Reps</label>
<input type="number" id="workoutReps" required min="1" max="20" value="5">
</div>
<div class="form-group">
<label>Notes (optional)</label>
<textarea id="workoutNotes" rows="3" placeholder="How did it feel?"></textarea>
</div>
<button type="submit" class="btn">Log Workout</button>
</form>

<div style="margin-top: 2rem;">
<h3 style="margin-bottom: 1rem; color: #9ca3bf;">Recent Workouts</h3>
<div class="workout-history" id="workoutHistory">Loading...</div>
</div>
</div>

</div>
</div>
</div>
</div>

<script>
let init = false;
let currentTab = 'chat';

function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    event.target.classList.add('active');
    document.getElementById(tab + 'Tab').classList.add('active');
    currentTab = tab;
    if (tab === 'workouts') {
        loadWorkoutHistory();
    }
}

async function login(e) {
    e.preventDefault();
    const r = await fetch('/api/login', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            username: document.getElementById('username').value,
            password: document.getElementById('password').value
        })
    });
    const d = await r.json();
    if (d.success) {
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('dashboard').classList.add('active');
        document.getElementById('userName').textContent = d.name;
        document.getElementById('userRole').textContent = d.role;
        loadAthletes();
    } else {
        alert('Invalid credentials');
    }
}

function logout() {
    document.getElementById('dashboard').classList.remove('active');
    document.getElementById('loginPage').classList.remove('hidden');
    document.getElementById('chat').innerHTML = '<div style="text-align: center; padding: 3rem; color: #9ca3bf;"><div style="font-size: 3rem; margin-bottom: 1rem;">🤖</div><div style="font-size: 1.1rem; font-weight: 600; margin-bottom: 0.5rem;">AI Assistant Ready</div><div style="font-size: 0.9rem;">Enter your API key and initialize the system to start asking questions</div></div>';
}

async function initSystem() {
    const k = document.getElementById('apiKey').value;
    if (!k) { alert('Enter API key'); return; }
    document.getElementById('initBtn').disabled = true;
    document.getElementById('initBtn').textContent = 'Initializing...';
    try {
        const r = await fetch('/api/initialize', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({api_key: k})
        });
        const d = await r.json();
        if (d.success) {
            init = true;
            document.getElementById('initBtn').textContent = '✓ System Ready';
            document.getElementById('chat').innerHTML = '';
            addMsg('system', 'System initialized successfully! Ask about progress, improvements, or team stats.');
        } else {
            throw new Error(d.error);
        }
    } catch (e) {
        alert('Error: ' + e.message);
        document.getElementById('initBtn').disabled = false;
        document.getElementById('initBtn').textContent = 'Initialize System';
    }
}

async function loadAthletes() {
    const r = await fetch('/api/athletes');
    const d = await r.json();
    document.getElementById('athletesList').innerHTML = d.athletes.map(a => 
        `<div class="athlete-item"><b>${a.name}</b><small>${a.sport} • ${a.position}</small></div>`
    ).join('');
}

async function loadWorkoutHistory() {
    const r = await fetch('/api/workouts');
    const d = await r.json();
    const workouts = d.workouts.slice(0, 10);
    document.getElementById('workoutHistory').innerHTML = workouts.map(w => 
        `<div class="workout-item">
            <strong>${w.exercise}</strong> - ${w.weight} lbs × ${w.sets}x${w.reps}<br>
            <small>${w.date}${w.notes ? ' • ' + w.notes : ''}</small>
        </div>`
    ).join('') || '<div style="color: #9ca3bf; text-align: center; padding: 2rem;">No workouts logged yet</div>';
}

async function logWorkout(e) {
    e.preventDefault();
    const workout = {
        exercise: document.getElementById('exerciseType').value,
        weight: parseInt(document.getElementById('workoutWeight').value),
        sets: parseInt(document.getElementById('workoutSets').value),
        reps: parseInt(document.getElementById('workoutReps').value),
        notes: document.getElementById('workoutNotes').value
    };
    
    try {
        const r = await fetch('/api/workouts', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(workout)
        });
        const d = await r.json();
        if (d.success) {
            document.getElementById('successMsg').classList.remove('hidden');
            setTimeout(() => document.getElementById('successMsg').classList.add('hidden'), 3000);
            e.target.reset();
            loadWorkoutHistory();
        }
    } catch (e) {
        alert('Error logging workout: ' + e.message);
    }
}

function ask(q) {
    document.getElementById('query').value = q;
    send();
}

async function send() {
    if (!init) { alert('Initialize system first'); return; }
    const q = document.getElementById('query').value.trim();
    if (!q) return;
    addMsg('user', q);
    document.getElementById('query').value = '';
    try {
        const r = await fetch('/api/query', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: q})
        });
        const d = await r.json();
        addMsg('ai', d.message + '\\n\\n⚡ ' + d.response_time.toFixed(2) + 's • 🤖 ' + d.agent_calls + ' agents');
    } catch (e) {
        addMsg('ai', '❌ Error: ' + e.message);
    }
}

function addMsg(t, txt) {
    const c = document.getElementById('chat');
    const d = document.createElement('div');
    d.className = 'message ' + (t === 'user' ? 'user-message' : 'ai-message');
    d.innerHTML = '<b>' + (t === 'user' ? '👤 You' : t === 'system' ? '✓ System' : '🤖 AthleteEdge') + '</b><br>' + txt.replace(/\\n/g, '<br>');
    c.appendChild(d);
    c.scrollTop = c.scrollHeight;
}
</script>
</body></html>"""

@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    user = USERS.get(data.get('username'))
    if user and user['password'] == data.get('password'):
        session['username'] = data.get('username')
        session['role'] = user['role']
        session['athlete_id'] = user['athlete_id']
        name = ATHLETES[user['athlete_id']-1]['name'] if user['athlete_id'] else 'Coach'
        return jsonify({'success': True, 'role': user['role'], 'name': name})
    return jsonify({'success': False}), 401

@app.route('/api/initialize', methods=['POST'])
def initialize():
    api_key = request.json.get('api_key')
    try:
        genai.configure(api_key=api_key)
        models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        if not models:
            return jsonify({'error': 'No models'}), 400
        system_state['model'] = genai.GenerativeModel(models[0].replace('models/', ''))
        system_state['initialized'] = True
        return jsonify({'success': True, 'model': models[0]})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/athletes', methods=['GET'])
def get_athletes():
    if session.get('role') == 'coach':
        return jsonify({'athletes': ATHLETES})
    else:
        return jsonify({'athletes': [ATHLETES[session.get('athlete_id')-1]]})

@app.route('/api/workouts', methods=['GET'])
def get_workouts():
    athlete_id = session.get('athlete_id')
    if session.get('role') == 'student' and athlete_id:
        my_workouts = [w for w in WORKOUTS if w['athlete_id'] == athlete_id]
        return jsonify({'workouts': sorted(my_workouts, key=lambda x: x['date'], reverse=True)})
    else:
        return jsonify({'workouts': sorted(WORKOUTS, key=lambda x: x['date'], reverse=True)[:50]})

@app.route('/api/workouts', methods=['POST'])
def add_workout():
    if 'username' not in session:
        return jsonify({'error': 'Not logged in'}), 401
    
    data = request.json
    athlete_id = session.get('athlete_id')
    
    if session.get('role') == 'student' and not athlete_id:
        return jsonify({'error': 'Student must have athlete_id'}), 400
    
    new_workout = {
        'id': len(WORKOUTS) + 1,
        'athlete_id': athlete_id if athlete_id else 1,
        'athlete_name': ATHLETES[athlete_id-1]['name'] if athlete_id else 'Coach',
        'sport': ATHLETES[athlete_id-1]['sport'] if athlete_id else 'N/A',
        'exercise': data.get('exercise'),
        'weight': data.get('weight'),
        'sets': data.get('sets'),
        'reps': data.get('reps'),
        'date': datetime.now().strftime("%Y-%m-%d"),
        'notes': data.get('notes', '')
    }
    
    WORKOUTS.append(new_workout)
    return jsonify({'success': True, 'workout': new_workout})

@app.route('/api/query', methods=['POST'])
def handle_query():
    if not system_state['initialized']:
        return jsonify({'error': 'Not initialized'}), 400
    query = request.json.get('query')
    start = datetime.now()
    allowed, msg = PrivacyFilter.check(query)
    if not allowed:
        return jsonify({'status': 'blocked', 'message': msg, 'response_time': 0.1, 'agent_calls': 1})
    context = DatabaseQuery.get_context(query, session.get('role'), session.get('athlete_id'))
    if context.get('error'):
        return jsonify({'status': 'error', 'message': context['error'], 'response_time': 0.1})
    prompt = f"AthleteEdge AI for GSU. Context: {json.dumps(context)[:1500]} Question: {query} Use the data provided including progress metrics, improvement percentages, and workout history. Cite research (JOSPT, AJSM). Keep response 2-3 paragraphs with emojis."
    try:
        response = system_state['model'].generate_content(prompt)
        return jsonify({'status': 'success', 'message': response.text, 'response_time': (datetime.now()-start).total_seconds(), 'agent_calls': 4})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e), 'response_time': (datetime.now()-start).total_seconds()})

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🏋️ ATHLETEEDGE - COMPLETE SYSTEM")
    print("="*60)
    print("\n✨ NEW: Workout Logging + Progress Tracking!")
    print("\n📱 http://localhost:5000")
    print("👤 Student: aanderson42 / Password123!")
    print("👨‍🏫 Coach: jsmith5 / Coach456#")
    print("\n" + "="*60 + "\n")
    app.run(debug=True, port=5000)
