# Smart Personal Assistant (Python Intelligent Agent)

A lightweight, text-based intelligent personal assistant built entirely in Python. This project demonstrates the foundational architecture of an AI agent using a continuous **Perceive → Decide → Act** loop. It handles everyday tasks, persists data to the local file system, and routes user intents to specific actions.

##  Features

*   **Information Lookup:** Searches Wikipedia for quick summaries ("who is...", "what is...").
*   **Persistent Notes:** Saves and retrieves personal notes/reminders using local file I/O.
*   **Math Calculator:** Solves standard mathematical equations safely.
*   **Web Navigation:** Opens websites directly in the default browser.
*   **Time & Date:** Fetches current system time.
*   **Quick Decisions:** Flips coins and rolls dice for random outcomes.
*   **Personality Module:** Tells programming jokes and shares inspirational quotes.
*   **Fallback Handling:** Gracefully handles unrecognized intents.

##  Prerequisites

*   Python 3.x installed on your machine.
*   An active internet connection (for Wikipedia and Web Browser features).

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/yourusername/your-repo-name.git](https://github.com/yourusername/your-repo-name.git)
   1. Navigate to the project directory:

Bash
cd your-repo-name
  2.Install the required third-party Wikipedia library:

Bash
pip install wikipedia
💻 Usage
Run the main Python script from your terminal to start the assistant loop:

Bash
python assistant.py
