import telebot
import json
import os
from config import BOT_TOKEN, ADMIN_ID, LOGGING_LEVEL

bot = telebot.TeleBot(BOT_TOKEN)
user_states = {}

GAME_DATA_FILE = 'texts.json'

if os.path.exists(GAME_DATA_FILE):
    with open(GAME_DATA_FILE, 'r', encoding='utf-8') as f:
        game_data = json.load(f)
else:
    print(f"Error: '{GAME_DATA_FILE}' not found.")
    exit(1)

def log_message(message_type, user_id, username, content=''):
    if LOGGING_LEVEL == 0:
        return
    if LOGGING_LEVEL == 1 and message_type not in ['start', 'end']:
        return
    log_text = f"{message_type.upper()} - User ID: {user_id}, Username: {username}"
    if content:
        log_text += f", Content: {content}"
    bot.send_message(ADMIN_ID, log_text)

# Start command handler
@bot.message_handler(commands=['start'])
def start_message(message):
    user_states[message.chat.id] = 'start'
    send_message_with_buttons(message.chat.id, 'start')
    log_message('start', message.chat.id, message.from_user.username)

# Message handler for button clicks and text inputs
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    state = user_states.get(chat_id, 'start')
    user_input = message.text.strip()
    log_message('input', chat_id, message.from_user.username, user_input)

    if state in game_data and user_input in game_data[state]['buttons']:
        next_state = game_data[state]['buttons'][user_input]
        user_states[chat_id] = next_state
        send_message_with_buttons(chat_id, next_state)
    else:
        bot.send_message(chat_id, "I don't understand that choice. Please select one of the available options.")

# Function to send messages with keyboard buttons
def send_message_with_buttons(chat_id, state):
    if state in game_data:
        text = game_data[state]['text']
        buttons = game_data[state].get('buttons', None)

        if buttons:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button_text in buttons:
                keyboard.add(telebot.types.KeyboardButton(button_text))
            bot.send_message(chat_id, text, reply_markup=keyboard)
        else:
            # If no buttons, remove the keyboard
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Oops, something went wrong...", reply_markup=telebot.types.ReplyKeyboardRemove())

# Restart command handler
@bot.message_handler(commands=['restart'])
def restart_game_command(message):
    user_states[message.chat.id] = 'start'
    send_message_with_buttons(message.chat.id, 'start')
    log_message('restart', message.chat.id, message.from_user.username)

# Back command handler
@bot.message_handler(commands=['back'])
def go_back(message):
    chat_id = message.chat.id
    state_history = get_user_state_history(chat_id)

    if len(state_history) > 1:
        # Remove the last state to go back
        state_history.pop()
        # Update the user's current state
        user_states[chat_id] = state_history[-1]
        send_message_with_buttons(chat_id, state_history[-1])
    else:
        bot.send_message(chat_id, "You're already at the beginning of the game!")

# Function to get the user's state history
def get_user_state_history(chat_id):
    if chat_id not in user_states:
        user_states[chat_id] = 'start'
    # For simplicity, we're using a list to track state history per user
    # In a production environment, consider a more robust method or database
    if '_history' not in user_states:
        user_states['_history'] = {}
    if chat_id not in user_states['_history']:
        user_states['_history'][chat_id] = ['start']
    return user_states['_history'][chat_id]

# Overriding send_message_with_buttons to update state history
def send_message_with_buttons(chat_id, state):
    if state in game_data:
        # Update user's state history
        state_history = get_user_state_history(chat_id)
        state_history.append(state)
        user_states['_history'][chat_id] = state_history

        text = game_data[state]['text']
        buttons = game_data[state].get('buttons', None)

        if buttons:
            keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
            for button_text in buttons:
                keyboard.add(telebot.types.KeyboardButton(button_text))
            bot.send_message(chat_id, text, reply_markup=keyboard)
        else:
            # If no buttons, remove the keyboard
            bot.send_message(chat_id, text, reply_markup=telebot.types.ReplyKeyboardRemove())
    else:
        bot.send_message(chat_id, "Oops, something went wrong...", reply_markup=telebot.types.ReplyKeyboardRemove())

bot.set_my_commands([
    telebot.types.BotCommand('start', 'Start the game'),
    telebot.types.BotCommand('restart', 'Restart the game'),
    telebot.types.BotCommand('back', 'Go back one step')
])

# Handler for stopping the bot gracefully (e.g., /stop command)
@bot.message_handler(commands=['stop'])
def stop_bot(message):
    log_message('end', message.chat.id, message.from_user.username)
    bot.send_message(message.chat.id, "Thank you for playing! Goodbye.")
    # Perform any cleanup here if necessary

bot.polling()