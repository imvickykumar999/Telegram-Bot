
# https://www.pythonanywhere.com/user/imvickykumar999/tasks_tab/
import requests

bot_token = '6297291074:AAFzpuG7i3GNqUgx9Wj5JNxHF6WF_TCufhk'
gets = f'https://api.telegram.org/bot{bot_token}/getUpdates'
req = requests.get(gets) 

show = req.json()
lst = list(show.values())[1]

bot_message = '''
Good morning, 
Here is today's news.

https://inshorts.com/en/read
'''

for i in lst:
  bot_chatID = i['message']['chat']['id']
  sets = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={bot_chatID}&parse_mode=Markdown&text={bot_message}'    
  requests.post(sets)
