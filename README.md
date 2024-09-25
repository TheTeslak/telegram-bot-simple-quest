![Telegram](https://img.shields.io/badge/telegram-API-blue)

# Telegram Text Adventure Game Bot

A simple Telegram bot that offers a text-based adventure game experience. Players make choices by clicking on buttons, navigating through different story paths. Easily customizable and extensible to create your own unique adventures.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Bot](#running-the-bot)
- [Usage](#usage)
- [Customization](#customization)
- [Ideas for Improvement](#ideas-for-improvement)

## Features

- **Interactive Storytelling**: Navigate through the adventure by making choices via Telegram buttons.
- **Customizable Storyline**: Easily modify the story through a JSON file.
- **User-Friendly Commands**:
  - `/start` - Begin the game
  - `/restart` - Restart the game from the beginning
  - `/back` - Go back one step in the story
- **State Management**: Keeps track of user progress, allowing players to restart or backtrack.
- **Logging**: Logs user interactions for monitoring and debugging.
- **Extensible**: Designed to be easily expanded with additional features like multi-language support or dynamic content.

## Prerequisites

- **Python**: Version 3.6 or higher
- **Telegram Account**: To interact with the bot
- **Telegram Bot Token**: Obtainable from [BotFather](https://t.me/BotFather)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/telegram-text-adventure-bot.git
cd telegram-text-adventure-bot
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Create a `config.py` File

Create a `config.py` file in the project root directory with the following content:

```python
BOT_TOKEN = 'YOUR_ACTUAL_BOT_TOKEN'
ADMIN_ID = YOUR_TELEGRAM_USER_ID
LOGGING_LEVEL = 1  # 0: No logging, 1: Minimal logging, 2: Detailed logging
```

- **BOT_TOKEN**: Replace `'YOUR_ACTUAL_BOT_TOKEN'` with the token you received from BotFather.
- **ADMIN_ID**: Replace `YOUR_TELEGRAM_USER_ID` with your Telegram user ID to receive logs. You can find your user ID by messaging [@userinfobot](https://t.me/userinfobot) on Telegram.
- **LOGGING_LEVEL**:
  - `0`: No logging.
  - `1`: Minimal logging (e.g., start and end commands).
  - `2`: Detailed logging (all user inputs).

### 2. Prepare the Story Data

Ensure that the `texts.json` file is present in the project directory. This file contains the game's storyline and choices. An example structure:

```json
{
  "start": {
    "text": "Welcome to the adventure! Do you go left or right?",
    "buttons": {
      "Left": "left_path",
      "Right": "right_path"
    }
  },
  "left_path": {
    "text": "You took the left path and encountered a river. Do you swim across or build a raft?",
    "buttons": {
      "Swim": "swim_river",
      "Build": "build_raft"
    }
  },
  "right_path": {
    "text": "You took the right path and found a treasure chest. Do you open it or leave it?",
    "buttons": {
      "Open": "open_chest",
      "Leave": "leave_chest"
    }
  }
  // Add more states as needed
}
```

## Running the Bot

Start the bot by running the following command:

```bash
python bot.py
```

The bot will begin polling for messages. Ensure that the `texts.json` and `config.py` files are correctly set up before running.

## Usage

Interact with your bot on Telegram using the following commands:

- `/start` - Begin the game
- `/restart` - Restart the game from the beginning
- `/back` - Go back one step in the story
- `/stop` - (Optional) Gracefully stop the bot (requires implementation)

### Example Interaction:

- **User**: `/start`
- **Bot**: "Welcome to the adventure! Do you go left or right?" with "Left" and "Right" buttons.
- **User**: Clicks "Left"
- **Bot**: "You took the left path and encountered a river. Do you swim across or build a raft?" with "Swim" and "Build" buttons.

And so on...

## Customization

### Editing the Story

The game's story is stored in `texts.json`. You can modify this file to create your own narrative. The structure for each state is as follows:

```json
"state_name": {
  "text": "The narrative text displayed to the player at this state.",
  "buttons": {
    "Button Label": "next_state_name"
  }
}
```

- **state_name**: A unique identifier for each state in the game.
- **text**: The message displayed to the player.
- **buttons**: A dictionary where each key is the label of a button, and the value is the `state_name` it leads to.

### Adding New States

1. **Define a New State**: Add a new entry in `texts.json`:

```json
"new_state": {
  "text": "Your new story segment here.",
  "buttons": {
    "Choice 1": "next_state_1",
    "Choice 2": "next_state_2"
  }
}
```

2. **Reference the New State**: In an existing state, add a button that points to the new state:

```json
"existing_state": {
  "text": "Existing story text.",
  "buttons": {
    "New Choice": "new_state",
    // Other choices
  }
}
```

### Multi-language Support

To support multiple languages:

1. **Create Separate JSON Files**: For each language, create a separate JSON file (e.g., `texts_en.json`, `texts_es.json`).
2. **Load Based on User Preference**: Modify the bot to detect or allow users to select their preferred language and load the corresponding JSON file.

## Enhancements

Consider implementing the following features to improve the bot:

- **State Persistence**: Use a database to save user states, ensuring continuity even if the bot restarts.
- **Inline Keyboards**: Replace reply keyboards with inline keyboards for a more polished user interface.
- **Dynamic Content**: Allow users to input text to make the game more interactive and personalized.
- **Advanced Logging**: Implement comprehensive logging to monitor errors and user interactions effectively.
- **Unit Testing**: Add tests to ensure all functionalities work as expected.

## Ideas for Improvement

- **Deploy to Cloud Platforms**: Host the bot on platforms like Heroku, AWS, or Google Cloud for better accessibility.
- **User Profiles**: Maintain user profiles to track progress, preferences, or achievements.
- **Rich Media Integration**: Incorporate images, videos, or audio to enhance storytelling.
- **Branching Narratives**: Develop more complex storylines with multiple branching paths and endings.
```
