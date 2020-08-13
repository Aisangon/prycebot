import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import logging
from decouple import config
from pricebot.spiders.shop4de import Shop4DeSpider
from pricebot.spiders.quotes_spider import QuotesSpider
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from pubsub import pub

class PriceBot():

    my_list = []

    def __init__(self, crawler):
        self.crawler = crawler
        self.process = CrawlerProcess(get_project_settings())
        TG_TOKEN = config('TELEGRAM_TOKEN')

        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        pub.subscribe(self.listener, 'rootTopic')

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
        d = self.process.crawl(self.crawler)
        d.addCallback(lambda result: self.successCallback(result, update))
        self.process.start(stop_after_crawl=True)

    def listener(self, arg1):
        self.my_list.append(arg1)
        return self.my_list

    def successCallback(self, result, update):
        for message in self.my_list:
            update.message.reply_text(message, parse_mode='HTML')
        # update.message.reply_text(''.join(self.my_list), parse_mode=ParseMode.HTML)
        # self.process.stop()
        return result

if __name__ == '__main__':
    pricebot = PriceBot(QuotesSpider)