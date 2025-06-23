## Adventure Game Master 

This is a simple text-based adventure game powered by AI emotion detection and music integration.



## Features

- Turn-based storytelling with emotional branching
- Emotion analysis based on player input
- Dynamic background music using `pygame`
- Agent-based system design with [Google ADK](https://github.com/google/agent-development-kit)
- All story content is presented in both Traditional Chinese and English for accessibility and immersion.
- Modular design with exposed agent tools (start, process, status, stop, diagnostics) for integration with LLM agents



## Project Structure

adventure_game/
├── emotion_analyzer.py        # Emotion classification based on user input
├── music_player.py            # Music playback logic using pygame
├── game_state.py              # Game state management (turns, history, etc.)
├── .env                       # Optional environment config (not required)
├── __init__.py                # Marks this folder as a Python package
├── requirements.txt           # Python dependencies
├── README.md                  # Project overview and instructions
├── adventure_game_master/
│  └── agent.py               # Main ADK agent logic and tool definitions
└── music/
    ├── intro.mp3
    ├── tense_battle.mp3
    ├── sad.mp3
    ├── ...
    └── ending(victory).mp3    # AI-generated background music from Mubert


## How to Run Locally

1. Clone the repo  
2. Create a virtual environment *(optional but recommended)*
3. Install dependencies: 
   
   pip install -r requirements.txt

IMPORTANT: To run this project, You must create a .env file in the root folder with the following content:
GOOGLE_API_KEY=your_api_key_here

4. Run the ADK web interface:
   
   adk web

5. Open your browser and go to http://localhost:8000/dev-ui

6. Select the adventure_game_master agent and start your adventure!



🎵 Music Folder
Make sure to include a music/ folder with your .mp3 files:

advance.mp3  
battle_2.mp3  
charge.mp3  
ending(defeat).mp3  
ending(peaceful).mp3  
ending(victory).mp3  
heroic death.mp3  
intro.mp3  
retreat.mp3  
sacrifice.mp3  
sad.mp3  
smile.mp3  
tense_battle.mp3  
wait_hide.mp3  

All background music tracks were generated using Mubert AI Music Generator, an AI-powered platform for royalty-free soundtracks.
Each track was designed to match specific emotional tones such as fear, courage, peace, sadness, and tension.



## 🧠 Powered By

- [Google Agent Development Kit] (https://github.com/google/agent-development-kit)
- pygame for music playback
- Mubert AI Music Generator for all background music
- ChatGPT, Gemini, and Claude as collaborative coding development assistants
