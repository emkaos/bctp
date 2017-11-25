import yaml
import telegram
import lsm
import bct
import time


# read config
def _read_config(filename):
    stream = open(filename, "r")
    config = yaml.load(stream)
    return config


def _get_telegram_bot(bot_key):
    bot = telegram.Bot(token=bot_key)
    return bot


def _is_empty(entry):
    return (not entry.content.strip() or entry.content.strip() == entry.username)


config = _read_config("config.yaml")
db = lsm.LSM(config["db"]["filename"])
bot = _get_telegram_bot(config["telegram"]["bot_key"])
my_chat_id = config["telegram"]["chat_id"]

for thread in config['threads']:
    (name,url) = thread.items()[0]
    entries = bct.read_last_page(url)

    for entry in entries:
        if not entry.id in db and not _is_empty(entry):
            message_text =  "= *" + name + "* =========\n" \
            + "[" + entry.username + "|" + entry.userrank + "]\n" \
            + entry.content
            db[entry.id] = "1"
            bot.send_message(chat_id=my_chat_id, text=message_text, parse_mode=telegram.ParseMode.MARKDOWN)
            time.sleep(0.05) # spam threshold






