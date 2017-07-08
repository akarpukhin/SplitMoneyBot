from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, RegexHandler
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.chat import Chat
import os
from datetime import datetime
import sys
import time
import configs
import logging
from botdb import db_session, engine
from botdb import Base, User, Goal, Event, List
import fundraising, info, join, put, event

if not os.path.exists(configs.LOG_FILE):
    os.mkdir(os.path.dirname(configs.LOG_FILE))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename=configs.LOG_FILE
                    )


def start_bot(bot, update):
    mytext = "Привет {}! Спасибо, что добавили меня!".format(update.message.chat.first_name)
    logging.info('Пользователь {} нажал /start'.format(update.message.chat.username))
    update.message.reply_text(mytext)


def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hi! \n I'm SplitMoneyBot! \n\n"
                                                 "<b>Fundraising</b>\n"
                                                 "/fundraising\n"
                                                 "/join\n"
                                                 "/info\n"
                                                 "/put\n\n"
                                                 "<b>Events</b>\n"
                                                 "/events\n\n"
                                                 "<b>You can also use</b>\n"
                                                 "/help\n"
                                                 "/exit\n"
                                                 "/reset", parse_mode='HTML')
    return 'Menu'


def f_help(bot, update):
    pass


def stop(bot, update):
    kill_keyboard = ReplyKeyboardRemove()
    bot.sendMessage(
        update.message.chat_id,
        text="stop!",
        reply_markup=kill_keyboard)
    return ConversationHandler.END


def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...!")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


main_conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],

    states={
        'Menu': [CommandHandler('fundraising', fundraising.fundraising),
                 CommandHandler('join', join.join),
                 CommandHandler('info', info.info, pass_args=True),
                 CommandHandler('put', put.put),
                 CommandHandler("event", event.event),
                 CommandHandler("help", f_help),
                 CommandHandler("exit", stop)],

        'Choice': [RegexHandler('^(Goal)$', join.choose_goal),
                   RegexHandler('^(Event)$', join.event_join),
                   RegexHandler('^(Yes)$', fundraising.fundraising),
                   RegexHandler('^(No)$', stop)],

        'Join': [RegexHandler('^(Цель\:.*)$', join.join_goal)],
    },

    fallbacks=[CommandHandler("exit", stop)]
)


def main():
    Base.metadata.create_all(bind=engine)

    updtr = Updater(configs.TELEGRAM_BOT_KEY)

    updtr.dispatcher.add_handler(main_conversation_handler)
    updtr.dispatcher.add_handler(CommandHandler("reset", restart))
    updtr.start_polling()
    updtr.idle()


if __name__ == "__main__":
    logging.info('Bot started')
    main()
()
