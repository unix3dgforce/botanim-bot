from typing import cast

import telegram
from telegram import Chat, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes


class BaseHandler:
    async def send_response(
            self,
            update: Update,
            context: ContextTypes.DEFAULT_TYPE,
            response: str,
            keyboard: InlineKeyboardMarkup | None = None,
    ) -> None:
        args = {
            "chat_id": cast(Chat, update.effective_chat).id,
            "text": response,
            "parse_mode": telegram.constants.ParseMode.HTML,
        }
        if keyboard:
            args["reply_markup"] = keyboard
        await context.bot.send_message(**args)
