from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import datetime
import wikipedia
import os
import webbrowser
import random

app = Flask(__name__)
CORS(app)

# Global memory variables for multi-turn conversations
last_trace = "No actions taken yet."
awaiting_meeting_details = False
meeting_step = 0
meeting_data = {}
awaiting_clarification = False
pending_intent = ""
awaiting_tasks = False

# ==========================================
# 3. ACT: The Action Functions (Web Ready)
# ==========================================

def get_time():
    now = datetime.datetime.now()
    return f"The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}"

def save_note(user_input):
    note_content = user_input.replace("note", "").replace("remember", "").replace("save", "").strip()
    with open("my_notes.txt", "a") as file:
        file.write(note_content + "\n")
    return f"Got it. I saved '{note_content}' to your notes."

def read_notes():
    if os.path.exists("my_notes.txt"):
        with open("my_notes.txt", "r") as file:
            return f"Here are your saved notes:\n\n{file.read()}"
    return "You don't have any saved notes yet."

def calculate(user_input):
    math_equation = ''.join(char for char in user_input if char in '0123456789+-*/().')
    try:
        result = eval(math_equation)
        return f"The answer is {result}"
    except:
        return "Sorry, I couldn't understand the math equation."

def search_info(user_input):
    query = user_input.replace("search", "").replace("who is", "").replace("what is", "").strip()
    try:
        summary = wikipedia.summary(query, sentences=2)
        return f"Looking up '{query}'...\n\n{summary}"
    except:
        return f"Sorry, I couldn't find any clear information on '{query}'."

def open_website(user_input):
    site_name = user_input.replace("open", "").replace("website", "").strip()
    if site_name == "":
        return "Please tell me which website to open, like 'open youtube'."
    
    url = f"https://www.{site_name}.com" if "." not in site_name else f"https://{site_name}"
    webbrowser.open(url)
    return f"Opening {site_name} in your web browser..."

def flip_coin():
    return f"I flipped a coin... It landed on {random.choice(['Heads', 'Tails'])}!"

def roll_die():
    return f"I rolled a die... You got a {random.randint(1, 6)}!"

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "There are 10 types of people in the world: those who understand binary, and those who don't."
    ]
    return random.choice(jokes)

def give_quote():
    quotes = [
        "“The only way to do great work is to love what you do.” – Steve Jobs",
        "“First, solve the problem. Then, write the code.” – John Johnson"
    ]
    return random.choice(quotes)

def forget_data():
    if os.path.exists("my_notes.txt"):
        os.remove("my_notes.txt")
        return "All your stored notes have been securely deleted."
    return "You have no stored data to delete."

def log_unanswered(user_input):
    with open("unanswered_queries.log", "a") as file:
        file.write(f"{datetime.datetime.now()}: {user_input}\n")
    return "I didn't understand that. I've logged this query to improve my future training."

def explain_action():
    global last_trace
    return f"Here is why I did that -> {last_trace}"

# ==========================================
# 2.A KNOWLEDGE & REASONING LAYER
# ==========================================

RULES = [
    (["time", "date", "clock"], "check_time"),
    (["show notes", "read notes", "what are my notes"], "read_notes"),
    (["note", "remember", "save"], "save_note"),
    (["calculate", "math", "+", "-", "*", "/"], "math"),
    (["search", "who is", "what is"], "search"),
    (["open", "website", "www", ".com"], "open_web"),
    (["flip", "coin"], "flip_coin"),
    (["roll", "dice", "die"], "roll_die"),
    (["joke", "funny", "laugh"], "joke"),
    (["quote", "inspire", "wisdom"], "quote"),
    (["forget", "delete data", "erase"], "forget_data"),
    (["plan", "schedule", "my day"], "plan_day"),
    (["why", "explain", "reason"], "explain_xai"),
    (["book", "meeting", "appointment"], "book_meeting")
]

def forward_chaining_inference(user_input):
    text = user_input.lower()
    best_intent = "unknown"
    highest_confidence = 0.0
    trace = "No rules matched."
    
    for conditions, intent in RULES:
        matches = [condition for condition in conditions if condition in text]
        match_count = len(matches)
        
        if match_count > 0:
            confidence = 0.6 if match_count == 1 else 1.0
            if confidence > highest_confidence:
                highest_confidence = confidence
                best_intent = intent
                trace = f"Rule matched: IF {matches} THEN Intent = {intent} (Confidence: {confidence*100}%)"
                
    return best_intent, highest_confidence, trace

