
# !/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""
from json import dumps

from requests import post
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler

from utils.ide import IDEIntegration, IDEtoTelegramResponseMapper
from utils.learning import reply_learning_data, send_learning_data, get_learning_data, learning_replies
from utils.logger import get_logger
from utils.mode import Mode
from utils.post_process import new_post_process
from utils.config import MANAGER_SCENARIO_WEBHOOK, RESUME_SCENARIO_WEBHOOK, SCREENING_SCENARIO_WEBHOOK, SUGGEST_PATH
logger = get_logger(__name__)
ide_manager = IDEIntegration(MANAGER_SCENARIO_WEBHOOK)
ide_resume = IDEIntegration(RESUME_SCENARIO_WEBHOOK)
ide_screening = IDEIntegration(SCREENING_SCENARIO_WEBHOOK)
ide_response_mapper = IDEtoTelegramResponseMapper()

IDEs = {
    "new": ide_manager,
    "screening": ide_screening,
    "create_resume": ide_resume
}


# Define a few command handlers. These usually take the two arguments update and
# context.
def send_event(event, update: Update, context: CallbackContext):
    mode = context.user_data.get("mode", None)
    if mode in IDEs:
        ide = IDEs[mode]
        response = ide.send_event(
            mid=update.update_id,
            uid=update.message.from_user.username,
            event=event
        )
        data = ide_response_mapper.reply_text(update.message.reply_text, response)
        if data:
            context.user_data["mode"] = Mode.NEW_POST_PROCESS
            new_post_process(data, update.message, context)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Я создан, чтобы помогать искать резюме :) У меня есть несколько команд.')
    update.message.reply_text('/new - новый поиск кандидатов.')
    update.message.reply_text('/screening - прохождение скринига для кандидата.')
    update.message.reply_text('/create_resume - помощь в создании резюме для кандидата.')
    update.message.reply_text('/run_learning - команда для запуска режима обучения модели.')
    update.message.reply_text('/stop - команда для завершения каждого из режимов.')


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Привет {user.mention_markdown_v2()}\! Я ваш личный помощник по поиску кандидатов :\) '
        fr'Чтобы узнать основные возможности, восполуьзуйтесь командой /help\.'
        fr'Или оспользуйся командой /new, чтобы начать поиск\!',
        reply_markup=ForceReply(selective=True),
    )


def create_resume(update: Update, context: CallbackContext) -> None:
    """Помощь пользователю в создании резюме."""
    mode = context.user_data.get("mode", None)
    if mode:
        update.message.reply_text(
            f"Запущен mode {mode}. Необходимо его остановить командой /stop прежде, чем запускать новый сценарий."
        )
    else:
        context.user_data["mode"] = Mode.CREATE_RESUME
        send_event("new", update, context)


def new(update: Update, context: CallbackContext) -> None:
    """Завести новое резюме."""
    mode = context.user_data.get("mode", None)
    if mode:
        update.message.reply_text(
            f"Запущен mode {mode}. Необходимо его остановить командой /stop прежде, чем запускать новый сценарий."
        )
    else:
        context.user_data["mode"] = Mode.NEW
        send_event("new", update, context)


def screening(update: Update, context: CallbackContext) -> None:
    """Завести новое резюме."""
    mode = context.user_data.get("mode", None)
    if mode:
        update.message.reply_text(
            f"Запущен mode {mode}. Необходимо его остановить командой /stop прежде, чем запускать новый сценарий."
        )
    else:
        context.user_data["mode"] = Mode.SCREENING
        send_event("new", update, context)


def is_int(obj):
    try:
        _ = int(obj)
        return True
    except Exception as exception:
        return False


