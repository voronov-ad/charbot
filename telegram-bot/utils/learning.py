from json import dumps
from requests import post, get
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

from .logger import get_logger
from .config import BACKEND_PATH

logger = get_logger(__name__)
learning_replies = {
    "like": "\U0001F44D",
    "dislike": "\U0001F44E",
    "hire": "\U0001F525"
}


def reply_learning_data(vacancy_id, resume, message, context):
    message.reply_text(f"Подходит ли под вакнсию {vacancy_id} данное резюме: {resume}", reply_markup=InlineKeyboardMarkup([[
        InlineKeyboardButton(learning_replies[reply], callback_data=reply) for reply in learning_replies
    ]]))


def get_learning_data(vacancy_id):
    data = get(f'{BACKEND_PATH}/api/related-vacancy?id={vacancy_id}')
    return data.json()


def send_learning_data(vote, vacancy_id, resume):
    data = {
        "url_vacancy": f"https://hh.ru/vacancy/{vacancy_id}",
        "url_candidate": resume,
        "label": 1 if vote == "like" or vote == "hire" else 0
    }
    headers = {
        'Content-type': 'application/json',
        'Accept': '*/*'
    }
    result = post(f"{BACKEND_PATH}/api/v1/feedback", data=dumps(data), headers=headers)
    logger.info(f"Send feedback result: {result.status_code}")
