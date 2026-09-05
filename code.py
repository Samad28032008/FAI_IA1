import datetime
import wikipedia
import os
import webbrowser

# ==========================================
# 3. ACT: The Action Functions
# ==========================================

def get_time():
    now = datetime.datetime.now()
    print(f"Assistant: The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}")

def save_note(user_input):
    note_content = user_input.replace("note", "").replace("remember", "").strip()
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
    # Remove the word "open" to find the target website
    site_name = user_input.replace("open", "").strip()
    
    if site_name == "":
        print("Assistant: Please tell me which website to open, like 'open youtube'.")
        return
        
    # Smart routing: check if the user included ".com" or ".org"
    if "." not in site_name:
        url = f"https://www.{site_name}.com"
    else:
        url = f"https://{site_name}"
        
    print(f"Assistant: Opening {site_name} in your web browser...")
    webbrowser.open(url)

def fallback():
    print("Assistant: I didn't understand that. You can ask me for the time, save a note, do math, search for info, or open a website.")

# ==========================================
# 2. DECIDE: The Intent Router
# ==========================================

def decide_and_act(user_input):
    text = user_input.lower()
    
    if "time" in text or "date" in text:
        get_time()
    elif "show notes" in text or "read notes" in text:
        read_notes()
    elif "note" in text or "remember" in text:
        save_note(text)
    elif "calculate" in text or "math" in text:
        calculate(text)
    elif "search" in text or "who is" in text or "what is" in text:
        search_info(text)
    elif "open" in text:
        open_website(text)
    else:
        fallback()

# ==========================================
# 1. PERCEIVE: The Agent Loop (Text Input)
# ==========================================

print("Assistant: Hello! I am online. Type 'quit' to exit.")

while True:
    # Perceive: Read typed input from the user
    user_input = input("\nYou: ")
    
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Assistant: Goodbye!")
        break
    
    # Send the perceived input to the brain
    decide_and_act(user_input)