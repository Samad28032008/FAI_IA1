import datetime
import wikipedia
import os
import webbrowser
import random

# Global variable for Explainable AI (Step 4)
last_trace = "No actions taken yet."

# ==========================================
# 3. ACT: The Action Functions
# ==========================================

def get_time():
    now = datetime.datetime.now()
    print(f"Assistant: The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}")

def save_note(user_input):
    note_content = user_input.replace("note", "").replace("remember", "").replace("save", "").strip()
    with open("my_notes.txt", "a") as file:
        file.write(note_content + "\n")
    print(f"Assistant: Got it. I saved '{note_content}' to your notes.")

def read_notes():
    if os.path.exists("my_notes.txt"):
        print("Assistant: Here are your saved notes:")
        with open("my_notes.txt", "r") as file:
            print(file.read())
    else:
        print("Assistant: You don't have any saved notes yet.")

def calculate(user_input):
    math_equation = ''.join(char for char in user_input if char in '0123456789+-*/().')
    try:
        result = eval(math_equation)
        print(f"Assistant: The answer is {result}")
    except:
        print("Assistant: Sorry, I couldn't understand the math equation.")

def search_info(user_input):
    query = user_input.replace("search", "").replace("who is", "").replace("what is", "").strip()
    print(f"Assistant: Looking up '{query}'...")
    try:
        summary = wikipedia.summary(query, sentences=2)
        print(f"Assistant: {summary}")
    except:
        print("Assistant: Sorry, I couldn't find any clear information on that.")

def open_website(user_input):
    site_name = user_input.replace("open", "").replace("website", "").strip()
    if site_name == "":
        print("Assistant: Please tell me which website to open, like 'open youtube'.")
        return
        
    if "." not in site_name:
        url = f"https://www.{site_name}.com"
    else:
        url = f"https://{site_name}"
        
    print(f"Assistant: Opening {site_name} in your web browser...")
    webbrowser.open(url)

def flip_coin():
    outcome = random.choice(["Heads", "Tails"])
    print(f"Assistant: I flipped a coin... It landed on {outcome}!")

def roll_die():
    outcome = random.randint(1, 6)
    print(f"Assistant: I rolled a die... You got a {outcome}!")

def tell_joke():
    jokes = [
        "Why do programmers prefer dark mode? Because light attracts bugs!",
        "There are 10 types of people in the world: those who understand binary, and those who don't.",
        "Why did the Python programmer not respond? Because he was stuck in a while loop!",
        "I told my computer I needed a break... now it won't stop sending me KitKat ads."
    ]
    print(f"Assistant: {random.choice(jokes)}")

def give_quote():
    quotes = [
        "“The only way to do great work is to love what you do.” – Steve Jobs",
        "“It does not matter how slowly you go as long as you do not stop.” – Confucius",
        "“Code is like humor. When you have to explain it, it’s bad.” – Cory House",
        "“First, solve the problem. Then, write the code.” – John Johnson"
    ]
    print(f"Assistant: {random.choice(quotes)}")

def forget_data():
    """Deletes the stored notes file."""
    if os.path.exists("my_notes.txt"):
        os.remove("my_notes.txt")
        print("Assistant: All your stored notes have been securely deleted.")
    else:
        print("Assistant: You have no stored data to delete.")

def log_unanswered(user_input):
    """Logs unrecognized queries for future improvement."""
    with open("unanswered_queries.log", "a") as file:
        file.write(f"{datetime.datetime.now()}: {user_input}\n")
    print("Assistant: I didn't understand that. I've logged this query to improve my future training.")

# ==========================================
# 2.A KNOWLEDGE & REASONING LAYER
# ==========================================

# The Rule Base (Propositional Logic Simulation)
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
    (["forget", "delete data", "erase"], "forget_data")
]

def forward_chaining_inference(user_input):
    """
    Inference Engine: Matches facts from user input against the Rule Base.
    Returns the inferred intent, confidence score, and the rule trace.
    """
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
# 2.B DECIDE: The Smart Intent Router
# ==========================================

def decide_and_act(user_input):
    global last_trace
    
    # 1. Run the inference engine
    intent, confidence, trace = forward_chaining_inference(user_input)
    last_trace = trace
    
    if intent == "unknown":
        log_unanswered(user_input)
        return
        
    # 2. Check Confidence Threshold (70%)
    if confidence < 0.7:
        clarification = input(f"Assistant: I am only {confidence*100}% sure. Did you mean to '{intent}'? (yes/no): ")
        if "y" not in clarification.lower():
            print("Assistant: Okay, cancelling action. Please try rephrasing.")
            return

    # 3. Act based on the inferred intent
    if intent == "check_time": get_time()
    elif intent == "read_notes": read_notes()
    elif intent == "save_note": save_note(user_input)
    elif intent == "math": calculate(user_input)
    elif intent == "search": search_info(user_input)
    elif intent == "open_web": open_website(user_input)
    elif intent == "flip_coin": flip_coin()
    elif intent == "roll_die": roll_die()
    elif intent == "joke": tell_joke()
    elif intent == "quote": give_quote()
    elif intent == "forget_data": forget_data()

# ==========================================
# 1. PERCEIVE: The Agent Loop
# ==========================================

print("Assistant: Hello! I am online. Type 'quit' to exit.")

while True:
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Assistant: Goodbye!")
        break
    
    decide_and_act(user_input)