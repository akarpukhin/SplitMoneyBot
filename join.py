from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from botdb import Goal


def join(bot, update):
    keyboard = [['Event'], ['Goal']]
    choice_keyboard = ReplyKeyboardMarkup(keyboard)
    bot.send_message(
        update.message.chat_id,
        text="Куда вы хотите присоедениться ?",
        reply_markup=choice_keyboard)
    return "Choice"


def choose_goal(bot, update):
    # choice = update.message.text  не помню зачем добавлял, если не вспомню, удалю
    goal_list = [['Цель: {}'.format(g.goal_name)]
                 for g in Goal.query.filter(Goal.status == 'A')]

    if len(goal_list) < 1:
        keyboard = [['Yes'], ['No']]
        choice_keyboard = ReplyKeyboardMarkup(keyboard)
        bot.send_message(
            update.message.chat_id,
            text="Сейчас нет активных целей. Создать ?",
            reply_markup=choice_keyboard
        )
        return "Choice"

    if len(goal_list) > 1:
        keyboard = goal_list
        goal_keyboard = ReplyKeyboardMarkup(keyboard)
        bot.send_message(
            update.message.chat_id,
            text="Выбери цель:",
            reply_markup=goal_keyboard
        )
        return "Join"

    if len(goal_list) == 1:
        keyboard = goal_list
        goal_keyboard = ReplyKeyboardMarkup(keyboard)
        bot.send_message(
            update.message.chat_id,
            text="Вы хотите присоедениться к этой цели ?",
            reply_markup=goal_keyboard
        )
        return "Join"


def join_goal(bot, update):
    goal_name = update.message.text
    goal_name = goal_name.split(': ')[1]
    goal_id = [g.id
               for g in Goal.query.filter(Goal.status == 'A' and Goal.goal_name == goal_name)]


def event_join(bot, update):
    choice = update.message.text
    remove_choice_keyboard = ReplyKeyboardRemove()
    bot.send_message(
        update.message.chat_id,
        text="Ты выбрал {choice}!".format(choice=choice),
        reply_markup=remove_choice_keyboard
    )
    return "Menu"
