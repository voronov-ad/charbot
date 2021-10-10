import json
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from .logger import get_logger

logger = get_logger(__name__)


class IDEIntegration:
    def __init__(self, webhook):
        self.webhook = webhook

    @staticmethod
    def create_text_message(mid, uid, text):
        return {
            "messageName": "MESSAGE_TO_SKILL",
            "messageId": mid,
            "uuid": {
                "userChannel": "B2C",
                "userId": uid
            },
            "payload": {
                "message": {
                    "original_text": text
                }
            }
        }

    @staticmethod
    def create_event_message(mid, uid, event, params=None):
        return {
            "messageName": "SERVER_ACTION",
            "messageId": mid,
            "uuid": {
                "userChannel": "B2C",
                "userId": uid
            },
            "payload": {
                "server_action": {
                    "action_id": event,
                    "parameters": params if params else {}
                }
            }
        }

    def _send(self, message):
        headers = {
            'Content-type': 'application/json',
            'Accept': '*/*'
        }
        logger.debug(f"Send: {message} to {self.webhook}")

        return requests.post(
            self.webhook,
            data=json.dumps(message),
            headers=headers
        )

    def send_text(self, mid, uid, text):
        response = self._send(self.create_text_message(mid, uid, text))
        logger.debug(f"Response on text: {response.text}")
        return response.json()

    def send_event(self, mid, uid, event):
        response = self._send(self.create_event_message(mid, uid, event))
        logger.debug(f"Response on event: {response.text}")
        return response.json()


class IDEtoTelegramResponseMapper:
    @staticmethod
    def _build_keyboard(suggestions):
        keyboard = []
        line = []
        index = 0

        for suggest in suggestions:
            title = suggest.get("title", None)
            if title:
                button = InlineKeyboardButton(title, callback_data=title)
            else:
                continue
            line.append(button)

            index += 1
            if index == 3:
                index = 0
                keyboard.append(line)
                line = []

        if line:
            keyboard.append(line)

        return keyboard

    @staticmethod
    def _reply(reply, text, reply_markup=None):
        if reply_markup:
            reply(text=text, reply_markup=reply_markup)
        else:
            reply(text=text)

    @staticmethod
    def _get_text(item):
        return item.get("bubble", {}).get("text", "")

    def reply_text(self, reply, message):
        payload = message.get("payload", {})
        suggestions = payload.get("suggestions", {}).get("buttons", [])
        keyboard = self._build_keyboard(suggestions)

        reply_markup = InlineKeyboardMarkup(keyboard)
        items = payload.get("items", [])

        if not items and not suggestions:
            return
        elif not items:
            self._reply(reply, "", reply_markup)
            return
        for item in items[:-1]:
            text = self._get_text(item)
            if text:
                self._reply(reply, text)
        if items[-1].get("type", None) == "STOP":
            return items[-1].get("data", {})
        else:
            self._reply(reply, self._get_text(items[-1]), reply_markup)

    def edit_reply_text(self, edit, reply, message):
        payload = message.get("payload", {})
        suggestions = payload.get("suggestions", {}).get("buttons", [])
        keyboard = self._build_keyboard(suggestions)
        reply_markup = InlineKeyboardMarkup(keyboard)
        items = payload.get("items", [])

        self._reply(edit, self._get_text(items[0]) if items else "", reply_markup)
        if len(items) < 2:
            return

        for item in items[1:-1]:
            text = self._get_text(item)
            if text:
                self._reply(reply, text)

        self._reply(reply, self._get_text(items[-1]), reply_markup)




