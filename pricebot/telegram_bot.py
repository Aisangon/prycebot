import os, sys
dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))
sys.path.insert(0, parent_dir_path)

import logging
from decouple import config
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from pubsub import pub
from threading import Thread
from pricebot.all_spiders import AllSpiders

class PriceBot():

    scraped_items = []
    TYPEIN, CONFIRM, RESTART = range(3)
    temp_query = ''

    def __init__(self, spiders):
        self.spiders = spiders
        self.process = CrawlerProcess(get_project_settings())

        logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

        pub.subscribe(self.listener, 'rootTopic')

        self.initBot()

    def start(self, update, context):
        user = update.message.from_user
        update.message.reply_text('Hi {0}! Please type in what you want to scrape.'.format(user.first_name))

        return self.TYPEIN

    def typeIn(self, update, context):
        self.setQuery(update.message.text)
        reply_keyboard = [['Yes', 'No']]

        update.message.reply_text('Start scraping your choice?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

        return self.CONFIRM

    def crawl(self, update, context):
        for spider in self.spiders:
            self.process.crawl(spider)

        d = self.process.join()
        d.addCallback(lambda result: self.successCallback(result, update))
        pub.sendMessage('queryTopic', query=self.temp_query)
        self.process.start(stop_after_crawl=True)

        return self.RESTART

    def cancel(self, update, context):
        update.message.reply_text('Bye! I hope we can talk again some day.')

        return ConversationHandler.END

    def restart(self, update, context):
        update.message.reply_text('Bot is restarting...')
        Thread(target=self.stop_and_restart).start()

        return ConversationHandler.END

    def stop_and_restart(self):
        self.updater.stop()
        os.execl(sys.executable, sys.executable, *sys.argv)

    def listener(self, arg1):
        self.scraped_items.append(arg1)
        return self.scraped_items

    def successCallback(self, result, update):
        reply_keyboard = [['Another', 'Done']]
        for message in self.scraped_items:
            update.message.reply_text(message, parse_mode='HTML')

        update.message.reply_text('These are your results! What would you want to do next?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    def setQuery(self, query):
        self.temp_query = query
        return self.temp_query

    def initBot(self):
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('hi', self.start)],
            states={
                self.TYPEIN: [MessageHandler(Filters.text & ~Filters.command, self.typeIn)],
                self.CONFIRM: [MessageHandler(Filters.regex('^(Yes)$'), self.crawl),
                        MessageHandler(Filters.regex('^(No)$'), self.typeIn)],
                self.RESTART: [MessageHandler(Filters.regex('^(Another$)'), self.restart),
                        MessageHandler(Filters.regex('^(Done)$'), self.cancel)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )

        TG_TOKEN = config('TELEGRAM_TOKEN')
        self.updater = Updater(TG_TOKEN, use_context=True)
        dp = self.updater.dispatcher
        dp.add_handler(conv_handler)
        dp.add_handler(CommandHandler('r', self.restart))

        self.updater.start_polling()
        self.updater.idle()

if __name__ == '__main__':
    allSpiders = AllSpiders()
    pricebot = PriceBot(allSpiders.get_list())