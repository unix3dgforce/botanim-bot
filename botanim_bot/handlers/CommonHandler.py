from telegram import Update
from telegram.ext import ContextTypes
from botanim_bot.handlers import BaseHandler
from botanim_bot.common import Messages


class CommonHandler(BaseHandler):
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_response(update, context, Messages.GREETINGS)

    async def help_(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await self.send_response(update, context, Messages.HELP)