# ==========================================
# 2.A.1 CSP LAYER (Constraint Satisfaction)
# ==========================================
class DayPlannerCSP:
    def __init__(self, tasks):
        self.variables = tasks
        self.time_slots = [9, 10, 11, 12, 13, 14, 15, 16, 17] 
        self.domains = {task: self.time_slots[:] for task in tasks}
        
        lunch_task = next((t for t in tasks if t.lower() == "lunch"), None)
        if lunch_task:
            self.domains[lunch_task] = [t for t in self.domains[lunch_task] if t in [12, 13]]

    def is_consistent(self, task, time, assignment):
        if time in assignment.values():
            return False
        return True

    def solve_forward_checking(self, assignment, domains):
        if len(assignment) == len(self.variables):
            return assignment
        
        unassigned = [v for v in self.variables if v not in assignment][0]
        for value in domains[unassigned]:
            if self.is_consistent(unassigned, value, assignment):
                assignment[unassigned] = value
                
                local_domains = {k: v[:] for k, v in domains.items()}
                possible = True
                for other in self.variables:
                    if other not in assignment:
                        if value in local_domains[other]:
                            local_domains[other].remove(value)
                        if not local_domains[other]:
                            possible = False
                            break
                
                if possible:
                    result = self.solve_forward_checking(assignment, local_domains)
                    if result:
                        return result
                del assignment[unassigned]
        return None

# ==========================================
# 2.B DECIDE: The Web Intent Router
# ==========================================

def decide_and_act(user_input):
    global last_trace, awaiting_meeting_details, meeting_step, meeting_data
    global awaiting_clarification, pending_intent, awaiting_tasks
    
    # 1. Check if we are waiting for a "yes/no" clarification
    if awaiting_clarification:
        awaiting_clarification = False
        if "y" in user_input.lower():
            intent = pending_intent
        else:
            return "Okay, cancelling action. Please try rephrasing."
            
    # 2. Check if we are in the middle of booking a meeting
    elif awaiting_meeting_details:
        if meeting_step == 1:
            meeting_data['title'] = user_input
            meeting_step = 2
            return "What date is this meeting? (e.g., Tomorrow, Oct 15)"
        elif meeting_step == 2:
            meeting_data['date'] = user_input
            meeting_step = 3
            return "What time will it start? (e.g., 10:00 AM)"
        elif meeting_step == 3:
            meeting_data['time'] = user_input
            awaiting_meeting_details = False
            with open("my_notes.txt", "a") as file:
                file.write(f"MEETING: {meeting_data['title']} on {meeting_data['date']} at {meeting_data['time']}\n")
            return f"Done. Meeting '{meeting_data['title']}' successfully booked for {meeting_data['date']} at {meeting_data['time']}."

    # 3. Check if we are waiting for tasks to schedule (CSP Layer)
    elif awaiting_tasks:
        awaiting_tasks = False
        tasks = [t.strip() for t in user_input.split(",") if t.strip()]
        if len(tasks) > 9:
            return "Error! You have more tasks than available working hours (9 slots). No schedule exists."
        
        csp = DayPlannerCSP(tasks)
        schedule = csp.solve_forward_checking({}, csp.domains)
        
        if schedule:
            result_text = "Here is your conflict-free schedule:\n\n"
            sorted_schedule = sorted(schedule.items(), key=lambda item: item[1])
            for task, time in sorted_schedule:
                am_pm = "AM" if time < 12 else "PM"
                display_time = time if time <= 12 else time - 12
                result_text += f" - {display_time}:00 {am_pm} : {task}\n"
            return result_text
        return "I could not find a valid schedule. Constraints conflict."

    # 4. Normal routing (if we aren't waiting for an answer)
    else:
        intent, confidence, trace = forward_chaining_inference(user_input)
        
        if intent != "explain_xai":
            last_trace = trace
        
        if intent == "unknown":
            return log_unanswered(user_input)
            
        if confidence < 0.7:
            awaiting_clarification = True
            pending_intent = intent
            return f"I am only {confidence*100}% sure. Did you mean to '{intent}'? (yes/no)"

    # 5. Execute the action
    if intent == "check_time": return get_time()
    elif intent == "read_notes": return read_notes()
    elif intent == "save_note": return save_note(user_input)
    elif intent == "math": return calculate(user_input)
    elif intent == "search": return search_info(user_input)
    elif intent == "open_web": return open_website(user_input)
    elif intent == "flip_coin": return flip_coin()
    elif intent == "roll_die": return roll_die()
    elif intent == "joke": return tell_joke()
    elif intent == "quote": return give_quote()
    elif intent == "forget_data": return forget_data()
    elif intent == "explain_xai": return explain_action()
    elif intent == "plan_day": 
        awaiting_tasks = True
        return "Let's plan your day. Please reply with your tasks separated by commas (e.g., 'Meeting, Coding, Lunch, Review')."
    elif intent == "book_meeting":
        awaiting_meeting_details = True
        meeting_step = 1
        meeting_data = {}
        return "Let's book a meeting. What is the title of the meeting? (e.g., Project Sync)"

# ==========================================
# 1. PERCEIVE: Flask API Endpoints
# ==========================================

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")
    
    if not user_message:
        return jsonify({"response": "Empty message received."})
        
    bot_response = decide_and_act(user_message)
    return jsonify({"response": bot_response})

if __name__ == '__main__':
    print("Starting Web Assistant on http://127.0.0.1:5000")
    app.run(debug=True, port=5000)