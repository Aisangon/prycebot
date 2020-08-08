from decouple import config
# from pricebot.spiders import Shop4DeSpider
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging

class PriceBot():

    def __init__(self):
        self.process = CrawlerProcess()
        TG_TOKEN = config('TELEGRAM_TOKEN')

        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        updater = Updater(TG_TOKEN, use_context=True)
        dp = updater.dispatcher
        
        dp.add_handler(CommandHandler("start", self.start))
        dp.add_handler(CommandHandler("help", self.help_command))
        dp.add_handler(CommandHandler("crawl", self.crawl))
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))

        updater.start_polling()
        updater.idle()

    def start(self, update, context):
        """Send a message when the command /start is issued."""
        update.message.reply_text('Hi!')

    def help_command(self, update, context):
        """Send a message when the command /help is issued."""
        update.message.reply_text('Help!')

    def echo(self, update, context):
        """Echo the user message."""
        update.message.reply_text(update.message.text)

    def crawl(self, update, context):
        self.process.crawl('shop4de')
        self.process.start()

if __name__ == '__main__':
    pricebot = PriceBot()