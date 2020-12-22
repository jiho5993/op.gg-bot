import telepot
import requests
from Summoner import Summoner
from bs4 import BeautifulSoup
from pprint import pprint

TOKEN = ''

def get_user_info(summoner_name):
    url = 'https://www.op.gg/summoner/userName={}'.format(summoner_name)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "html.parser")

    # get summoner info
    try:
        user = Summoner(summoner_name)
        user.get_level(bs)
        user.get_rank(bs)
        return user
    except:
        return False

def make_message(summoner):
    if summoner is not False:
        result = '{}\n' \
                 'level: {}\n' \
                 'solo rank: {} ({})\n' \
                 'sub rank: {} ({})' \
            .format(summoner.name,
                    summoner.level,
                    summoner.solo_rank["tier"],
                    summoner.solo_rank["point"],
                    summoner.sub_rank["tier"],
                    summoner.sub_rank["point"],
                    )
        return result
    return "This user is not registered."

def handler(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    pprint(msg)

    if content_type == 'text':
        str_msg = msg['text']
        if str_msg[0:1] == '/':
            args = str_msg.split(" ")
            command = args[0]
            del args[0]

            if command == '/user':
                name = ' '.join(args)
                result = make_message(get_user_info(name))
                bot.sendMessage(chat_id, result)

bot = telepot.Bot(TOKEN)
bot.message_loop(handler, run_forever=True)