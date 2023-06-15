import configparser
import redis
import telebot
import sys
import os

from utils.db.db_api import Database

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
config = configparser.ConfigParser()
config.read('./data/config.ini')

db = Database(
    host=config['Mysql']['hostname'],
    user=config['Mysql']['user'],
    password=config['Mysql']['password'],
    db=config['Mysql']['db'],
)

cache = redis.Redis(
    host=config['Redis']['hostname'],
    port=config['Redis']['port'],
    db=config['Redis']['db'],
    charset=config['Redis']['charset'],
    decode_responses=True
)
state_storage = telebot.storage.StateRedisStorage(
    host=config['Redis']['hostname'],
    port=config['Redis']['port'],
    db=config['Redis']['db']
)

bot = telebot.TeleBot(
    token=config['DEFAULT']['token'],
    state_storage=state_storage,
    parse_mode="Markdown",
    disable_web_page_preview=True
)

me = bot.get_me()
