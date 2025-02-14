
# https://www.pythonanywhere.com/user/imvickykumar999/tasks_tab/
import requests
import os

bot_token = os.getenv("TELEGRAM_BOT_TOKEN")

gets = f'https://api.telegram.org/bot{bot_token}/getUpdates'
req = requests.get(gets) 

show = req.json()
lst = list(show.values())[1]

bot_message = '''
Good morning, 
Read our blogs.

https://blogforge.pythonanywhere.com
'''

for i in lst:
  bot_chatID = i['message']['chat']['id']
  sets = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'    
  requests.post(sets)
