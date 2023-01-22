#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
import logging
import analytics
import json

from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


# Load config.json file
with open('config.json') as f:
  config = json.load(f)

# Set up ChatGPT API client
openai.api_key = config['OpenAItoken']
async def start(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I am a ChatGPT bot. How can I help you today? Just send me a message and I will keep talking.")

async def statistic(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=analytics.analysis())


async def about(update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="This is ChatGPT bot which can assist you in different tasks.\
You can ask to translate, rephrase or summarize text. \
You can also ask to create a letter or meeting agenda. \nEnjoy 🙂 \nBy @yuliya_rubtsova\n \n \n\
ChatGPT - это бот, который может помочь вам с различными задачами.\
Вы можете попросить его перевести, перефразировать или обобщить текст, а также создать письмо или повестку дня для встречи.\
\nПриятной работы 🙂 \nВопросы и предложения можете слать автору: @yuliya_rubtsova")

async def donate(update, context: ContextTypes.DEFAULT_TYPE):

    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text='Sadly, OpenAI charges money for each request to the ChatGPT model, so if you appreciate the bot, <a href="some url">you can help to keep it running</a>\n \n \n\
К сожалению, OpenAI берет деньги за каждый запрос к модели ChatGPT, поэтому, если вы цените бота, вы можете <a href="some url">помочь и поддерживать его работу</a>', parse_mode='HTML')


async def chat(update, context: ContextTypes.DEFAULT_TYPE):
    # Check if message is not None
    if update.message and update.message.text:
        # Get user's message
        message = update.message.text
        # Get statistics
        analytics.statistics(update.effective_chat.id)
        # Send message to ChatGPT API
        response = openai.Completion.create(
            #engine="text-davinci-003",
            model= "text-davinci-003",
            prompt=message,
            max_tokens=500,
            temperature=0.3
        )

        # Get response from ChatGPT API
        response_text = response['choices'][0]['text']

        # Send response to user
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response_text)



if __name__ == '__main__':
    application = ApplicationBuilder().token(config['TelegramBotToken']).build()

    start_handler = CommandHandler('start', start)
    chat_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chat)
    statistic_handler = CommandHandler('statistic', statistic)
    about_handler = CommandHandler('about', about)
    donate_handler = CommandHandler('donate', donate)

    application.add_handler(start_handler)
    application.add_handler(chat_handler)
    application.add_handler(statistic_handler)
    application.add_handler(about_handler)
    application.add_handler(donate_handler)

    application.run_polling()