def message_handler(update: Update, context: CallbackContext) -> None:
    """Отлавливаем все текстовые сообщения."""
    mode = context.user_data.get("mode", None)

    if mode == Mode.LEARNING:
        vacancy_id = context.user_data.get("vacancy_id", None)
        if not vacancy_id and is_int(update.message.text):
            vacancy_id = update.message.text
            context.user_data["vacancy_id"] = vacancy_id
            resume_list = get_learning_data(vacancy_id)
            if resume_list:
                context.user_data["resume_list"] = resume_list[:-1]
                reply_learning_data(vacancy_id, resume_list[-1], update.message, context)
                return
            else:
                update.message.reply_text(
                    "К сожалению, по данной вакансии нет подходящих резюме."
                    " Назовите id вакансии с hh.ru (число в ссылке)"
                )
                return
        elif not vacancy_id:
            update.message.reply_text("Назовите id вакансии с hh.ru (число в ссылке)")
            return

        resume_list = context.user_data.get("resume_list", [])
        if resume_list:
            reply_learning_data(vacancy_id, resume_list[-1], update.message, context)
            return
        else:
            context.user_data["vacancy_id"] = None
            update.message.reply_text("Назовите id вакансии с hh.ru (число в ссылке)")

    elif mode in IDEs:
        ide = IDEs[mode]
        response = ide.send_text(
            mid=update.update_id,
            uid=update.message.from_user.username,
            text=update.message.text
        )
        data = ide_response_mapper.reply_text(update.message.reply_text, response)
        if data:
            context.user_data["mode"] = Mode.NEW_POST_PROCESS
            new_post_process(data, update.message, context)


def button(update: Update, context: CallbackContext) -> None:
    """Parses the CallbackQuery and updates the message text."""
    query = update.callback_query
    mode = context.user_data.get("mode", None)

    query.answer()
    if mode == Mode.LEARNING:
        query.edit_message_text(f"{learning_replies[update.callback_query.data]} " + query.message.text)
        vacancy_id = context.user_data.get("vacancy_id", None)
        resume_list = context.user_data.get("resume_list", None)

        resume = resume_list[-1]
        send_learning_data(update.callback_query.data, vacancy_id, resume)

        if len(resume_list) > 1:
            context.user_data["resume_list"] = resume_list[:-1]
            reply_learning_data(vacancy_id, resume_list[-2], update.callback_query.message, context)
        else:
            context.user_data["resume_list"] = None
            context.user_data["vacancy_id"] = None
            update.callback_query.message.reply_text(
                "Резюме закончились. Назовите id новой вакансии с hh.ru (число в ссылке) "
            )

    elif mode in IDEs:
        ide = IDEs[mode]

        query.edit_message_text(query.message.text)
        response = ide.send_text(
            mid=update.update_id,
            uid=update.callback_query.from_user.username,
            text=query.data
        )
        data = ide_response_mapper.reply_text(update.callback_query.message.reply_text, response)
        if data:
            context.user_data["mode"] = Mode.NEW_POST_PROCESS
            new_post_process(data, update.callback_query.message, context)


def run_learning(update: Update, context: CallbackContext) -> None:
    """ Запустить обучение. """
    context.user_data["mode"] = Mode.LEARNING
    update.message.reply_text("Запущен процесс обучения. Чтобы выйти из него используйте команду /stop.")
    update.message.reply_text("Назовите id вакансии на hh")
    # reply_learning_data(update.message, context)


def stop(update: Update, context: CallbackContext) -> None:
    """ Запустить обучение. """
    mode = context.user_data.get("mode", None)
    context.user_data["mode"] = None
    update.message.reply_text("Процесс обучения завершён.")

    if mode == Mode.LEARNING and context.user_data.get("vacancy_id", None) and context.user_data.get("dataLoad", None):
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*'
        }
        data = post(SUGGEST_PATH, data=dumps(context.user_data["dataLoad"]), headers=headers)
        # data = get_learning_data(context.user_data["vacancy_id"])
        update.message.reply_text(f"Тебе лучше всего подойдут кандидаты: {data.json()['result'][:10]}")


def main() -> None:
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    updater = Updater("2060726235:AAGXvRaZluRuGQ4oPxuDZp4r8w51JauisOI")

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("new", new))
    dispatcher.add_handler(CommandHandler("run_learning", run_learning))
    dispatcher.add_handler(CommandHandler("stop", stop))
    dispatcher.add_handler(CommandHandler("screening", screening))
    dispatcher.add_handler(CommandHandler("create_resume", create_resume))
    dispatcher.add_handler(CallbackQueryHandler(button))

    # on non command i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, message_handler))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()

