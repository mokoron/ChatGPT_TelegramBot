import openai
import logging
from warnings import filters

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import json
import os

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
import json

# Load chatgpt.json file
file_path = __file__
dir_name = os.path.dirname(file_path)
file_path = os.path.join(dir_name, 'chatgpt.json')

with open(file_path) as f:
  data = json.load(f)
# Set up ChatGPT API client
openai.api_key = data['OpenAItoken']

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a ChatGPT bot. How can I help you today?")


async def chat(update, context: ContextTypes.DEFAULT_TYPE):
        # Get the user's ID
    user_id = update.message.from_user.id
    print(user_id)
    print(data['TelegramChatId'])
    # Check if the user's ID is the one you want
    if user_id != data['TelegramUserId']:
        # Do something here
        context.bot.send_message(chat_id=update.message.chat_id, text="Sorry, you are not authorized to use this bot.")
        return 

    # Check if message is not None
    if update.message and update.message.text:
        # Get user's message
        message = update.message.text

        # Send message to ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=1000,
            temperature=0.7
        )

        # Get response from ChatGPT API
        response_text = response['choices'][0]['text']

        # Send response to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)


if __name__ == '__main__':
    application = ApplicationBuilder().token(data['TelegramBotToken']).build()

# add check of telegram user id
    start_handler = CommandHandler('start', start)

    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)


    application.run_polling()


