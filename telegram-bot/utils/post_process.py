from requests import post
from json import dumps

from .learning import reply_learning_data
from .logger import get_logger
from .mode import Mode
from .config import SUGGEST_PATH

logger = get_logger(__name__)


def new_post_process(data, message, context):
    headers = {
        'Content-type': 'application/json',
        'Accept': '*/*'
    }
    result = post(SUGGEST_PATH, data=dumps(data), headers=headers)
    context.user_data["resume_list"] = result.json()["result"][::-1]
    context.user_data["vacancy_id"] = result.json()["vacancy"] or "12345"
    context.user_data["dataLoad"] = data
    context.user_data["mode"] = Mode.LEARNING
    message.reply_text(
        "Я подготовил для вас подборку резюме. Но необходимо помочь их мне отранжировать. "
        "Я буду предлагать тебе резюме на оценку. "
        "Как надоест, введи /stop - и я верну тебе конечный результат."
    )
    reply_learning_data(context.user_data["vacancy_id"], context.user_data["resume_list"][-1], message, context)
