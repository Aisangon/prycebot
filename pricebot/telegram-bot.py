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
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from pubsub import pub
from threading import Thread

class PriceBot():

    scraped_items = []
    TYPEIN,  CRAWL, RESTART = range(3)

    def __init__(self, crawler):
        self.crawler = crawler
        self.process = CrawlerProcess(get_project_settings())

        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        pub.subscribe(self.listener, 'rootTopic')

        self.initBot()

    # def echo(self, update, context):
    #     update.message.reply_text(update.message.text)

    def typeIn(self, update, context):
        user = update.message.from_user
        update.message.reply_text('Hi' + user + '! Please type in what you want to scrape.')

        return CRAWL

    def crawl(self, update, context):
        d = self.process.crawl(self.crawler)
        d.addCallback(lambda result: self.successCallback(result, update))
        self.process.start(stop_after_crawl=True)

        return RESTART

    def cancel(self, update, context):
        update.message.reply_text('Bye! I hope we can talk again some day.',
                                reply_markup=ReplyKeyboardRemove())

        return ConversationHandler.END

    def restart(self, update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=self.stop_and_restart).start()

    def stop_and_restart(self):
        self.updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def listener(self, arg1):
        self.scraped_items.append(arg1)
        return self.scraped_items

    def successCallback(self, result, update):
        for message in self.scraped_items:
            update.message.reply_text(message, parse_mode='HTML')
        return result

    def initBot(self):

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('hi', start)],
            states={
                TYPEIN: [MessageHandler(Filters.text & ~Filters.command, self.typeIn)],
                CRAWL: [MessageHandler(Filters.text & ~Filters.command, self.crawl)],
                RESTART: [MessageHandler(Filters.text & ~Filters.command, self.restart)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        TG_TOKEN = config('TELEGRAM_TOKEN')
        self.updater = Updater(TG_TOKEN, use_context=True)
        dp = self.updater.dispatcher

        dp.add_handler(conv_handler)
        # dp.add_handler(CommandHandler("crawl", self.crawl))
        # dp.add_handler(MessageHandler(Filters.text & ~Filters.command, self.echo))
        # dp.add_handler(CommandHandler('r', self.restart))

        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    pricebot = PriceBot(QuotesSpider)