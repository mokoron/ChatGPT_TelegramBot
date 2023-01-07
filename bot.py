import openai
import logging
from warnings import filters

from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
import json

# Load chatgpt.json file
with open('chatgpt.json') as f:
  data = json.load(f)
# Set up ChatGPT API client
openai.api_key = data['OpenAItoken']

async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a ChatGPT bot. How can I help you today?")


async def chat(update, context: ContextTypes.DEFAULT_TYPE):
    # Check if message is not None
    if update.message and update.message.text:
        # Get user's message
        message = update.message.text

        # Send message to ChatGPT API
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=message,
            max_tokens=900,
            temperature=0.5
        )

        # Get response from ChatGPT API
        response_text = response['choices'][0]['text']

        # Send response to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)



if __name__ == '__main__':
    application = ApplicationBuilder().token(data['TelegramBotToken']).build()

    start_handler = CommandHandler('start', start)

    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    application.add_handler(start_handler)
    application.add_handler(chat_handler)


    application.run_polling()


