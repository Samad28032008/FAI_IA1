import datetime
import wikipedia
import os

# ==========================================
# 3. ACT: The Action Functions
# ==========================================

def get_time():
    now = datetime.datetime.now()
    print(f"Assistant: The current date and time is {now.strftime('%Y-%m-%d %H:%M:%S')}")

def save_note(user_input):
    # Remove the trigger word to just save the note content
    note_content = user_input.replace("note", "").replace("remember", "").strip()
    
    # Open a text file in "append" mode (creates it if it doesn't exist)
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
    # Keep only numbers and math symbols
    math_equation = ''.join(char for char in user_input if char in '0123456789+-*/().')
    try:
        # eval() safely solves basic math strings like "5+5"
        result = eval(math_equation)
        print(f"Assistant: The answer is {result}")
    except:
        print("Assistant: Sorry, I couldn't understand the math equation.")

def search_info(user_input):
    # Clean up the search query
    query = user_input.replace("search", "").replace("who is", "").replace("what is", "").strip()
    print(f"Assistant: Looking up '{query}'...")
    try:
        # Get a short 2-sentence summary from Wikipedia
        summary = wikipedia.summary(query, sentences=2)
        print(f"Assistant: {summary}")
    except:
        print("Assistant: Sorry, I couldn't find any clear information on that.")

def fallback():
    print("Assistant: I didn't understand that. You can ask me for the time, to save a note, do math, or search for info.")

# ==========================================
# 2. DECIDE: The Intent Router
# ==========================================

def decide_and_act(user_input):
    # Convert input to lowercase to make keyword matching easier
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
    else:
        fallback()

# ==========================================
# 1. PERCEIVE: The Agent Loop
# ==========================================

print("Assistant: Hello! I am online. Type 'quit' to exit.")

while True:
    # Perceive: Listen for user input
    user_input = input("\nYou: ")
    
    # Check if the user wants to exit the loop
    if user_input.lower() in ["exit", "quit", "stop"]:
        print("Assistant: Goodbye!")
        break
    
    # Send the perceived input to the brain (Decide & Act)
    decide_and_act(user_input)
