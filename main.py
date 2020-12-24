import telepot
import requests
import sys
from Summoner import Summoner
from bs4 import BeautifulSoup
from pprint import pprint

TOKEN = sys.argv[1]

def get_info(summoner_name, type):
    url = 'https://www.op.gg/summoner/userName={}'.format(summoner_name)
    r = requests.get(url)
    bs = BeautifulSoup(r.text, "html.parser")

    user = Summoner(summoner_name)

    # get summoner info
    if type == 1:
        try:
            user.get_summoner_info(bs)
            return user
        except:
            return None
    # get match list
    elif type == 2:
        try:
            user.get_match_list(bs)
            return user
        except:
            return None

def handler(msg):
    content_type, chat_type, chat_id, msg_date, msg_id = telepot.glance(msg, long=True)
    pprint(msg)
    print('-'*100)

    if content_type == 'text':
        str_msg = msg['text']
        # /이면 명령 실행
        if str_msg[0:1] == '/':
            args = str_msg.split(" ")
            command = args[0]
            del args[0]

            bot.sendMessage(chat_id, "plz wait...")

            if command == '/user':
                name = ' '.join(args)
                summoner = get_info(name, 1)
                if summoner is not None:
                    bot.sendMessage(chat_id, summoner.msg_summoner_info())
                else:
                    bot.sendMessage(chat_id, "This user is not registered.")
            elif command == '/match':
                name = ' '.join(args)
                summoner = get_info(name, 2)
                if summoner is not None:
                    bot.sendMessage(chat_id, summoner.msg_match_list())
                else:
                    bot.sendMessage(chat_id, "This user is not registered.")



bot = telepot.Bot(TOKEN)
bot.message_loop(handler, run_forever=True)